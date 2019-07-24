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

# Need to figure out how to tell the user they need to install additional software for the plugin
# need to create two pages one with only add option and the other to allow deletion of config and
# database stuff as an option when deleting a plugin
# don't allow deletion of local only plugins (no git) (user must delete files, config & db)
# first run
# needs to hide the next button unless at least 1 plugin downloaded.
# needs to show a restart button once at least 1 plugin has been downloaded
# restart page needs to send the user back to this page
# main system
# needs to only show the restart option once a plugin is added or deleted otherwise no buttons


GITHUB_PLUGINS = []
LOCAL_PLUGINS = []
def is_git_repo(path):
    '''quick script to check if folder is a git repo'''
    try:
        _ = git.Repo(path).git_dir
        return True
    except git.InvalidGitRepositoryError:
        return False

def get_local_plugins():
    '''gets a list of local plugins'''
    LOCAL_PLUGINS.clear()
    for folder in glob("plugins/*/*/"):
        if not "__pycache__" in folder:
            folder_split = folder.split("/")
            local_plugin = {
                'plugin_name':folder_split[-2],
                'plugin_type':folder_split[-3],
                'repo':is_git_repo(folder)
            }

            LOCAL_PLUGINS.append(local_plugin)

def get_github_plugins():
    '''grabs the list of plugins on github and checks if local'''
    GITHUB_PLUGINS.clear()
    response = requests.get("https://api.github.com/users/garythebrown/repos")

    for item in json.loads(response.text):
        if 'Tackem-Plugin-' in item['name']:
            name_split = item['name'].split("-")
            save = {
                'name':item['name'],
                'description':item['description'],
                'clone_url':item['clone_url'],
                #Local Info
                'plugin_name':name_split[-1],
                'plugin_type':name_split[-2],
                'downloaded':False,
                'download':False,
            }

            temp = {'print_name': name_split[-1], 'plugin_type': name_split[-2]}
            if temp in LOCAL_PLUGINS:
                save['downloaded'] = True
            GITHUB_PLUGINS.append(save)

def plugin_download_page():
    '''returns the web page for choosing plugins'''
    html = "<h2>GITHUB PLUGINS</h2>"
    panels_html = ""
    for plugin in GITHUB_PLUGINS:
        title = plugin['plugin_type'] + " - " + plugin['plugin_name']
        control = html_parts.input_button("Add", "")
        variable_name = plugin['plugin_type'] + "-" + plugin['plugin_name']
        section_html = plugin['description']
        panels_html += html_parts.panel(title, control, "", variable_name, section_html)
    html += panels_html
    html += "<h2>LOCAL PLUGINS</h2>"
    for plugin in LOCAL_PLUGINS:
        title = plugin['plugin_type'] + " - " + plugin['plugin_name']
        if plugin['repo']:
            control = "[REPO]"
        else:
            control = ""
        panels_html += "<H4>" + title + " " + control + "</H4>"
    html += panels_html
    return html_parts.form("/", html_parts.hidden_page_index(3), "Next", html)

def update_plugins():
    '''function to use list from html page to download the plugins'''
    for plugin in GITHUB_PLUGINS:
        if plugin['downloaded']:
            plugin_location = 'plugins/' + plugin['plugin_type'] + '/' + plugin['plugin_name'] + '/'
            git.Repo(plugin_location).remotes.origin.pull()

def download_plugin(plugin_type, plugin_name):
    '''function to use list from html page to download the plugins'''
    os.mkdir("plugins/" + plugin_type + "/" + plugin_name, exist_ok=True)
    for plugin in GITHUB_PLUGINS:
        if plugin['plugin_name'] == plugin_name and plugin['plugin_type'] == plugin_type:
            git.Repo.clone_from(plugin['clone_url'], "plugins/" + plugin_type + "/" + plugin_name)
            break

def delete_plugin(plugin_type, plugin_name):
    '''deletes the plugin'''
    shutil.rmtree("plugins/" + plugin_type + "/" + plugin_name)
    try:
        os.rmdir("plugins/" + plugin_type)
    except OSError:
        pass

def clean_config_after_deletion(plugin_type, plugin_name, config):
    '''function to remove data from the config'''
    config_file = PROGRAMCONFIGLOCATION + "config.ini"
    config_backup = PROGRAMCONFIGLOCATION + "config.bak" + datetime.now().strftime("%Y%m%d%H%M%S")
    shutil.copyfile(config_file, config_backup)
    del config['plugins'][plugin_type][plugin_name]
    if not config['plugins'][plugin_type]:
        del config['plugins'][plugin_type]

def clean_db_after_deletion(plugin_type, plugin_name, config):
    '''function to clean the Database after plugin removal'''
    #SELECT name FROM table_version WHERE name LIKE '[PLUGIN_TYPE]_[PLUGIN_NAME]_%';
    #drop all the tables
    #remove rows from table_version

get_local_plugins()
get_github_plugins()
