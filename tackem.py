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
            signal.signal(signal.SIGINT, ctrl_c)

    def _setup_plugins(self):
        '''Setup the Plugins'''
        plugin_cfg = ""
        print("Loading Plugins...")
        for folder in glob("plugins/*/"):
            if not "__pycache__" in folder:
                name = folder.split("/")[-2]
                print("Loading Plugin " + name + "...")
                temp_plugin = importlib.import_module("plugins." + name)
                plugin_platforms = temp_plugin.SETTINGS.get("platforms", ['Linux',
                                                                          'Darwin',
                                                                          'Windows'])
                if not platform.system() in plugin_platforms:
                    continue
                if hasattr(temp_plugin, "check_disabled") and temp_plugin.check_disabled():
                    continue
                if hasattr(temp_plugin, "check_enabled") and not temp_plugin.check_enabled():
                    continue

                Tackem.plugins[name] = temp_plugin

                if isinstance(Tackem.plugins[name].CONFIG, ConfigList):
                    plugin_cfg += Tackem.plugins[name].CONFIG.get_cfg(name)
                else:
                    plugin_cfg += Tackem.plugins[name].CFG
        return plugin_cfg

    def _setup_systems(self):
        '''setup the systems section'''
        for key in Tackem.plugins:
            if Tackem.plugins[key].SETTINGS['single_instance']:
                if Tackem.config['plugins'][key]['enabled']:
                    print("Loading " + key)
                    Tackem.systems[key] = Tackem.plugins[key].Plugin(key, key,
                                                                     Tackem.config['plugins'][key],
                                                                     Tackem.sql)
            else:
                for inst in Tackem.config['plugins'][key]:
                    partal = Tackem.config.get('plugins', {}).get(key, {})
                    if partal.get(inst, {}).get('enabled', True):
                        print("Loading " + inst + " (" + key + ")")
                        name = key + inst
                        config_inst = Tackem.config['plugins'][key][inst]
                        Tackem.systems[name] = Tackem.plugins[key].Plugin(key, name,
                                                                          config_inst, Tackem.sql)

    def start(self):
        '''Startup Of the systems'''
        if not Tackem.started:
            temp_keys = []
            for key in Tackem.systems:
                print("Starting " + key)
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

    def run(self):
        '''Looping function'''
        while True:
            self.setup()
            self.start()
            Tackem.root_event.wait()
            self.shutdown()

            if Tackem.root_event.check_shutdown():
                break
            elif Tackem.root_event.check_reboot():
                Tackem.root_event.clear_event()
                Tackem.setup_done = False
                Tackem.first_run = False
            else:
                print("!!!ERROR!!! HOW DID YOU GET HERE??? !!!ERROR!!! QUITTING NOW")
                break


##############################################
# Catching the ctrl + c event and doing a clean shutdown
def ctrl_c(_, __):
    '''Function to call once ctrl + c is pressed'''
    print(" caught Shutting Down Cleanly...")
    RootEvent().shutdown()
##############################################

if __name__ == "__main__":
    Tackem().run()
    signal.signal(signal.SIGINT, False)
