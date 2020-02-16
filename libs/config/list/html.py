'''Config List Class'''
from libs.config.obj.data.input_attributes import InputAttributes
from libs.html_system import HTMLSystem
from libs.config.list.base import ConfigListBase

class ConfigListHtml(ConfigListBase):
    '''Config List Class'''

    def html(self, variable_name: str = "") -> str:
        '''Returns the html for the config option'''
        if variable_name == "":
            if self.var_name == "root":
                return self.__root_html()
        if self.var_name == "plugin":
            return ""
        if self.is_section:
            return self.__section(variable_name)
        return self.__section(variable_name)


    def __root_html(self) -> str:
        '''Returns the html for the config option'''
        page = HTMLSystem.part(
            "pages/configpage",
            NAV=HTMLSystem.part(
                "section/tabbar",
                TABBARITEMS=self.__root_tab_bar_items(),
            ),
            HTML=self.__root_tab_panes(),
        )

        if HTMLSystem.setting("post_save"):
            return HTMLSystem.part(
                "section/form",
                RETURNURL="admin/config",
                BUTTONLABEL="Save",
                PAGE=page,
            )
        return page


    def __root_tab_bar_items(self) -> str:
        '''Generates tab bar Item Html'''
        html = ""
        first = True
        for obj in self._objects:
            if not isinstance(obj, ConfigListBase):
                continue
            html += HTMLSystem.part(
                "section/tabbaritem",
                NAME=obj.var_name,
                ACTIVE="active" if first else "",
                LABEL=obj.label
            )
            first = False
        return html


    def __root_tab_panes(self) -> str:
        '''Generates the Tab Pane'''
        single_html = ""
        panels_html = ""
        first = True
        for obj in self._objects:
            if not isinstance(obj, ConfigListBase):
                single_html += obj.html()
                continue

            panels_html += HTMLSystem.part(
                "section/tabpane",
                NAME=obj.var_name,
                ACTIVE="active" if first else "",
                HTML=obj.html(obj.var_name),
            )
            first = False
        return single_html + panels_html


    def __single_panel(self, variable_name: str) -> str:
        '''Generates a Single Instance Setion/Panel'''
        return HTMLSystem.part(
            "section/panel",
            CONTROL=self.__controls(variable_name, False),
            MODAL="",#possibley none
            VARIABLENAME=variable_name,
            SECTION=self.__section_data(variable_name, True)
        )


    def __multi_panel(self, variable_name: str) -> str:
        '''Generates a Multi Instance Setion/Panel'''
        return HTMLSystem.part(
            "section/panel",
            CONTROL=self.__controls(variable_name, True),
            MODAL="", #TODO its own class in config to set it up. act like a list
            VARIABLENAME=variable_name,
            SECTION=self.__section_data(variable_name, True)
        )


    def __section_data(self, variable_name, hide_controls: bool = False):
        '''pulls all objects out for inclusion in the section'''
        html = ""
        for obj in self._objects:
            if hide_controls and (obj.var_name == "enabled" or obj.var_name == "disabled"):
                continue
            html += obj.html(variable_name)
        return html


    def __controls(self, variable_name: str, multi: bool) -> str:
        '''creates the control buttons'''
        html = ""
        for obj in self._objects:
            if obj.var_name == "enabled" or obj.var_name == "disabled":
                html += obj.item_html(variable_name)
                break
        if multi:
            variables = variable_name.split("_")
            input_attributes = InputAttributes(
                action="delete_multi_plugin",
                data_plugin_type=variables[1],
                data_plugin_name=variables[2],
                data_plugin_instance=self.var_name
                ).html()

            html += HTMLSystem.part(
                "input/button",
                BUTTONVALUE="Delete",
                DATA=input_attributes
            )

        return html


    def __section(self, variable_name: str) -> str:
        '''creates an Invisible to html section'''
        var = "{}_{}".format(variable_name, self.var_name) if variable_name != "" else self.var_name
        section_html = HTMLSystem.part(
            "section/section",
            SECTIONNAME=var,
            SECTION=self.__section_data(variable_name)
        )
        return section_html
