'''Admin Control Of System Data'''
import os
import glob
import importlib
import platform
from system.full import TackemSystemFull
from libs.config.list import ConfigList
from libs.plugin_base import load_plugin_settings
from libs.program_checker import check_for_required_programs
from libs.startup_arguments import PLUGINFOLDERLOCATION
from config_data import CONFIG

class TackemSystemAdmin(TackemSystemFull):
    '''Admin Control Of System Data'''

    def can_plugin_load(self, plugin_type: str, plugin_name: str) -> tuple:
        '''checks if the plugin can be loaded'''
        plugin_json_file = f"{PLUGINFOLDERLOCATION}{plugin_type}/{plugin_name}/settings.json"

        plugin_settings = load_plugin_settings(plugin_json_file)
        if platform.system() == 'Linux':
            return check_for_required_programs(
                plugin_settings.get('linux_programs', []),
                plugin_name
            )
        return "Platform Not Supported yet", 2

    def is_plugin_loaded(self, plugin_type: str, plugin_name: str) -> bool:
        '''checks if the plugin is loaded'''
        return plugin_name.lower() in self._base_data.plugins.get(plugin_type.lower(), {})

    # Plugin Methods
    def load_plugins(self) -> None:
        '''imports all plugin'''
        for folder in glob.glob(PLUGINFOLDERLOCATION + "*/*/"):
            if not "__pycache__" in folder:
                folder_split = folder.split("/")
                plugin_type = folder_split[-3]
                plugin_name = folder_split[-2]
                if plugin_name[0] == "_" or plugin_name[0] == "_":
                    continue
                if os.path.exists(folder + "__init__.py"):
                    self.load_plugin(plugin_type, plugin_name)

    def load_plugin(self, plugin_type: str, plugin_name: str) -> tuple:
        '''import a plugin'''
        if self.can_plugin_load(plugin_type, plugin_name)[0] is not True:
            return "Plugin Cannot Import", 0
        plugin = importlib.import_module(
            "plugins." + plugin_type + "." + plugin_name)
        plugin_platforms = plugin.SETTINGS.get(
            "platforms", ['Linux', 'Darwin', 'Windows'])
        if not platform.system() in plugin_platforms:
            return "Plugin Not Allowed On This OS", 1
        if hasattr(plugin, "check_disabled") and plugin.check_disabled():
            return "Is Marked as Disabled (Check Disabled)", 2
        if hasattr(plugin, "check_enabled") and not plugin.check_enabled():
            return "Is Marked as Disabled (Check Enabled)", 3

        if not plugin_type in self._base_data.plugins:
            self._base_data.plugins[plugin_type] = {}
        self._base_data.plugins[plugin_type][plugin_name] = plugin

        if not isinstance(CONFIG['plugins'][plugin_type], ConfigList):
            CONFIG['plugins'].append(ConfigList(
                plugin_type, plugin_type.capitalize()))
        if not plugin_name in CONFIG['plugins'][plugin_type].keys():
            CONFIG['plugins'][plugin_type].append(plugin.CONFIG)
        return True, 0

    def reload_plugins(self) -> None:
        '''reimports all plugins'''
        for plugin_type in self._base_data.plugins:
            for plugin_name in self._base_data.plugins[plugin_type]:
                self.reload_plugin(plugin_type, plugin_name)

    def reload_plugin(self, plugin_type: str, plugin_name: str) -> tuple:
        '''reimports the plugin'''
        plugin = self._base_data.plugins[plugin_type][plugin_name]
        try:
            importlib.reload(plugin)
        except ModuleNotFoundError:
            message = f"Reloading Module {plugin_type} {plugin_name} Failed"
            print(message)
            return message, 1

        CONFIG['plugins'][plugin_type].delete(plugin_name)
        CONFIG['plugins'][plugin_type].append(plugin.CONFIG)
        return True, 0

    def unload_plugins(self) -> None:
        '''deletes the plugins'''
        list_of_plugins = []
        for plugin_type in self._base_data.plugins:
            for plugin_name in self._base_data.plugins[plugin_type]:
                list_of_plugins.append((plugin_type, plugin_name))
        for plugin_type, plugin_name in list_of_plugins:
            self.unload_plugin(plugin_type, plugin_name)

    def unload_plugin(self, plugin_type: str, plugin_name: str) -> None:
        '''deletes a plugin'''
        del self._base_data.plugins[plugin_type][plugin_name]
        CONFIG['plugins'][plugin_type].delete(plugin_name)
        if not self._base_data.plugins[plugin_type]:
            del self._base_data.plugins[plugin_type]
            CONFIG['plugins'].delete(plugin_type)

    # Systems Methods
    def load_systems(self) -> None:
        '''load systems fors all plugins'''
        for plugin_type in self._base_data.plugins:
            for plugin_name in self._base_data.plugins[plugin_type]:
                self.load_plugin_systems(plugin_type, plugin_name)

    def load_system(self, system_name: str, single_instance: bool = True) -> bool:
        '''loads system'''
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
        self._base_data.systems[system_name] = temp_plugin.Plugin(
            system_name, single_instance)
        return True

    def unload_systems(self) -> None:
        '''deletes the systems'''
        for name in list(name for name in self._base_data.systems):
            self.unload_system(name)

    def unload_system(self, system_name: str) -> bool:
        '''deletes a system'''
        if not self._base_data.systems[system_name].running():
            del self._base_data.systems[system_name]
            return True
        return False

    def start_systems(self) -> bool:
        '''starts all of the systems'''
        return_check = True
        for name in self._base_data.systems:
            if not self.start_system(name):
                return_check = False
        return return_check

    def start_system(self, system_name: str) -> bool:
        '''starts a system'''
        if self._base_data.systems[system_name].running():
            return True
        started, message = self._base_data.systems[system_name].startup()
        if not started:
            print(f"{self._base_data.systems[system_name].name()} Failed to start: {message}")
            return False
        return True

    def stop_systems(self) -> None:
        '''stops all of the systems'''
        for name in self._base_data.systems:
            self._base_data.systems[name].shutdown()
        running = True
        while running:
            running = False
            for name in self._base_data.systems:
                if self._base_data.systems[name].running():
                    running = True

    def stop_system(self, system_name: str) -> None:
        '''stops a system'''
        self._base_data.systems[system_name].shutdown()
        while True:
            if not self._base_data.systems[system_name].running():
                return

    def load_plugin_systems(self, plugin_type: str, plugin_name: str) -> bool:
        '''loads a single plugin systems'''
        system_name = f"{plugin_type} {plugin_name}"
        system_config = CONFIG['plugins'][plugin_type][plugin_name]
        if self._base_data.plugins[plugin_type][plugin_name].SETTINGS.get('single_instance', True):
            if system_config['enabled'].value:
                if not self.load_system(system_name, True):
                    return False
            return True
        all_created = True
        for inst_obj in system_config:
            inst = inst_obj.var_name
            full_system_name = f"{system_name} {inst}"
            if system_config[inst]['enabled'].value:
                if not self.load_system(full_system_name, False):
                    all_created = False
        return all_created

    def unload_plugin_systems(self, plugin_type: str, plugin_name: str) -> None:
        '''deletes a plugin systems'''
        system_names = self.get_systems_for_plugin(plugin_type, plugin_name)
        for system_name in system_names:
            self.unload_system(system_name)

    def start_plugin_systems(self, plugin_type: str, plugin_name: str) -> None:
        '''start systems for a plugin'''
        system_names = self.get_systems_for_plugin(plugin_type, plugin_name)
        for system_name in system_names:
            self.start_system(system_name)

    def stop_plugin_systems(self, plugin_type: str, plugin_name: str) -> None:
        '''stop systems for a plugin'''
        system_names = self.get_systems_for_plugin(plugin_type, plugin_name)
        for system_name in system_names:
            self._base_data.systems[system_name].shutdown()
        temp_system_names = system_names.copy()
        while temp_system_names:
            for index, system_name in enumerate(temp_system_names):
                if not self._base_data.systems[system_name].running():
                    del temp_system_names[index]
                    break

    def get_systems_for_plugin(self, plugin_type: str, plugin_name: str) -> list:
        '''gets a list of systems for a plugin'''
        system_name = f"{plugin_type} {plugin_name}"
        return [key for key in self._base_data.systems if system_name in key]

    def do_systems_for_plugin_exist(self, plugin_type: str, plugin_name: str) -> bool:
        '''returns if one or more systems for this plugin exists'''
        system_name = f"{plugin_type} {plugin_name}"
        for key in self._base_data.systems:
            if system_name in key:
                return True
        return False

    def is_systems_for_plugin_running(self, plugin_type: str, plugin_name: str) -> bool:
        '''returns if one or more systems for this plugin are running'''
        system_name = f"{plugin_type} {plugin_name}"
        for key in self._base_data.systems:
            if system_name in key:
                if self._base_data.systems[key].running():
                    return True
        return False
