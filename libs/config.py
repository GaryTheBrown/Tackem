'''Config File Setup'''
from collections import OrderedDict
from configobj import ConfigObj
from validate import Validator
from libs.config_list import ConfigList
from libs.config_object import ConfigObject
from libs.config_option import ConfigOption

#TODO PULL ALL HTML CODE OUT AND PUT IT INTO INDIVIDUAL FILES SO THEY CAN BE CHANGED in Theming
#TODO ADD A WAY OF RELOADING OR EVEN ADDING AN INSTANCE OF THE PLUGIN TO THE SYSTEM
#TODO ALSO MAKE IT POSSIBLE TO SHUTDOWN THE PLUGIN

CONFIG = ConfigList("root", None)
CONFIG.append(ConfigObject("", "", "", config_group="plugins"))
CONFIG.append(
    ConfigObject("operationmode", "Operation Mode", "option",
                 config_group="system",
                 default='SINGLE',
                 input_type='radio',
                 options=[ConfigOption("SINGLE",
                                       toggle_sections=([], ['master', 'slave']),
                                       enable_disable=[('webui', False, None),
                                                       ('api', False, None)]),
                          ConfigOption("MASTER",
                                       toggle_sections=(['master'], ['slave']),
                                       enable_disable=[('webui', True, True),
                                                       ('api', True, True)],
                                       disabled=True),
                          ConfigOption("SLAVE",
                                       toggle_sections=(['slave'], ['master']),
                                       enable_disable=[('webui', True, False),
                                                       ('api', True, True)],
                                       disabled=True)],
                 help_text="""
Is this program running alone or acting as part of a multi computer setup<br>
<i>DISABLED OPTIONS AS NOT IMPLEMENTED YET</i>"""))

#Master Only
CONFIG.append(
    ConfigObject("portrangefrom", "Port Range From", "integer", config_group="system",
                 minimum=1001, maximum=65535, default=50000, section="master", help_text="""
The Min range of allowed ports for communication between systems"""))
CONFIG.append(
    ConfigObject("portrangeto", "Port Range To", "integer", config_group="system",
                 minimum=1001, maximum=65535, default=50100, section="master", help_text="""
The Max range of allowed ports for communication between systems"""))
#Slave Only
CONFIG.append(
    ConfigObject("masteraddress", "Master Address", "string", config_group="system",
                 default="", section="slave", help_text="The master systems address or mastername"))
CONFIG.append(
    ConfigObject("masterport", "Master Port", "integer", config_group="system",
                 minimum=1001, maximum=65535, default=8081, section="slave", help_text="""
The master systems API/WebUI port"""))
CONFIG.append(
    ConfigObject("masterapikey", "Master API Key", "string", config_group="system",
                 default="", section="slave", help_text="The master systems API key"))

CONFIG.append(
    ConfigObject("mode", "Database System", "option",
                 config_group="database",
                 default='SQLite3',
                 input_type='radio',
                 options=[ConfigOption("SQLite3", hide="mysql"),
                          ConfigOption("MYSQL", show="mysql", disabled=True)], help_text="""
Is this The Database Connection used for the software<br>
<i>DISABLED OPTIONS AS NOT IMPLEMENTED YET</i>"""))
CONFIG.append(
    ConfigObject("address", "Database Address", "string", config_group="database",
                 default="localhost", section="mysql", help_text="""
The database address or mastername"""))
CONFIG.append(
    ConfigObject("port", "Database Port", "integer", config_group="database",
                 minimum=1001, maximum=65535, default=3306, section="mysql", help_text="""
The database port"""))
CONFIG.append(
    ConfigObject("username", "Database Username", "string", config_group="database",
                 default="", section="mysql", help_text="The database username"))
CONFIG.append(
    ConfigObject("password", "Database Password", "password", config_group="database",
                 default="", section="mysql", help_text="The database password"))
CONFIG.append(
    ConfigObject("name", "Database Name", "string", config_group="database",
                 default="tackem", section="mysql", help_text="The database Name"))
CONFIG.append(ConfigObject("enabled", "Enabled", "boolean", config_group="api", default=False,
                           toggle_section="api", input_type="switch"))
CONFIG.append(ConfigObject("masterkey", "Master API Key", "string", config_group="api", default='',
                           button="Generate API Key",
                           button_onclick="GenerateAPIKey('api_masterkey');",
                           help_text="The master API key for slaves to access"))
CONFIG.append(ConfigObject("userkey", "User API Key", "string", config_group="api", default='',
                           button="Generate API Key",
                           button_onclick="GenerateAPIKey('api_userkey');",
                           help_text="The user API key for slaves to access"))
#<br><small>Leave blank to work on per plugin API's for extra security</small>

CONFIG.append(ConfigObject("enabled", "Enabled", "boolean", config_group="webui", default=True,
                           toggle_section="webui", input_type="switch"))
CONFIG.append(
    ConfigObject("port", "Port", "integer", config_group="webui",
                 minimum=1001, maximum=65535, default=8081, help_text="The port for the WebUI"))
CONFIG.append(
    ConfigObject("baseurl", "Base Url", "string", config_group="webui",
                 default="", help_text="The Base URL"))

def config_load(path, plugin_configs):
    """Create a config file using a configspec and validate it against a Validator object"""
    _spec = CONFIG.get_cfg("").replace("$$PLUGIN_CONFIGS$$", plugin_configs, 1).split("\n")
    config = ConfigObj(path, configspec=_spec)
    validator = Validator()
    config.validate(validator, copy=True)
    config.filename = path
    return config

def post_config_settings(kwargs, config, plugins):
    '''Fills in the config dict with the settings based on its name'''
    for key in kwargs:
        key_list = key.split("_")
        if key_list[0] == "cs":
            val = ""
            location = ""
            if key_list[1] in plugins:
                if plugins[key_list[1]].SETTINGS['single_instance']:
                    location = "single"
                    val = plugins[key_list[1]].CONFIG.convert_var(None,
                                                                  key_list[2], kwargs[key])
                else:
                    location = "multi"
                    val = plugins[key_list[1]].CONFIG.convert_var("__many__",
                                                                  key_list[3], kwargs[key])
            else:
                location = "root"
                val = CONFIG.convert_var(key_list[1], key_list[2], kwargs[key])
            if val is None:
                continue
            if location == "root":
                config[key_list[1]][key_list[2]] = val
            elif location == "multi":
                if not key_list[2] in config["plugins"][key_list[1]]:
                    config["plugins"][key_list[1]][key_list[2]] = {}
                config["plugins"][key_list[1]][key_list[2]][key_list[3]] = val
            elif location == "single":
                if len(key_list) == 2:
                    config["plugins"][key_list[1]] = val
                elif len(key_list) == 3:
                    config["plugins"][key_list[1]][key_list[2]] = val
                elif len(key_list) == 4:
                    config["plugins"][key_list[1]][key_list[2]][key_list[3]] = val
                elif len(key_list) == 5:
                    config["plugins"][key_list[1]][key_list[2]][key_list[3]][key_list[4]] = val

def full_config_page(config_dict, plugins):
    '''returns a full config page layout for all systems'''

    root_string = _get_root_configs_page(config_dict)
    replace_data = CONFIG.get_list_of_vars_and_values(config_dict)
    for key in replace_data:
        root_string = root_string.replace(key, str(replace_data[key]))

    groups = CONFIG.get_groups()
    for group in groups:
        value = config_dict.get(group, {}).get('enabled', None)
        default = CONFIG.get_default(group, 'enabled')

        replace_hidden = ""
        if value is False or (value is None and default is False):
            replace_hidden = 'style="display:none"'
        root_string = root_string.replace("%%" + group.upper() + "ENABLED%%", replace_hidden)

    plugin_string = _get_plugin_configs_page(plugins, config_dict.get("plugins", {}))
    replace_data = {}
    plugin_config = config_dict.get('plugins', {})
    for key in plugins:
        config_part = plugin_config.get(key, {})
        if not plugins[key].SETTINGS['single_instance']:
            if not config_part:
                plugin_string = plugin_string.replace("%%" + key.upper() + "SECTION%%", '')
                continue
            plugin_groups = plugins[key].CONFIG.get_groups()
            section_html = ""
            for item in config_part:
                if isinstance(config_part[item], dict):
                    if not item in plugin_groups:
                        section_html += get_multi_setup(plugins, key, config_part, item)
            plugin_string = plugin_string.replace("%%" + key.upper() + "SECTION%%", section_html)
    for key in replace_data:
        plugin_string = plugin_string.replace(key, str(replace_data[key]))

    baseurl = config_dict.get("webui", {}).get("baseurl", "")

    page = root_string + plugin_string

    form_html = str(open("www/html/inputs/form.html", "r").read())
    form_html = form_html.replace("%%RETURNURL%%", baseurl + "/config")
    hidden_html = str(open("www/html/inputs/hiddenpageindex.html", "r").read())
    hidden_html = hidden_html.replace("%%PAGEINDEX%%", "RESTART")
    form_html = form_html.replace("%%HIDDEN%%", hidden_html)
    form_html = form_html.replace("%%BUTTONLABEL%%", "Save")
    form_html = form_html.replace("%%PAGE%%", page)
    return form_html

def root_config_page():
    '''setup for Libraries'''
    form_html = str(open("www/html/inputs/form.html", "r").read())
    form_html = form_html.replace("%%RETURNURL%%", "/")
    hidden_html = str(open("www/html/inputs/hiddenpageindex.html", "r").read())
    hidden_html = hidden_html.replace("%%PAGEINDEX%%", "2")
    form_html = form_html.replace("%%HIDDEN%%", hidden_html)
    form_html = form_html.replace("%%BUTTONLABEL%%", "Next")
    form_html = form_html.replace("%%PAGE%%", _get_root_configs_page({}))

    replace_data = CONFIG.get_list_of_vars_and_defaults()
    for key in replace_data:
        form_html = form_html.replace(key, replace_data[key])

    groups = CONFIG.get_groups()
    for group in groups:
        if CONFIG.get_default(group, 'enabled', True):
            form_html = form_html.replace("%%" + group.upper() + "ENABLED%%", '')
        else:
            form_html = form_html.replace("%%" + group.upper() + "ENABLED%%",
                                          'style="display:none"')
    return form_html

def _get_root_configs_page(config):
    '''setup for Libraries'''
    sections = CONFIG.get_only_html_options(config)
    page = str(open("www/config/root_config_page.html", "r").read())
    page = page.replace("%%PLUGINLIST%%", sections)
    page = page.replace("%%PLUGIN%%_", "")
    page = page.replace("root_", "")
    page = page.replace("%%PLUGIN%%", "")
    return page

def plugin_config_page(plugins):
    '''setup for Libraries'''
    form_html = str(open("www/html/inputs/form.html", "r").read())
    form_html = form_html.replace("%%RETURNURL%%", "/")
    hidden_html = str(open("www/html/inputs/hiddenpageindex.html", "r").read())
    hidden_html = hidden_html.replace("%%PAGEINDEX%%", "3")
    form_html = form_html.replace("%%HIDDEN%%", hidden_html)
    form_html = form_html.replace("%%BUTTONLABEL%%", "Save & Restart")
    form_html = form_html.replace("%%PAGE%%", _get_plugin_configs_page(plugins, {}))

    replace_data = {}
    for key in plugins:
        if plugins[key].SETTINGS['single_instance']:
            replace_data.update(plugins[key].CONFIG.get_list_of_vars_and_defaults(key))
        else:
            form_html = form_html.replace("%%" + key.upper() + "SECTION%%", "")
    for key in replace_data:
        form_html = form_html.replace(key, replace_data[key])

    return form_html

def _get_plugin_configs_page(plugins, config):
    '''setup for Libraries'''
    plugin_lists = []
    sorted_plugins = OrderedDict(sorted(plugins.items()))
    plugin_types = []
    for key in sorted_plugins:
        plugin = ""
        plugin_type = plugins[key].SETTINGS['type']
        if not plugin_type in plugin_types:
            plugin_types.append(plugin_type)
        plugins[key].CONFIG.sort_config()
        if plugins[key].SETTINGS['single_instance']:
            plugin = plugins[key].CONFIG.single_instance_load(config.get(key, {}))
        else:
            plugin = plugins[key].CONFIG.multi_instance_load()
        plugin = plugin.replace("%%PLUGINNAME%%", key)
        if plugin != "":
            plugin_lists.append((plugin_type, plugin))

    navlink_html, plugins_html = _plugin_panel_and_nav_create(plugin_lists, plugin_types)

    page = str(open("www/config/plugin_config_page.html", "r").read())
    return page.replace("%%PANELTABS%%", navlink_html).replace("%%PLUGINLIST%%", plugins_html)

def _plugin_panel_and_nav_create(plugins, plugin_types):
    '''create and return plugin section and its navigation'''
    tabbar_html = str(open("www/html/inputs/tabbar.html", "r").read())
    tabbar_item_html = str(open("www/html/inputs/tabbaritem.html", "r").read())
    tabpane_item_html = str(open("www/html/inputs/tabpane.html", "r").read())
    tabbar_items_html = ""
    tabpanes_html = ""
    first_window = True
    for plugin_type in plugin_types:
        tabbar_item = tabbar_item_html.replace("%%PLUGINTYPE%%", plugin_type)
        tabbar_item = tabbar_item.replace("%%PLUGINTYPECAPITALIZE%%", plugin_type.capitalize())
        tabpane_item = tabpane_item_html.replace("%%PLUGINTYPE%%", plugin_type)
        if first_window:
            tabbar_item = tabbar_item.replace("%%ACTIVE%%", 'active')
            tabpane_item = tabpane_item.replace("%%ACTIVE%%", 'active')
            first_window = False
        else:
            tabbar_item = tabbar_item.replace(" %%ACTIVE%%", '')
            tabpane_item = tabpane_item.replace(" %%ACTIVE%%", '')
        tabbar_items_html += tabbar_item
        plugins_html = ''
        for plugin in plugins:
            if plugin[0] == plugin_type:
                plugins_html += plugin[1]
        tabpanes_html += tabpane_item.replace("%%PLUGIN%%", plugins_html)

    tabbar_html = tabbar_html.replace("%%TABBARITEMS%%", tabbar_items_html)
    return tabbar_html, tabpanes_html

def get_multi_setup(plugins, plugin, config, name=""):
    '''Return the information needed for the setup of the plugin'''
    if plugins[plugin].SETTINGS['single_instance']:
        return "<BAD>"
    data = plugins[plugin].CONFIG.get_multi_html_options(config)
    data = data.replace("%%NAME%%", name)
    data = data.replace("%%PLUGIN%%", plugin)
    data = data.replace("%%PLUGINTYPE%%", plugins[plugin].SETTINGS['type'])
    data = data.replace("%%VARNAME%%", name.replace(" ", ""))
    data = data.replace("%%TITLE%%", name.capitalize())
    data = data.replace("%%SCRIPT%%", "")
    return data

def javascript():
    '''Javascript File'''
    return str(open("www/config/config.js", "r").read())
