'''Admin Control Of System Data'''
import glob
import importlib
import platform
from system.base import TackemSystemBase
from libs.authenticator import Authentication
from libs.config import config_load
from libs.config_list import ConfigList
from libs.plugin_base import load_plugin_settings
from libs.program_checker import check_for_required_programs
from libs.musicbrainz import MusicBrainz
from libs.sql import setup_db
from libs.startup_arguments import ARGS, PLUGINFOLDERLOCATION

class TackemSystemAdmin(TackemSystemBase):
    '''Admin Control Of System Data'''

    def can_plugin_load(self, plugin_type, plugin_name):
        '''checks if the plugin can be loaded'''
        plugin_json_file = PLUGINFOLDERLOCATION + plugin_type + "/" + plugin_name + "/settings.json"
        plugin_settings = load_plugin_settings(plugin_json_file)
        if platform.system() == 'Linux':
            return check_for_required_programs(plugin_settings.get('linux_programs', []))
        return False

    def is_plugin_loaded(self, plugin_type, plugin_name):
        '''checks if the plugin is loaded'''
        return plugin_name in self._base_data.plugins.get(plugin_type, {})

    #Plugin Methods
    def load_plugins(self):
        '''loads all plugin'''
        for folder in glob.glob(PLUGINFOLDERLOCATION + "*/*/"):
            if not "__pycache__" in folder:
                folder_split = folder.split("/")
                plugin_name = folder_split[-2]
                plugin_type = folder_split[-3]
                self.load_plugin(plugin_type, plugin_name)

    def load_plugin(self, plugin_type, plugin_name):
        '''load a plugin'''
        if not self.can_plugin_load(plugin_type, plugin_name):
            return False
        with self._base_data.plugins_lock:
            plugin = importlib.import_module("plugins." + plugin_type + "." + plugin_name)
            plugin_platforms = plugin.SETTINGS.get("platforms", ['Linux', 'Darwin', 'Windows'])
            if not platform.system() in plugin_platforms:
                return False
            if hasattr(plugin, "check_disabled") and plugin.check_disabled():
                return False
            if hasattr(plugin, "check_enabled") and not plugin.check_enabled():
                return False

            if not plugin_type in self._base_data.plugins:
                self._base_data.plugins[plugin_type] = {}
            self._base_data.plugins[plugin_type][plugin_name] = plugin
        return True

    def delete_plugins(self):
        '''deletes the plugins'''
        list_of_plugins = []
        for plugin_type in self._base_data.plugins:
            for plugin_name in self._base_data.plugins[plugin_type]:
                list_of_plugins.append((plugin_type, plugin_name))
        for plugin_type, plugin_name in list_of_plugins:
            self.delete_plugin(plugin_type, plugin_name)
        return True

    def delete_plugin(self, plugin_type, plugin_name):
        '''deletes a plugin'''
        with self._base_data.plugins_lock:
            if self.is_systems_for_plugin_exists(plugin_type, plugin_name):
                self.stop_plugin(plugin_type, plugin_name)
            del self._base_data.plugins[plugin_type][plugin_name]
            if not self._base_data.plugins[plugin_type]:
                del self._base_data.plugins[plugin_type]
        return True

    def start_plugin(self, plugin_type, plugin_name):
        '''Starts a plugins systems'''
        self.load_plugin_systems(plugin_type, plugin_name)
        self.start_plugin_systems(plugin_type, plugin_name)

    def stop_plugin(self, plugin_type, plugin_name):
        '''Stops a plugins systems'''
        self.stop_plugin_systems(plugin_type, plugin_name)
        self.delete_plugin_systems(plugin_type, plugin_name)

    #Systems Methods
    def load_systems(self):
        '''load systems fors all plugins'''
        for plugin_type in self._base_data.plugins:
            for plugin_name in self._base_data.plugins[plugin_type]:
                self.load_plugin_systems(plugin_type, plugin_name)

    def load_system(self, system_name, single_instance=True):
        '''loads system'''
        with self._base_data.systems_lock:
            if system_name in self._base_data.systems:
                return False
            name_split = system_name.split(" ")
            if single_instance:
                plugin_name = name_split[-1]
                plugin_type = name_split[-2]
            else:
                plugin_name = name_split[-2]
                plugin_type = name_split[-3]
            temp_plugin = self._base_data.plugins[plugin_type][plugin_name]
            self._base_data.systems[system_name] = temp_plugin.Plugin(system_name, single_instance)
        return True

    def load_plugin_systems(self, plugin_type, plugin_name):
        '''loads a single plugin systems'''
        system_name = plugin_type + " " + plugin_name
        system_config = self._base_data.config['plugins'][plugin_type][plugin_name]
        if self._base_data.plugins[plugin_type][plugin_name].SETTINGS.get('single_instance', True):
            if system_config.get('enabled', True):
                if not self.load_system(system_name, True):
                    return False
            return True
        all_created = True
        for inst in system_config:
            full_system_name = system_name + " " + inst
            if system_config.get(inst, {}).get('enabled', True):
                if not self.load_system(full_system_name, False):
                    all_created = False
        return all_created

    def delete_systems(self):
        '''deletes the systems'''
        for name in list(name for name in self._base_data.systems):
            self.delete_system(name)
        return True

    def delete_system(self, system_name):
        '''deletes a system'''
        with self._base_data.systems_lock:
            if not self._base_data.systems[system_name].running():
                del self._base_data.systems[system_name]
                return True
        return False

    def delete_plugin_systems(self, plugin_type, plugin_name):
        '''deletes a plugin systems'''
        system_names = self.get_systems_for_plugin(plugin_type, plugin_name)
        for system_name in system_names:
            self.delete_system(system_name)

    def start_systems(self):
        '''starts all of the systems'''
        return_check = True
        for name in self._base_data.systems:
            if not self.start_system(name):
                return_check = False
        return return_check

    def start_system(self, system_name):
        '''starts a system'''
        with self._base_data.systems_lock:
            if self._base_data.systems[system_name].running():
                return True
            started, message = self._base_data.systems[system_name].startup()
            if not started:
                print(self._base_data.systems[system_name].name() + " Failed to start: " + message)
                return False
            return True

    def start_plugin_systems(self, plugin_type, plugin_name):
        '''start systems for a plugin'''
        system_names = self.get_systems_for_plugin(plugin_type, plugin_name)
        for system_name in system_names:
            self.start_system(system_name)

    def stop_systems(self):
        '''stops all of the systems'''
        with self._base_data.systems_lock:
            for name in self._base_data.systems:
                self._base_data.systems[name].shutdown()
            running = True
            while running:
                running = False
                for name in self._base_data.systems:
                    if self._base_data.systems[name].running():
                        running = True
            return True

    def stop_system(self, system_name):
        '''stops a system'''
        with self._base_data.systems_lock:
            self._base_data.systems[system_name].shutdown()
            while True:
                if not self._base_data.systems[system_name].running():
                    return True

    def stop_plugin_systems(self, plugin_type, plugin_name):
        '''stop systems for a plugin'''
        with self._base_data.systems_lock:
            system_names = self.get_systems_for_plugin(plugin_type, plugin_name)
            for system_name in system_names:
                self._base_data.systems[system_name].shutdown()
            temp_system_names = system_names.copy()
            while temp_system_names:
                for index, system_name in enumerate(temp_system_names):
                    if not self._base_data.systems[system_name].running():
                        del temp_system_names[index]

    def get_systems_for_plugin(self, plugin_type, plugin_name):
        '''gets a list of systems for a plugin'''
        with self._base_data.systems_lock:
            system_name = plugin_type + " " + plugin_name
            return list(key for key, _ in self._base_data.systems if system_name in key)

    def is_systems_for_plugin_exists(self, plugin_type, plugin_name):
        '''gets a list of systems for a plugin'''
        with self._base_data.systems_lock:
            system_name = plugin_type + " " + plugin_name
            for key in self._base_data.systems:
                if system_name in key:
                    return True
            return False

    def is_systems_for_plugin_running(self, plugin_type, plugin_name):
        '''gets a list of systems for a plugin'''
        with self._base_data.systems_lock:
            system_name = plugin_type + " " + plugin_name
            for key in self._base_data.systems:
                if system_name in key:
                    if self._base_data.systems[key].running():
                        return True
            return False

    #Plugin Cfg Methods
    def load_plugin_cfgs(self):
        '''load all plugin cfgs'''
        for plugin_type in self._base_data.plugins:
            for plugin_name in self._base_data.plugins[plugin_type]:
                self.load_plugin_cfg(plugin_type, plugin_name)
        return True

    def load_plugin_cfg(self, plugin_type, plugin_name):
        '''load a plugins cfg'''
        with self._base_data.plugin_cfg_lock:
            if not plugin_type in self._base_data.plugin_cfg:
                self._base_data.plugin_cfg[plugin_type] = {}
            with self._base_data.plugins_lock:
                temp_plugin = self._base_data.plugins[plugin_type][plugin_name]
                plugin_cfg = self._base_data.plugin_cfg[plugin_type]
                if isinstance(temp_plugin.CONFIG, ConfigList):
                    single_instance = temp_plugin.SETTINGS.get("single_instance", False)
                    plugin_cfg[plugin_name] = temp_plugin.CONFIG.get_plugin_spec(single_instance)
                else:
                    plugin_cfg[plugin_name] = temp_plugin.CFG
        return True

    def delete_plugin_cfgs(self):
        '''deletes the plugins cfg'''
        with self._base_data.plugin_cfg_lock:
            self._base_data.plugin_cfg = {}
        return True

    def delete_plugin_cfg(self, plugin_type, plugin_name):
        '''removes a plugins cfg'''
        with self._base_data.plugin_cfg_lock:
            if plugin_name not in self._base_data.plugin_cfg[plugin_type]:
                return False
            del self._base_data.plugin_cfg[plugin_type][plugin_name]
            if not self._base_data.plugin_cfg[plugin_type]:
                del self._base_data.plugin_cfg[plugin_type]
        return True

    def get_plugin_cfg(self):
        '''retrieves the plugins cfg'''
        with self._base_data.plugin_cfg_lock:
            cfg = ""
            for plugin_type in self._base_data.plugin_cfg:
                cfg += "[[" + plugin_type + "]]\n"
                for plugin_name in self._base_data.plugin_cfg[plugin_type]:
                    cfg += self._base_data.plugin_cfg[plugin_type][plugin_name]
            return cfg

    #Config Methods
    def load_config(self):
        '''load the config'''
        with self._base_data.config_lock:
            if self._base_data.config is None:
                self._base_data.config = config_load(ARGS.home, self.get_plugin_cfg())

    def delete_config(self):
        '''deletes the config'''
        with self._base_data.config_lock:
            if self._base_data.config is not None:
                self._base_data.config = None

    def write_config_to_disk(self, outfile=None):
        '''writes config to file'''
        with self._base_data.config_lock:
            try:
                self._base_data.config.write(outfile=outfile)
            except OSError:
                print("ERROR WRITING CONFIG FILE")

    def get_plugin_config(self, plugin_type, plugin_name, instance=None):
        '''returns the config for a plugin'''
        with self._base_data.config_lock:
            if instance:
                return self._base_data.config[plugin_type][plugin_name][instance]
            return self._base_data.config[plugin_type][plugin_name]

    def get_global_config(self):
        '''returns the global config'''
        with self._base_data.config_lock:
            return self._base_data.config

    #SQL Methods
    def load_sql(self):
        '''load SQL'''
        self._base_data.sql = setup_db(self._base_data.config['database'])

    def delete_sql(self):
        '''deletes the SQL system'''
        self._base_data.sql = None

    def start_sql(self):
        '''starts the SQL System'''
        self._base_data.sql.start_thread()

    def stop_sql(self):
        '''stops the SQL System'''
        if self._base_data.sql is not None:
            self._base_data.sql.stop_thread()

    #MusicBrainz Methods
    def load_musicbrainz(self):
        '''load musicbrainz'''
        if self._base_data.config.get("musicbrainz", {}).get('enabled', True):
            self._base_data.musicbrainz = MusicBrainz()

    def delete_musicbrainz(self):
        '''deletes the musicbrainz'''
        if self._base_data.musicbrainz is not None:
            self._base_data.musicbrainz = None

    #Authentication Methods
    def load_auth(self):
        '''loads the auth'''
        if self._base_data.config.get("authentication", {}).get('enabled', True):
            self._base_data.auth = Authentication()

    def delete_auth(self):
        '''deletes the auth'''
        if self._base_data.auth is not None:
            self._base_data.auth = None

    def start_auth(self):
        '''starts the auth'''
        if self._base_data.auth is not None:
            self._base_data.auth.start()
