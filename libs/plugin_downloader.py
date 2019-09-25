'''System for downloading plugins'''
import json
import os
import platform
import shutil
import subprocess
import sys
from datetime import datetime
from glob import glob
import git
import requests
from libs.plugin_base import load_plugin_settings
import libs.html_parts as html_parts
from libs.startup_arguments import PLUGINFOLDERLOCATION, PROGRAMCONFIGLOCATION
from system.admin import TackemSystemAdmin

#TODO Need to figure out how to tell the user they need to install additional software

SYSTEM_NAME = "plugin_downloader"

HOST_NAME = "GaryTheBrown"
HOST_API_URL = "https://api.github.com/users/" + HOST_NAME + "/repos"

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

def plugin_download_page(full_system=True):
    '''returns the web page for choosing plugins'''
    html = "<h2>GITHUB PLUGINS</h2>"
    plugin_count = 0
    panels_html = ""
    for plugin in GITHUB_PLUGINS:
        title = plugin['plugin_type'] + " - " + plugin['plugin_name']
        if plugin['downloaded']:
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
        if full_system:
            # if plugin running:
            stop_start_action = "Start/Stop"
        else:
            stop_start_action = "Reload"
            stop_start_enabled = not TackemSystemAdmin().is_plugin_loaded(plugin['plugin_type'],
                                                                          plugin['plugin_name'])
        start_stop = html_parts.input_button_with_data(
            stop_start_action,
            class_name="pluginbutton",
            data={'plugin':plugin['name']},
            outer_div=False,
            enabled=stop_start_enabled,
            visible=plugin['downloaded']
        )
        panels_html += html_parts.plugin_panel(title, plugin['description'], clear_config,
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
    html += html_parts.hidden("new_plugin_count", str(NEW_PLUGIN_COUNT), True)
    if full_system:
        html += html_parts.form("/", "", "Exit", "")
    else:
        html += html_parts.form("/", html_parts.hidden_page_index(3), "Next", "")
    if plugin_count == 0:
        html += '<script>$("button").prop("disabled", true);</script>'
    html += html_parts.dim_screen()
    return html

def update_plugins():
    '''function to use list from html page to download the plugins'''
    for plugin in GITHUB_PLUGINS:
        location = PLUGINFOLDERLOCATION + plugin['plugin_type'] + '/' + plugin['plugin_name'] + '/'
        if plugin['downloaded']:
            git.Repo(location).remotes.origin.pull()
            #TODO Loading Of The Module using importlib.reload([module])

def download_plugin(plugin_title):
    '''function to use list from html page to download the plugins'''
    #TODO need to make this return info for the page to tell the user or if possible send a request
    # for user password if can be done safely
    name_split = plugin_title.split("-")
    plugin_type = name_split[-2].lower()
    plugin_name = name_split[-1].lower()
    os.makedirs(PLUGINFOLDERLOCATION + plugin_type + "/" + plugin_name, exist_ok=True)
    for plugin in GITHUB_PLUGINS:
        if plugin['name'] == plugin_title:
            location = PLUGINFOLDERLOCATION + plugin_type.lower() + "/" + plugin_name.lower()
            git.Repo.clone_from(plugin['clone_url'], location)
            install_plugin_modules(plugin_type, plugin_name)
            TackemSystemAdmin().write_config_to_disk()
            if not TackemSystemAdmin().load_plugin(plugin_type, plugin_name):
                return download_plugin_failed(plugin_type, plugin_name)
            TackemSystemAdmin().load_plugin_cfgs()
            TackemSystemAdmin().load_config()

            plugin['downloaded'] = True
            return True

def download_plugin_failed(plugin_type, plugin_name):
    '''if the download plugin fails then find out why'''
    return_string = "This Plugin Requires extra Programs Please Install: "
    plugin_json_file = PLUGINFOLDERLOCATION + plugin_type + "/" + plugin_name + "/settings.json"
    plugin_settings = load_plugin_settings(plugin_json_file)
    if platform.system() == 'Linux':
        return_string += " ".join(plugin_settings.get('linux_programs', ["N/A"]))
    else:
        return_string += "N/A"
    return_string += "\n"
    if os.path.isfile("/indocker"):
        return_string += """
You are running an docker you need to install the above programs or pick a image that contains the
required programs for the plugin"""

    return return_string


def delete_plugin(plugin_title):
    '''deletes the plugin'''
    name_split = plugin_title.split("-")
    plugin_type = name_split[-2].lower()
    plugin_name = name_split[-1].lower()
    TackemSystemAdmin().write_config_to_disk()
    TackemSystemAdmin().delete_plugin(plugin_type, plugin_name)
    uninstall_plugin_modules(plugin_type, plugin_name)
    folder = PLUGINFOLDERLOCATION + plugin_type + "/" + plugin_name + "/"
    shutil.rmtree(folder)
    for plugin in GITHUB_PLUGINS:
        if plugin['name'] == plugin_title:
            plugin['downloaded'] = False
    try:
        os.rmdir(PLUGINFOLDERLOCATION + plugin_type)
    except OSError:
        pass
    TackemSystemAdmin().delete_plugin_cfg(plugin_type, plugin_name)
    TackemSystemAdmin().load_config()

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

def clean_db_after_deletion(plugin_type, plugin_name, sql):
    '''function to clean the Database after plugin removal'''
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
