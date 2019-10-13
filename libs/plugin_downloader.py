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
from system.plugin_downloader import TackemSystemPluginDownloader


def plugin_download_page(full_system: bool = True) -> str:
    '''returns the web page for choosing plugins'''
    TackemSystemPluginDownloader().get_github_plugins()
    TackemSystemPluginDownloader().get_local_plugins()
    html = "<h2>GITHUB PLUGINS</h2>"
    plugin_count = 0
    panels_html = ""
    for plugin in GITHUB_PLUGINS:
        title = plugin['plugin_type'] + " - " + plugin['plugin_name']
        loaded = False
        if plugin['downloaded']:
            loaded = TackemSystemPluginDownloader().is_plugin_loaded(
                plugin['plugin_type'],
                plugin['plugin_name']
            )
            if loaded:
                plugin_count += 1

        clear_config = html_parts.input_button_with_data(
            "Clear Config",
            class_name="pluginbutton",
            data={'plugin':plugin['name']},
            outer_div=False,
            enabled=not loaded,
            visible=(full_system and plugin['downloaded'])
        )
        clear_database = html_parts.input_button_with_data(
            "Clear Database",
            class_name="pluginbutton",
            data={'plugin':plugin['name']},
            outer_div=False,
            enabled=not loaded,
            visible=(full_system and plugin['downloaded'])
        )
        add_remove = html_parts.input_button_with_data(
            ("Delete" if plugin['downloaded'] else "Download"),
            class_name="pluginbutton",
            data={'plugin':plugin['name']},
            outer_div=False
        )

        stop_start_action = ""
        stop_start_enabled = True
        stop_start_visible = False

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
        return html
    html += html_parts.form("/", html_parts.hidden_page_index(3), "Next", "")
    if plugin_count == 0:
        html += '<script>$("button").prop("disabled", true);</script>'

    return html


def plugin_control(action: str, plugin_title: str) -> str:
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



def download_plugin(plugin_title, plugin_type, plugin_name) -> tuple(bool, int):
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


def delete_plugin(plugin_title: str, plugin_type: str, plugin_name: str) -> None:
    '''deletes the plugin'''
    if not stop_plugin_systems(plugin_type, plugin_name):
        return False

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


def update_plugins() -> None:
    '''function to use list from html page to download the plugins'''
    for plugin in GITHUB_PLUGINS:
        if plugin['downloaded']:
            update_plugin(plugin['plugin_type'], plugin['plugin_name'])


def update_plugin(plugin_type: str, plugin_name: str) -> bool:
    '''function to use list from html page to download the plugins'''
    if not stop_plugin_systems(plugin_type, plugin_name):
        return False
    location = PLUGINFOLDERLOCATION + plugin_type + '/' + plugin_name + '/'
    git.Repo(location).remotes.origin.pull()
    TackemSystemAdmin().reload_plugin(plugin_type, plugin_name)
    if start_plugin_systems(plugin_type, plugin_name):
        return True
    return False


def get_plugin_branches(plugin_type: str, plugin_name: str) -> list:
    '''Gets a list of branches'''
    location = PLUGINFOLDERLOCATION + plugin_type.lower() + "/" + plugin_name.lower()
    return [branch.name for branch in git.Repo(location).heads]


def get_current_plugin_branch(plugin_type: str, plugin_name: str) -> str:
    '''Gets the current branch'''
    location = PLUGINFOLDERLOCATION + plugin_type.lower() + "/" + plugin_name.lower()
    return git.Repo(location).active_branch()


def change_plugin_branch(plugin_type: str, plugin_name: str, branch: str) -> bool:
    '''will change the branch for the plugin'''
    location = PLUGINFOLDERLOCATION + plugin_type.lower() + "/" + plugin_name.lower()
    repo = git.Repo(location)
    if branch in [branch.name for branch in repo.heads]:
        repo.heads[branch].checkout()
        return True
    return False


def reload_plugin(plugin_type: str, plugin_name: str) -> bool:
    '''Function to attempt to reload the plugin after a failed install'''
    TackemSystemAdmin().write_config_to_disk()
    if not TackemSystemAdmin().load_plugin(plugin_type, plugin_name):
        return False
    TackemSystemAdmin().load_plugin_cfgs()
    TackemSystemAdmin().load_config()
    return True


def start_plugin_systems(plugin_type: str, plugin_name: str) -> bool:
    '''function to start up the plugins systems'''
    if TackemSystemAdmin().is_plugin_loaded(plugin_type, plugin_name):
        return False
    reload_plugin(plugin_type, plugin_name)
    TackemSystemAdmin().load_plugin_systems(plugin_type, plugin_name)
    return True


def stop_plugin_systems(plugin_type: str, plugin_name: str) -> bool:
    '''function to start up the plugins systems'''
    if not TackemSystemAdmin().is_plugin_loaded(plugin_type, plugin_name):
        return False
    TackemSystemAdmin().stop_plugin_systems(plugin_type, plugin_name)
    TackemSystemAdmin().write_config_to_disk()
    TackemSystemAdmin().delete_plugin(plugin_type, plugin_name)
    TackemSystemAdmin().delete_plugin_cfg(plugin_type, plugin_name)
    uninstall_plugin_modules(plugin_type, plugin_name)
    TackemSystemAdmin().load_config()
    return True


def clean_config_after_deletion(plugin_type: str, plugin_name: str, backup: bool - True) -> None:
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


def clean_db_after_deletion(plugin_type: str, plugin_name: str) -> None:
    '''function to clean the Database after plugin removal'''
    sql = TackemSystemAdmin().sql
    name_like = plugin_type + "_" + plugin_name + "_%"
    results = sql.select_like(SYSTEM_NAME, "table_version", {'name':name_like})
    for result in results:
        sql.call(SYSTEM_NAME, "DROP TABLE " + result['name'] + ";")
        sql.delete_row(SYSTEM_NAME, "table_version", result['id'])


def javascript() -> str:
    '''Javascript File'''
    return str(open("www/javascript/plugindownloader.js", "r").read())





def uninstall_plugin_modules(plugin_type: str, plugin_name: str) -> None:
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
