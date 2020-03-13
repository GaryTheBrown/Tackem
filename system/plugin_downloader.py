'''System for downloading plugins'''
import json
import os
import shutil
import subprocess
import sys
from glob import glob
from typing import Union
import git
import requests
import markdown
from libs.startup_arguments import PLUGINFOLDERLOCATION
from config_data import CONFIG
from system.admin import TackemSystemAdmin


class TackemSystemPluginDownloader(TackemSystemAdmin):
    '''System for downloading plugins'''

    __REPO_BRANCH = "master"
    __HOST_NAME = "GaryTheBrown"
    __HOST_API_URL = "https://api.github.com/users/{}/repos".format(
        __HOST_NAME)
    __HOST_RAW_URL = "https://raw.githubusercontent.com/{}/".format(
        __HOST_NAME)
    __HOST_RAW_URL2 = "/{}/".format(__REPO_BRANCH)

    __GITHUB_PLUGINS = []
    __LOCAL_PLUGINS = []

    @property
    def github_plugins(self):
        '''returns the github plugins'''
        return self.__GITHUB_PLUGINS

    @property
    def local_plugins(self):
        '''returns the local plugins'''
        return self.__LOCAL_PLUGINS

    def is_git_repo(self, path: str) -> bool:
        '''quick script to check if folder is a git repo'''
        try:
            _ = git.Repo(path).git_dir
            return True
        except git.InvalidGitRepositoryError:
            return False

    def is_origin_offical(self, path: str, plugin_name: str, plugin_type: str) -> bool:
        '''checks if repo is linked to the offical github'''
        url = ""
        try:
            url = git.Repo(path).remotes.origin.url.lower()
        except git.InvalidGitRepositoryError:
            return False
        if plugin_name.lower() in url and plugin_type.lower() in url \
                and self.__HOST_NAME.lower() in url:
            return True
        return False

    def get_local_plugins(self) -> None:
        '''gets a list of local plugins'''
        self.__LOCAL_PLUGINS.clear()
        for folder in glob("plugins/*/*/"):
            if not "__pycache__" in folder:
                folder_split = folder.split("/")
                local_plugin = {
                    'folder': folder,
                    'plugin_name': folder_split[-2],
                    'plugin_type': folder_split[-3],
                    'repo': self.is_git_repo(folder),
                    'offical': self.is_origin_offical(folder,
                                                      folder_split[-2].capitalize(),
                                                      folder_split[-3].capitalize()
                                                      )
                }

                self.__LOCAL_PLUGINS.append(local_plugin)

    def get_github_plugins(self) -> None:
        '''grabs the list of plugins on github and checks if local'''
        self.__GITHUB_PLUGINS.clear()
        response = requests.get(self.__HOST_API_URL)

        for item in json.loads(response.text):
            if 'Tackem-Plugin-' in item['name']:
                name_split = item['name'].split("-")
                location = PLUGINFOLDERLOCATION + name_split[-2].lower()
                location += "/" + name_split[-1].lower()
                save = {
                    'name': item['name'].lstrip(),
                    'description': item['description'],
                    'clone_url': item['clone_url'],
                    # Local Info
                    'plugin_name': name_split[-1],
                    'plugin_type': name_split[-2],
                    'downloaded': False
                }
                if os.path.exists(location):
                    try:
                        url = git.Repo(location).remotes.origin.url
                    except git.InvalidGitRepositoryError:
                        url = ""
                    if item['name'] in url and self.__HOST_NAME in url and "github.com" in url:
                        save['downloaded'] = True

                self.__GITHUB_PLUGINS.append(save)

    def get_single_file(
        self,
        plugin_type: str,
        plugin_name: str,
        file_to_get: str
    ) -> Union[str, None]:
        '''grabs a single file from github'''
        folder = PLUGINFOLDERLOCATION + plugin_type.lower() + "/" + \
            plugin_name.lower() + "/"
        if os.path.isfile(folder + file_to_get):
            return str(open(folder + file_to_get, "r").read())
        plugin = "Tackem-plugin-" + plugin_type + "-" + plugin_name
        link = self.__HOST_RAW_URL + plugin + self.__HOST_RAW_URL2 + file_to_get
        return_data = requests.get(link)
        if return_data.status_code == 200:
            return return_data.text
        return None

    def get_readme_as_html(self, plugin_type: str, plugin_name: str) -> str:
        '''turns the readme.nd into html'''
        readme = self.get_single_file(plugin_type, plugin_name, "README.md")
        readme = "\n".join(readme.split("\n")[3:])
        if readme is None or readme == "":
            return None
        return markdown.markdown(readme, output_format="html5")

    def download_plugin(self, plugin_type: str, plugin_name: str) -> tuple:
        '''function to use list from html page to download the plugins'''
        location = PLUGINFOLDERLOCATION + plugin_type.lower() + "/" + plugin_name.lower()
        try:
            os.makedirs(location)
        except OSError:
            if os.path.exists(location + "/.git"):
                return "PLUGIN ALREADY EXISTS", 0
        for plugin in self.__GITHUB_PLUGINS:
            if plugin['plugin_type'].lower() == plugin_type.lower() \
                    and plugin['plugin_name'].lower() == plugin_name.lower():
                git.Repo.clone_from(
                    plugin['clone_url'], location, branch=self.__REPO_BRANCH)
                return True, 0
        return "PLUGIN NOT IN LIST [BUG]", 1

    def reload_plugin(self, plugin_type: str, plugin_name: str) -> tuple:
        '''Function to attempt to reload the plugin after a failed install'''
        CONFIG.save()
        return_data = self.import_plugin(plugin_type, plugin_name)
        if return_data[0] is not True:
            return return_data
        CONFIG.load()
        return True, 0

    def install_plugin_modules(self, plugin_type: str, plugin_name: str) -> None:  # (pip)
        '''install plugin modiles'''
        plugin_folder = plugin_type + "/" + plugin_name + "/"
        requirements_file = PLUGINFOLDERLOCATION + plugin_folder + "requirements.txt"
        if os.path.exists(requirements_file):
            print("installing plugin requirements..")
            pip_call = [sys.executable, '-m', 'pip',
                        'install', '-r', requirements_file, '--user']
            subprocess.check_call(pip_call)
            print("installed plugin requirements")

    def uninstall_plugin_modules(self, plugin_type: str, plugin_name: str) -> None:
        '''uninstall plugin modiles'''
        plugin_folder = plugin_type + "/" + plugin_name + "/"
        requirements_file = PLUGINFOLDERLOCATION + plugin_folder + "requirements.txt"
        if os.path.exists(requirements_file):
            print("uninstalling plugin requirements..")
            pip_call = [sys.executable, '-m', 'pip',
                        'uninstall', '-y', '-r', requirements_file]
            subprocess.check_call(pip_call)
            print("uninstalled plugin requirements")

    def delete_plugin(self, plugin_type: str, plugin_name: str) -> tuple:
        '''deletes the plugin'''
        folder = PLUGINFOLDERLOCATION + plugin_type + "/" + plugin_name + "/"
        try:
            shutil.rmtree(folder)
        except OSError:
            return "CANNOT DELETE THE FOLDER ({})".format(folder), 1
        for plugin in self.__GITHUB_PLUGINS:
            if plugin['plugin_type'] == plugin_type and plugin['plugin_name'] == plugin_name:
                plugin['downloaded'] = False
                break
        try:
            os.rmdir(PLUGINFOLDERLOCATION + plugin_type)
        except OSError:
            pass

        return True, 0

    def update_plugins(self) -> None:
        '''function to use list from html page to download the plugins'''
        for plugin in self.__GITHUB_PLUGINS:
            if plugin['downloaded']:
                self.update_plugin(
                    plugin['plugin_type'], plugin['plugin_name'])

    def update_plugin(self, plugin_type: str, plugin_name: str) -> None:
        '''function to use list from html page to download the plugins'''
        location = PLUGINFOLDERLOCATION + plugin_type + '/' + plugin_name + '/'
        git.Repo(location).remotes.origin.pull()
        return True

    def get_plugin_branches(self, plugin_type: str, plugin_name: str) -> list:
        '''Gets a list of branches'''
        location = PLUGINFOLDERLOCATION + plugin_type.lower() + "/" + plugin_name.lower()
        return [branch.name for branch in git.Repo(location).heads]

    def get_current_plugin_branch(self, plugin_type: str, plugin_name: str) -> str:
        '''Gets the current branch'''
        location = PLUGINFOLDERLOCATION + plugin_type.lower() + "/" + plugin_name.lower()
        return git.Repo(location).active_branch()

    def change_plugin_branch(self, plugin_type: str, plugin_name: str, branch: str) -> bool:
        '''will change the branch for the plugin'''
        location = PLUGINFOLDERLOCATION + plugin_type.lower() + "/" + plugin_name.lower()
        repo = git.Repo(location)
        if branch in [branch.name for branch in repo.heads]:
            repo.heads[branch].checkout()
            return True
        return False
