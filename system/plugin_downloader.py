'''System for downloading plugins'''
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from glob import glob
from typing import Union
import git
import requests
import markdown
from libs.startup_arguments import PLUGINFOLDERLOCATION, PROGRAMCONFIGLOCATION
from system.admin import TackemSystemAdmin

class TackemSystemPluginDownloader(TackemSystemAdmin):
    '''System for downloading plugins'''
    __SYSTEM_NAME = "plugin_downloader"
    __REPO_BRANCH = "master"
    __HOST_NAME = "GaryTheBrown"
    __HOST_API_URL = "https://api.github.com/users/{}/repos".format(__HOST_NAME)
    __HOST_RAW_URL = "https://raw.githubusercontent.com/{}/".format(__HOST_NAME)
    __HOST_RAW_URL2 = "/{}/".format(__REPO_BRANCH)

    __GITHUB_PLUGINS = []
    __LOCAL_PLUGINS = []


    def __init__(self):
        self.get_local_plugins()
        self.get_github_plugins()

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
                    'folder':folder,
                    'plugin_name':folder_split[-2],
                    'plugin_type':folder_split[-3],
                    'repo':self.is_git_repo(folder),
                    'offical': self.is_origin_offical(folder,
                                                      folder_split[-2].capitalize(),
                                                      folder_split[-3].capitalize()
                                                     )
                }

                self.__LOCAL_PLUGINS.append(local_plugin)

    #TODO Find out if you can use ssh way
    #Need to also figure out what to send through the api for install and uninstall
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
                    'name':item['name'].lstrip(),
                    'description':item['description'],
                    'clone_url':item['clone_url'],
                    #Local Info
                    'plugin_name':name_split[-1],
                    'plugin_type':name_split[-2],
                    'downloaded':False
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
        folder = PLUGINFOLDERLOCATION + plugin_type.lower() + "/" + plugin_name.lower() + "/"
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


    def download_plugin(self, plugin_type: str, plugin_name: str) -> Union[str, bool]:
        '''function to use list from html page to download the plugins'''
        try:
            os.makedirs(PLUGINFOLDERLOCATION + plugin_type + "/" + plugin_name)
        except OSError:
            return "FOLDER ALREADY EXISTS"
        for plugin in self.__GITHUB_PLUGINS:
            if plugin['plugin_type'] == plugin_type and plugin['plugin_name'] == plugin_name:
                location = PLUGINFOLDERLOCATION + plugin_type.lower() + "/" + plugin_name.lower()
                git.Repo.clone_from(plugin['clone_url'], location, branch=self.__REPO_BRANCH)
                return True
        return "PLUGIN NOT IN LIST [BUG]"


    def reload_plugin(self, plugin_type: str, plugin_name: str) -> bool:
        '''Function to attempt to reload the plugin after a failed install'''
        self.write_config_to_disk()
        if not self.load_plugin(plugin_type, plugin_name):
            return False
        self.load_plugin_cfgs()
        self.load_config()
        return True


    def install_plugin_modules(self, plugin_type: str, plugin_name: str) -> None: #(pip)
        '''install plugin modiles'''
        plugin_folder = plugin_type + "/" + plugin_name + "/"
        requirements_file = PLUGINFOLDERLOCATION + plugin_folder + "requirements.txt"
        if os.path.exists(requirements_file):
            print("installing plugin requirements..")
            pip_call = [sys.executable, '-m', 'pip', 'install', '-r', requirements_file, '--user']
            subprocess.check_call(pip_call)
            print("installed plugin requirements")
