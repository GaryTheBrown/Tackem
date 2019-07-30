'''System for downloading plugins'''
import os
import json
import shutil
from glob import glob
from datetime import datetime
import git
import requests
from libs.startup_arguments import PROGRAMCONFIGLOCATION
import libs.html_parts as html_parts
# from system.admin import TackemSystemAdmin

# Need to figure out how to tell the user they need to install additional software for the plugin

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
            location = "plugins/" + name_split[-2].lower() + "/" + name_split[-1].lower()
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

def button_remove(name):
    '''returns the remove button'''
    return "RemovePlugin('" + name + "')"

def button_add(name):
    '''returns the remove button'''
    return "DownloadPlugin('" + name + "')"

def no_button():
    '''returns the on system text'''
    return "[On System]"

def plugin_download_page(full_system=True):
    '''returns the web page for choosing plugins'''
    html = "<h2>GITHUB PLUGINS</h2>"
    plugin_count = 0
    panels_html = ""
    for plugin in GITHUB_PLUGINS:
        title = plugin['plugin_type'] + " - " + plugin['plugin_name']
        add_remove = ""
        start_stop = ""
        clear_config = ""
        clear_database = ""
        if full_system:
            #TODO Make these check if they are there and if so show them so you can delete this info
            # regardless of if the plugin is there.
            clear_config = html_parts.input_button("Remove Config", "", False)
            clear_database = html_parts.input_button("Remove Data", "", False)
        if plugin['downloaded']:
            if full_system:
                add_remove = html_parts.input_button("Remove", button_remove(plugin['name']), False)
            else:
                add_remove = no_button()
            plugin_count += 1
        else:
            add_remove = html_parts.input_button("Add", button_add(plugin['name']), False)
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
    html += html_parts.input_button("Restart", "Restart()", False)
    if plugin_count == 0:
        html += '<script>$("button").prop("disabled", true);</script>'
    if NEW_PLUGIN_COUNT == 0:
        html += '<script>$(\'input[value="Restart"]\').hide();</script>'
    html += html_parts.dim_screen()
    return html

def update_plugins():
    '''function to use list from html page to download the plugins'''
    for plugin in GITHUB_PLUGINS:
        if plugin['downloaded']:
            plugin_location = 'plugins/' + plugin['plugin_type'] + '/' + plugin['plugin_name'] + '/'
            git.Repo(plugin_location).remotes.origin.pull()

def download_plugin(plugin_title):
    '''function to use list from html page to download the plugins'''
    name_split = plugin_title.split("-")
    plugin_type = name_split[-2].lower()
    plugin_name = name_split[-1].lower()
    os.makedirs("plugins/" + plugin_type + "/" + plugin_name, exist_ok=True)
    for plugin in GITHUB_PLUGINS:
        if plugin['name'] == plugin_title:
            location = "plugins/" + plugin_type.lower() + "/" + plugin_name.lower()
            git.Repo.clone_from(plugin['clone_url'], location)
            plugin['downloaded'] = True
            break

def delete_plugin(plugin_title):
    '''deletes the plugin'''
    #TODO DO I NEED TO KILL THE PLUGIN THROUGH HERE .ACCESS THE PLUGIN AND STOP
    # MAYBE EVEN LOOK AT BEING ABLE TO ADD OR REMOVE PLUGINS LIVE TO SAVE RESTARTS. MAY NEED TO
    # SPLIT THE DATA FROM TACKEM WITH CONTROLS FOR ADDING AND REMOVING PLUGINS AND MAKING IT SAFE TO
    # DO LIVE STARTS AND STOPS. COULD LOOK INTO DOING THIS SO CONFIG UPDATES THAT DISABLES PLUGINS
    # WILL THEN NOT NEED THE REBOOT. THIS COULD THEN BE EXPANDED TO ALLOW GIT UPDATES TO RELOAD THE
    # PLUGIN
    name_split = plugin_title.split("-")
    plugin_type = name_split[-2].lower()
    plugin_name = name_split[-1].lower()
    folder = "plugins/" + plugin_type + "/" + plugin_name + "/"
    shutil.rmtree(folder)
    for plugin in GITHUB_PLUGINS:
        if plugin['name'] == plugin_title:
            plugin['downloaded'] = False
    try:
        os.rmdir("plugins/" + plugin_type)
    except OSError:
        pass

def clean_config_after_deletion(plugin_type, plugin_name, config, backup=True):
    '''function to remove data from the config'''
    #TODO DEBUG THIS
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
    #TODO TEST THIS
    name_like = plugin_type + "_" + plugin_name + "_%"
    results = sql.select_like(SYSTEM_NAME, "table_version", {'name':name_like})
    for result in results:
        sql.call(SYSTEM_NAME, "DROP TABLE " + result['name'] + ";")
        sql.delete_row(SYSTEM_NAME, "table_version", result['id'])

get_local_plugins()
get_github_plugins()
