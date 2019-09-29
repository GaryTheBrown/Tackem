'''System for downloading plugins'''
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from glob import glob
import git
import requests
import markdown
import libs.html_parts as html_parts
from libs.startup_arguments import PLUGINFOLDERLOCATION, PROGRAMCONFIGLOCATION
from system.admin import TackemSystemAdmin

SYSTEM_NAME = "plugin_downloader"

REPO_BRANCH = "master"
HOST_NAME = "GaryTheBrown"
HOST_API_URL = "https://api.github.com/users/" + HOST_NAME + "/repos"
HOST_RAW_URL = "https://raw.githubusercontent.com/" + HOST_NAME + "/"
HOST_RAW_URL2 = "/" + REPO_BRANCH + "/"

GITHUB_PLUGINS = []
LOCAL_PLUGINS = []
NEW_PLUGIN_COUNT = 0

def is_git_repo(path):
    '''quick script to check if folder is a git repo'''
    try:
        _ = git.Repo(path).git_dir
        return True
    except git.InvalidGitRepositoryError:
        return False

def is_origin_offical(path, plugin_name, plugin_type):
    '''checks if repo is linked to the offical github'''
    url = ""
    try:
        url = git.Repo(path).remotes.origin.url.lower()
    except git.InvalidGitRepositoryError:
        return False
    if plugin_name.lower() in url and plugin_type.lower() in url and HOST_NAME.lower() in url:
        return True
    return False

def get_local_plugins():
    '''gets a list of local plugins'''
    LOCAL_PLUGINS.clear()
    for folder in glob("plugins/*/*/"):
        if not "__pycache__" in folder:
            folder_split = folder.split("/")
            local_plugin = {
                'folder':folder,
                'plugin_name':folder_split[-2],
                'plugin_type':folder_split[-3],
                'repo':is_git_repo(folder),
                'offical': is_origin_offical(folder,
                                             folder_split[-2].capitalize(),
                                             folder_split[-3].capitalize()
                                            )
            }

            LOCAL_PLUGINS.append(local_plugin)

def get_github_plugins():
    '''grabs the list of plugins on github and checks if local'''
    GITHUB_PLUGINS.clear()
    response = requests.get(HOST_API_URL)

    for item in json.loads(response.text):
        if 'Tackem-Plugin-' in item['name']:
            name_split = item['name'].split("-")
            location = PLUGINFOLDERLOCATION + name_split[-2].lower() + "/" + name_split[-1].lower()
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
                if item['name'] in url and HOST_NAME in url and "github.com" in url:
                    save['downloaded'] = True

            GITHUB_PLUGINS.append(save)

def get_single_file(plugin_type, plugin_name, file_to_get):
    '''grabs a single file from github'''
    folder = PLUGINFOLDERLOCATION + plugin_type.lower() + "/" + plugin_name.lower() + "/"
    if os.path.isfile(folder + file_to_get):
        return str(open(folder + file_to_get, "r").read())
    plugin = "Tackem-plugin-" + plugin_type + "-" + plugin_name
    link = HOST_RAW_URL + plugin + HOST_RAW_URL2 + file_to_get
    return_data = requests.get(link)
    if return_data.status_code == 200:
        return return_data.text
    return None

def plugin_download_page(full_system=True):
    '''returns the web page for choosing plugins'''
    html = "<h2>GITHUB PLUGINS</h2>"
    plugin_count = 0
    panels_html = ""
    for plugin in GITHUB_PLUGINS:
        title = plugin['plugin_type'] + " - " + plugin['plugin_name']
        if plugin['downloaded']:
            if TackemSystemAdmin().is_plugin_loaded(plugin['plugin_type'], plugin['plugin_name']):
                plugin_count += 1

        clear_config = html_parts.input_button_with_data(
            "Clear Config",
            class_name="pluginbutton",
            data={'plugin':plugin['name']},
            outer_div=False,
            enabled=False,
            visible=(full_system and plugin['downloaded'])
        )
        clear_database = html_parts.input_button_with_data(
            "Clear Database",
            class_name="pluginbutton",
            data={'plugin':plugin['name']},
            outer_div=False,
            enabled=False,
            visible=(full_system and plugin['downloaded'])
        )
        add_remove = html_parts.input_button_with_data(
            ("Remove" if plugin['downloaded'] else "Add"),
            class_name="pluginbutton",
            data={'plugin':plugin['name']},
            outer_div=False
        )

        stop_start_action = ""
        stop_start_enabled = True
        stop_start_visible = False
        loaded = TackemSystemAdmin().is_plugin_loaded(plugin['plugin_type'], plugin['plugin_name'])
        if full_system:
            stop_start_visible = plugin['downloaded']
            stop_start_action = "Stop" if loaded else "Start"
        else:
            stop_start_action = "Reload"
            stop_start_visible = plugin['downloaded'] and not loaded

        start_stop = html_parts.input_button_with_data(
            stop_start_action,
            class_name="pluginbutton",
            data={'plugin':plugin['name']},
            outer_div=False,
            enabled=stop_start_enabled,
            visible=stop_start_visible
        )
        readme = get_readme_as_html(plugin['plugin_type'], plugin['plugin_name'])
        if readme is None:
            readme = plugin['description']
        panels_html += html_parts.plugin_panel(title, readme, clear_config,
                                               clear_database, start_stop, add_remove)
    html += panels_html
    html += "<h2>LOCAL PLUGINS</h2>"
    panels_html = ""
    for plugin in LOCAL_PLUGINS:
        if not plugin['offical']:
            title = plugin['plugin_type'] + " - " + plugin['plugin_name']
            offical = ""
            if plugin['repo']:
                offical = "[repo]"
            panels_html += "<H4>" + title + "</H4>" + offical
    html += panels_html
    html += html_parts.hidden("plugin_count", str(plugin_count), True)
    if full_system:
        html += html_parts.form("/", "", "Exit", "")
    else:
        html += html_parts.form("/", html_parts.hidden_page_index(3), "Next", "")
    if plugin_count == 0:
        html += '<script>$("button").prop("disabled", true);</script>'

    return html

def plugin_control(action, plugin_title):
    '''function to link to all actions for plugin control'''
    return_data = {
        'success' : False,
        'code' : 0,
        'message' : None,
    }
    name_split = plugin_title.split("-")
    plugin_type = name_split[-2].lower()
    plugin_name = name_split[-1].lower()

    if action == "Add":
        success, error = download_plugin(plugin_title, plugin_type, plugin_name)
        if success:
            print(plugin_type, plugin_name, "Installed")
            return_data['success'] = True
        else:
            if error == 0:
                print(plugin_type, plugin_name, " Folder Already Exists")
                return_data['code'] = 1
                return_data['message'] = "Folder Already Exists"
            elif error == 1:
                print(plugin_type, plugin_name, "Failed to Install")
                return_data['code'] = 2
                if os.path.isfile("/indocker"):
                    return_data['message'] = """
You are running inside a docker container you need to pick an image that contains the required
programs for the plugin"""
                else:
                    return_data['message'] = """
This Plugin Requires extra Programs Please see the readme"""

    elif action == "Remove":
        if delete_plugin(plugin_title, plugin_type, plugin_name):
            print(plugin_type, plugin_name, "Deleted")
            return_data['success'] = True
        else:
            print(plugin_type, plugin_name, "Removal Fail")
            return_data['message'] = "Removal Failed"
    elif action == "Reload":
        if reload_plugin(plugin_type, plugin_name):
            print(plugin_type, plugin_name, "Reloaded")
            return_data['success'] = True
        else:
            print(plugin_type, plugin_name, "Reload Failed")
            return_data['message'] = "Reload Failed"
    elif action == "Clear Config":
        if clean_config_after_deletion(plugin_type, plugin_name):
            print(plugin_type, plugin_name, "Removed From Config")
            return_data['success'] = True
        else:
            print(plugin_type, plugin_name, "Removal from Config Failed")
            return_data['message'] = "Removal from Config Failed"
    elif action == "Clear Database":
        if clean_db_after_deletion(plugin_type, plugin_name):
            print(plugin_type, plugin_name, "Removed From DB")
            return_data['success'] = True
        else:
            print(plugin_type, plugin_name, "Removal from DB Failed")
            return_data['message'] = "Removal from DB Failed"
    elif action == "Start":
        if start_plugin_systems(plugin_type, plugin_name):
            print(plugin_type, plugin_name, "Systems Started")
            return_data['success'] = True
        else:
            print(plugin_type, plugin_name, "Starting Failed")
            return_data['message'] = "Starting Failed"
    elif action == "Stop":
        if stop_plugin_systems(plugin_type, plugin_name):
            print(plugin_type, plugin_name, "Systems Stopped")
            return_data['success'] = True
        else:
            print(plugin_type, plugin_name, "Stopping Failed")
            return_data['message'] = "Stopping Failed"

    return json.dumps(return_data)

def get_readme_as_html(plugin_type, plugin_name):
    '''turns the readme.nd into html'''
    readme = get_single_file(plugin_type, plugin_name, "README.md")
    readme = "\n".join(readme.split("\n")[3:])
    if readme is None or readme == "":
        return None
    return markdown.markdown(readme, output_format="html5")

def download_plugin(plugin_title, plugin_type, plugin_name):
    '''function to use list from html page to download the plugins'''
    try:
        os.makedirs(PLUGINFOLDERLOCATION + plugin_type + "/" + plugin_name)
    except OSError:
        return False, 0
    for plugin in GITHUB_PLUGINS:
        if plugin['name'] == plugin_title:
            location = PLUGINFOLDERLOCATION + plugin_type.lower() + "/" + plugin_name.lower()
            git.Repo.clone_from(plugin['clone_url'], location, branch=REPO_BRANCH)
            install_plugin_modules(plugin_type, plugin_name)
            if reload_plugin(plugin_type, plugin_name):
                return True, 0
            return False, 1


def delete_plugin(plugin_title, plugin_type, plugin_name):
    '''deletes the plugin'''
    if TackemSystemAdmin().is_plugin_loaded(plugin_type, plugin_name):
        TackemSystemAdmin().write_config_to_disk()
        TackemSystemAdmin().delete_plugin(plugin_type, plugin_name)
        TackemSystemAdmin().delete_plugin_cfg(plugin_type, plugin_name)
        uninstall_plugin_modules(plugin_type, plugin_name)
        TackemSystemAdmin().load_config()
    folder = PLUGINFOLDERLOCATION + plugin_type + "/" + plugin_name + "/"
    try:
        shutil.rmtree(folder)
    except OSError:
        return False
    for plugin in GITHUB_PLUGINS:
        if plugin['name'] == plugin_title:
            plugin['downloaded'] = False
    try:
        os.rmdir(PLUGINFOLDERLOCATION + plugin_type)
    except OSError:
        pass

    return True

def update_plugins():
    '''function to use list from html page to download the plugins'''
    for plugin in GITHUB_PLUGINS:
        if plugin['downloaded']:
            update_plugin(plugin['plugin_type'], plugin['plugin_name'])

def update_plugin(plugin_type, plugin_name):
    '''function to use list from html page to download the plugins'''
    if not stop_plugin_systems(plugin_type, plugin_name):
        return False
    location = PLUGINFOLDERLOCATION + plugin_type + '/' + plugin_name + '/'
    git.Repo(location).remotes.origin.pull()
    TackemSystemAdmin().reload_plugin(plugin_type, plugin_name)
    if start_plugin_systems(plugin_type, plugin_name):
        return True
    return False

def get_plugin_branches(plugin_type, plugin_name):
    '''Gets a list of branches'''
    location = PLUGINFOLDERLOCATION + plugin_type.lower() + "/" + plugin_name.lower()
    return [branch.name for branch in git.Repo(location).heads]

def get_current_plugin_branch(plugin_type, plugin_name):
    '''Gets the current branch'''
    location = PLUGINFOLDERLOCATION + plugin_type.lower() + "/" + plugin_name.lower()
    return git.Repo(location).active_branch()

def change_plugin_branch(plugin_type, plugin_name, branch):
    '''will change the branch for the plugin'''
    location = PLUGINFOLDERLOCATION + plugin_type.lower() + "/" + plugin_name.lower()
    repo = git.Repo(location)
    if branch in [branch.name for branch in repo.heads]:
        repo.heads[branch].checkout()
        return True
    return False

def reload_plugin(plugin_type, plugin_name):
    '''Function to attempt to reload the plugin after a failed install'''
    TackemSystemAdmin().write_config_to_disk()
    if not TackemSystemAdmin().load_plugin(plugin_type, plugin_name):
        return False
    TackemSystemAdmin().load_plugin_cfgs()
    TackemSystemAdmin().load_config()
    return True

def start_plugin_systems(plugin_type, plugin_name):
    '''function to start up the plugins systems'''
    if TackemSystemAdmin().is_plugin_loaded(plugin_type, plugin_name):
        return False
    TackemSystemAdmin().load_plugin_systems(plugin_type, plugin_name)
    return True

def stop_plugin_systems(plugin_type, plugin_name):
    '''function to start up the plugins systems'''
    if not TackemSystemAdmin().is_plugin_loaded(plugin_type, plugin_name):
        return False
    TackemSystemAdmin().stop_plugin_systems(plugin_type, plugin_name)
    return True

def clean_config_after_deletion(plugin_type, plugin_name, backup=True):
    '''function to remove data from the config'''
    config = TackemSystemAdmin().get_global_config()
    if not config['plugins'][plugin_type][plugin_name]:
        return

    config_file = PROGRAMCONFIGLOCATION + "config.ini"
    if backup:
        time_format = "%Y%m%d%H%M%S"
        config_backup = PROGRAMCONFIGLOCATION + "config.bak" + datetime.now().strftime(time_format)
        shutil.copyfile(config_file, config_backup)
    config['plugins'][plugin_type][plugin_name].clear()
    del config['plugins'][plugin_type][plugin_name]
    if not config['plugins'][plugin_type]:
        del config['plugins'][plugin_type]
    config.write()

def clean_db_after_deletion(plugin_type, plugin_name):
    '''function to clean the Database after plugin removal'''
    sql = TackemSystemAdmin().get_sql()
    name_like = plugin_type + "_" + plugin_name + "_%"
    results = sql.select_like(SYSTEM_NAME, "table_version", {'name':name_like})
    for result in results:
        sql.call(SYSTEM_NAME, "DROP TABLE " + result['name'] + ";")
        sql.delete_row(SYSTEM_NAME, "table_version", result['id'])


def javascript():
    '''Javascript File'''
    return str(open("www/javascript/plugindownloader.js", "r").read())


#plugin Modules (pip)
def install_plugin_modules(plugin_type, plugin_name):
    '''install plugin modiles'''
    plugin_folder = plugin_type + "/" + plugin_name + "/"
    requirements_file = PLUGINFOLDERLOCATION + plugin_folder + "requirements.txt"
    if os.path.exists(requirements_file):
        print("installing plugin requirements..")
        pip_call = [sys.executable, '-m', 'pip', 'install', '-r', requirements_file, '--user']
        subprocess.check_call(pip_call)
        print("installed plugin requirements")

def uninstall_plugin_modules(plugin_type, plugin_name):
    '''uninstall plugin modiles'''
    plugin_folder = plugin_type + "/" + plugin_name + "/"
    requirements_file = PLUGINFOLDERLOCATION + plugin_folder + "requirements.txt"
    if os.path.exists(requirements_file):
        print("uninstalling plugin requirements..")
        pip_call = [sys.executable, '-m', 'pip', 'uninstall', '-y', '-r', requirements_file]
        subprocess.check_call(pip_call)
        print("uninstalled plugin requirements")


get_local_plugins()
get_github_plugins()
