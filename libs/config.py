'''Config File Setup'''
from configobj import ConfigObj
from validate import Validator
from libs.config_list import ConfigList
from libs.config_object import ConfigObject
from libs.config_option import ConfigOption
import libs.html_parts as html_part

# TO DO PULL ALL HTML CODE OUT AND PUT IT INTO INDIVIDUAL FILES SO THEY CAN BE CHANGED in Theming
# TO DO ADD A WAY OF RELOADING OR EVEN ADDING AN INSTANCE OF THE PLUGIN TO THE SYSTEM
# TO DO ALSO MAKE IT POSSIBLE TO SHUTDOWN THE PLUGIN

CONFIG = ConfigList("root")
CONFIG.append(
    ConfigList("system", objects=[
        ConfigObject("operationmode", "Operation Mode", "option", default='single',
                     input_type='radio', options=[
                         ConfigOption("single", "SINGLE",
                                      toggle_sections=([], ['system_master', 'system_slave'])),
                         ConfigOption("master", "MASTER", disabled=True,
                                      toggle_sections=(['system_master'], ['system_slave'])),
                         ConfigOption("slave", "SLAVE", disabled=True,
                                      toggle_sections=(['system_slave'], ['system_master']))
                     ],
                     help_text="""
Is this program running alone or acting as part of a multi computer setup"""),
        #Master Only
        ConfigList("master", objects=[
            ConfigObject("portrangefrom", "Port Range From", "integer", minimum=1001, maximum=65535,
                         default=50000, help_text="""
    The Min range of allowed ports for communication between systems"""),
            ConfigObject("portrangeto", "Port Range To", "integer", minimum=1001, maximum=65535,
                         default=50100, help_text="""
    The Max range of allowed ports for communication between systems""")
        ], is_section=True, section_link=["system", "operationmode"]),
        #Slave Only
        ConfigList("slave", objects=[
            ConfigObject("masteraddress", "Master Address", "string", default="",
                         help_text="The master systems address or mastername"),
            ConfigObject("masterport", "Master Port", "integer", minimum=1001, maximum=65535,
                         default=8081, help_text="The master systems API/WebUI port"),
            ConfigObject("masterapikey", "Master API Key", "string", default="",
                         help_text="The master systems API key")
        ], is_section=True, section_link=["system", "operationmode"])
    ])
)
CONFIG.append(
    ConfigList("database", objects=[
        ConfigObject("mode", "Database System", "option", default='sqlite3', input_type='radio',
                     options=[ConfigOption("sqlite3", "SQLite3", hide="database_mysql"),
                              ConfigOption("mysql", "MYSQL", show="database_mysql", disabled=True)],
                     help_text="Is this The Database Connection used for the software"),
        ConfigList("mysql", "MYSQL", objects=[
            ConfigObject("address", "Database Address", "string", default="localhost",
                         help_text="The database address or mastername"),
            ConfigObject("port", "Database Port", "integer", minimum=1001, maximum=65535,
                         default=3306, help_text="The database port"),
            ConfigObject("username", "Database Username", "string", default="",
                         help_text="The database username"),
            ConfigObject("password", "Database Password", "password", default="",
                         help_text="The database password"),
            ConfigObject("name", "Database Name", "string", default="tackem",
                         help_text="The database Name")
        ], is_section=True, section_link=["database", "mode"])
    ])
)
CONFIG.append(
    ConfigList("api", "API Interface", objects=[
        ConfigObject("enabled", "Enabled", "boolean", default=True, toggle_section="api",
                     input_type="switch"),
        ConfigObject("masterkey", "Master API Key", "string", default='', button="Generate API Key",
                     button_onclick="GenerateAPIKey('api_masterkey');",
                     help_text="The master API key for slaves to access"),
        ConfigObject("userkey", "User API Key", "string", default='', button="Generate API Key",
                     button_onclick="GenerateAPIKey('api_userkey');",
                     help_text="The user API key for slaves to access")
    ])
)
CONFIG.append(
    ConfigList("webui", "Web Interface", objects=[
        ConfigObject("enabled", "Enabled", "boolean", default=True, toggle_section="webui",
                     input_type="switch"),
        ConfigObject("port", "Port", "integer", minimum=1001, maximum=65535, default=8081,
                     help_text="The port for the WebUI"),
        ConfigObject("baseurl", "Base Url", "string", default="/", help_text="""The Base URL
must start with '/'""")
    ])
)
CONFIG.append(ConfigList("plugins"))# keep this one at the end of the config section

def config_load(path, plugin_configs):
    """Create a config file using a configspec and validate it against a Validator object"""
    temp_spec = CONFIG.get_root_spec() + plugin_configs
    _spec = temp_spec.split("\n")
    config = ConfigObj(path, configspec=_spec)
    validator = Validator()
    config.validate(validator, copy=True)
    config.filename = path
    return config

def javascript():
    '''Javascript File'''
    return str(open("www/javascript/config.js", "r").read())

def post_config_settings(kwargs, config, plugins):
    '''Fills in the config dict with the settings based on its name'''
    for key in kwargs:
        key_list = key.split("_")
        if key_list[0] == "cs":
            value = None
            if key_list[1] == "plugins":
                if key_list[2] in plugins and key_list[3] in plugins[key_list[2]]:
                    plugin = plugins[key_list[2]][key_list[3]]
                    if plugin.SETTINGS['single_instance']:
                        value = plugin.CONFIG.convert_var(key_list[4:], kwargs[key])
                    else:
                        value = plugin.CONFIG.convert_var(key_list[5:], kwargs[key])
            else:
                value = CONFIG.convert_var(key_list[1:], kwargs[key])
            if value is not None:
                add_val_to_config(config, key_list[1:], value)

def add_val_to_config(config, key_list, value):
    '''recursive way of adding value into the config'''
    if len(key_list) is 1:
        config[key_list[0]] = value
    else:
        if not config:
            config[key_list[0]] = {}
        elif key_list[0] not in config:
            config[key_list[0]] = {}
        add_val_to_config(config[key_list[0]], key_list[1:], value)

def root_config_page(config):
    '''get the full root config setup page into a form'''
    return html_part.form("/", html_part.hidden_page_index(2), "Next", _root_config_page(config))

def plugin_config_page(config, plugins):
    '''setup for Libraries into a form'''
    return html_part.form("/", html_part.hidden_page_index(3), "Save & Restart",
                          _plugin_config_page(config, plugins))

def full_config_page(config, plugins):
    '''get the full config setup page into a form'''
    baseurl = config.get("webui", {}).get("baseurl", "")
    return html_part.form(baseurl + "/config", "", "Save & Restart",
                          _root_config_page(config) + _plugin_config_page(config, plugins))

def _root_config_page(config):
    '''get the full root config setup page'''
    return html_part.root_config_page(CONFIG.get_config_html(config))

def _plugin_config_page(config, plugins):
    '''setup for Libraries'''
    plugin_tabs_html = ""
    plugin_panes_html = ""
    first_type = True
    for plugin_type in plugins:
        plugin_pane_html = ""
        plugin_tabs_html += html_part.tab_bar_item(plugin_type, first_type)
        for plugin in plugins[plugin_type]:
            temp_plugin = plugins[plugin_type][plugin]
            temp_config = config["plugins"][plugin_type][plugin]
            variable_name = "plugins_" + plugin_type + "_" + plugin + "_"
            if temp_plugin.SETTINGS.get("single_instance", True):
                plugin_pane_html += _single_plugin_config_page(plugin, temp_plugin, temp_config,
                                                               variable_name)
            else:
                plugin_pane_html += _multi_plugin_config_page(plugin, temp_plugin, temp_config,
                                                              variable_name)
        plugin_panes_html += html_part.tab_pane(plugin_type, plugin_pane_html, first_type)
        if first_type:
            first_type = False
    return html_part.plugin_config_page(html_part.tab_bar(plugin_tabs_html), plugin_panes_html)

def _single_plugin_config_page(plugin_name, plugin, config, variable_name):
    '''returns the single plugin pane'''
    section_enabled = plugin.CONFIG.check_if_section_is_enabled(config)
    control_html = ""
    if plugin.CONFIG.search_for_object_by_name("enabled"):
        control_html = html_part.checkbox_switch("enabled",
                                                 variable_name,
                                                 section_enabled, script=True)
    plugin_html = plugin.CONFIG.get_config_html(config, variable_name)
    return html_part.panel(plugin_name, plugin_name, control_html, "", variable_name[:-1],
                           plugin_html, section_enabled)

def _multi_plugin_config_page(plugin_name, plugin, config, variable_name):
    '''returns the multi plugin pane'''
    section_enabled = plugin.CONFIG.check_if_section_is_enabled(config)
    #add instance button
    control_html = html_part.add_instance_button(variable_name[:-1])
    modal = ""
    if 'list_of_options' in plugin.SETTINGS:
        options_html = ""
        for option in plugin.SETTINGS['list_of_options']:
            options_html += html_part.select_box_option(option, option)
        select_html = html_part.select_box(variable_name + "name", None, options_html)
        modal = html_part.list_modal(plugin_name, variable_name[:-1], select_html)
    else:
        modal = html_part.multi_modal(plugin_name, variable_name[:-1])
    modal = modal.replace("cs_", "")
    plugin_html = ""
    if config:
        for name in config:
            plugin_html = multi_plugin_config_section(plugin, config, variable_name[:-1], name)

    return html_part.panel(plugin_name, plugin_name, control_html, modal, variable_name[:-1],
                           plugin_html, section_enabled)

def multi_plugin_config_section(plugin, config, variable_name, name):
    '''returns a section of a multi plugin'''
    section_enabled = plugin.CONFIG.check_if_section_is_enabled(config)
    enable_option = ""
    if plugin.CONFIG.search_for_object_by_name("enabled"):
        enable_option = html_part.checkbox_switch("enabled",
                                                  variable_name,
                                                  section_enabled, script=True)
    delete_option = html_part.delete_instance_button(variable_name, name)
    section_html = plugin.CONFIG.get_config_html(config, variable_name + "_" + name + "_")
    return html_part.multi_panel(variable_name, name, enable_option, delete_option,
                                 section_html, section_enabled)

def get_config_multi_setup(plugins, plugin_path, full_config, name=""):
    '''Return the information needed for the setup of the plugin'''
    plugin_location = plugin_path.split("_")
    plugin = plugins[plugin_location[1]][plugin_location[2]]
    config = full_config[plugin_location[0]][plugin_location[1]][plugin_location[2]]
    return multi_plugin_config_section(plugin, config, plugin_path, name)
