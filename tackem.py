'''Start Point Of Program'''
#https://docs.cherrypy.org/en/latest/tutorials.html
import os
import os.path
import importlib
import platform
import signal
from glob import glob
from libs.startup_arguments import ARGS
from libs.config import config_load
from libs.config_list import ConfigList
from libs.sql import setup_db
from libs.root_event import RootEventMaster as RootEvent
from libs.httpd import Httpd

class Tackem:
    '''main program entrance'''
    setup_done = False
    started = False
    first_run = False # change this to true if you need to access the first run script for editing
    plugins = {}
    sql = None
    systems = {}
    cherrypy = None
    config = None
    webserver = None
    root_event = RootEvent()

    def __init__(self):
        pass

    def setup(self):
        '''Setup of the program'''
        if not Tackem.setup_done:
            #First check if home folder exists (useable to run first time script)
            if not os.path.exists(ARGS.home):
                Tackem.first_run = True
                os.mkdir(ARGS.home)

            #Load Plugin Data
            plugin_cfg = self._setup_plugins()

            #Load Config File
            if not os.path.exists(ARGS.home + "config.ini"):
                Tackem.first_run = True
            Tackem.config = config_load(ARGS.home + "config.ini", plugin_cfg)

            if not Tackem.first_run:
                #DB Load
                Tackem.sql = setup_db(Tackem.config['database'])
                print("Loading Systems...")
                self._setup_systems()

            Tackem.setup_done = True
            #Setup signal to watch for ctrl + c command
            signal.signal(signal.SIGINT, ctrl_c)

    def _setup_plugins(self):
        '''Setup the Plugins'''
        cfg = ""
        Tackem.plugins = {}
        print("Loading Plugins...")
        for folder in glob("plugins/*/*/"):
            if not "__pycache__" in folder:
                folder_split = folder.split("/")
                name = folder_split[-2]
                print_name = name.replace("_", " ").capitalize()
                plugin_type = folder_split[-3]
                print("Loading " + plugin_type.capitalize() + ":" + print_name.capitalize() + "...")
                plugin = importlib.import_module("plugins." + plugin_type + "." + name)
                plugin_platforms = plugin.SETTINGS.get("platforms", ['Linux',
                                                                     'Darwin',
                                                                     'Windows'])
                if not platform.system() in plugin_platforms:
                    continue
                if hasattr(plugin, "check_disabled") and plugin.check_disabled():
                    continue
                if hasattr(plugin, "check_enabled") and not plugin.check_enabled():
                    continue

                if not plugin_type in Tackem.plugins:
                    Tackem.plugins[plugin_type] = {}
                Tackem.plugins[plugin_type][name] = plugin
        for plugin_type in Tackem.plugins:
            cfg += "    [[" + plugin_type + "]]\n"
            for plugin in Tackem.plugins[plugin_type]:
                temp_plugin = Tackem.plugins[plugin_type][plugin]
                if isinstance(temp_plugin.CONFIG, ConfigList):
                    single_instance = temp_plugin.SETTINGS.get("single_instance", False)
                    cfg += temp_plugin.CONFIG.get_plugin_spec(single_instance)
                else:
                    cfg += temp_plugin.CFG
        return cfg

    def _setup_systems(self):
        '''setup the systems section'''
        for plugin_type in Tackem.plugins:
            for plugin_name in Tackem.plugins[plugin_type]:
                temp_plugin = Tackem.plugins[plugin_type][plugin_name]
                temp_config = Tackem.config['plugins'][plugin_type][plugin_name]
                plugin_full_name = plugin_type + " " + plugin_name
                if temp_plugin.SETTINGS['single_instance']:
                    if temp_config.get('enabled', True):
                        print("Loading " + plugin_full_name)
                        Tackem.systems[plugin_full_name] = temp_plugin.Plugin(temp_plugin,
                                                                              plugin_full_name,
                                                                              temp_config,
                                                                              Tackem.sql)
                else:
                    for inst in temp_config:
                        full_name = plugin_full_name + " " + inst
                        if temp_config.get(inst, {}).get('enabled', True):
                            print("Loading " + full_name)
                            Tackem.systems[full_name] = temp_plugin.Plugin(temp_plugin,
                                                                           full_name,
                                                                           temp_config[inst],
                                                                           Tackem.sql)

    def start(self):
        '''Startup Of the systems'''
        if not Tackem.started:
            temp_keys = []
            for key in Tackem.systems:
                clean_key = key.replace("_", " ")
                print("Starting " + clean_key)
                started, message = Tackem.systems[key].startup()
                if not started:
                    print(Tackem.systems[key].name() + " Failed to start because " + message)
                    temp_keys.append(key)

            for key in temp_keys:
                del Tackem.systems[key]
            del temp_keys

            if Tackem.config['api']['enabled'] or Tackem.config['webui']['enabled']:
                print("Starting WebUI and/or API")
                Tackem.webserver = Httpd(Tackem.config, Tackem.systems,
                                         Tackem.plugins, Tackem.first_run)
                Tackem.webserver.start()

            Tackem.started = True


    def shutdown(self):
        '''Shutdown commands'''
        if Tackem.started:
            print("SHUTDOWN STARTED")
            #stop the WebUI AND/OR API
            if Tackem.webserver is not None:
                print("Stopping Web Services")
                Tackem.webserver.stop()

            #Stop All Plugins
            print("Stopping Plugins")
            for key in Tackem.systems:
                Tackem.systems[key].shutdown()

            while Tackem.systems:
                for key in Tackem.systems:
                    if not Tackem.systems[key].running():
                        print(key + " Stopped")
                        del Tackem.systems[key]
                        break
            print("All systems Shutdown")

            if Tackem.sql is not None:
                Tackem.sql.stop_thread()

            if not Tackem.first_run:
                try:
                    Tackem.config.write()
                except OSError:
                    print("ERROR WRITING CONFIG FILE")
            Tackem.started = False

    def system_start(self, system_name):
        '''Start up an invidual plugin system'''
        print("Starting " + system_name)
        started, message = Tackem.systems[system_name].startup()
        if not started:
            print(Tackem.systems[system_name].name() + " Failed to start because " + message)
            del Tackem.systems[system_name]

    def system_stop(self, system_name):
        '''Stop up an invidual plugin system'''
        Tackem.systems[system_name].shutdown()
        while True:
            if not Tackem.systems[system_name].running():
                print(system_name + " Stopped")
                del Tackem.systems[system_name]
                break

    def run(self):
        '''Looping function'''
        self.setup()
        self.start()
        while True:
            event_type, event_variable = Tackem.root_event.wait_and_get_event()

            if event_type is False:
                continue
            elif event_type == "shutdown":
                self.shutdown()
                break
            elif event_type == "reboot":
                self.shutdown()
                Tackem.setup_done = False
                Tackem.first_run = False
                self.setup()
                self.start()
            elif event_type == "start system":
                if event_variable is False:
                    continue
                self.system_start(event_variable)
            elif event_type == "stop system":
                if event_variable is False:
                    continue
                self.system_stop(event_variable)
            elif event_type == "restart system":
                if event_variable is False:
                    continue
                self.system_stop(event_variable)
                self.system_start(event_variable)
            else:
                print("Event Not Recognised Ignoring")
                continue

##############################################
# Catching the ctrl + c event and doing a clean shutdown
def ctrl_c(_, __):
    '''Function to call once ctrl + c is pressed'''
    print(" caught Shutting Down Cleanly...")
    RootEvent().set_event("shutdown")
##############################################

if __name__ == "__main__":
    Tackem().run()
    signal.signal(signal.SIGINT, False)
