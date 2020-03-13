'''Config List Class'''
from libs.config.obj.data.input_attributes import InputAttributes
from libs.html_system import HTMLSystem
from libs.config.list.base import ConfigListBase


class ConfigListHtml(ConfigListBase):
    '''Config List Class'''

    def html(self, variable_name: str = "") -> str:
        '''Returns the html for the config option'''
        if variable_name == "" and self.var_name == "root":
            return self.__root_html()
        if self.var_name == "plugins":
            return self.plugins_html()
        if self.is_section:
            return self.__section(variable_name)
        return self.__section(variable_name)

    def __root_html(self) -> str:
        '''Returns the html for the config option'''
        page = HTMLSystem.part(
            "pages/configpage",
            HTML=HTMLSystem.part(
                "section/tabsection",
                NAV=HTMLSystem.part(
                    "section/tabbar",
                    TABBARITEMS=self.__root_tab_bar_items(),
                ),
                HTML=self.__root_tab_panes(),
            )
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
                "section/tabpane" if obj.var_name == "plugins" else "section/tabpanewithmargin",
                NAME=obj.var_name,
                ACTIVE="active" if first else "",
                HTML=obj.html(obj.var_name),
            )
            first = False
        return single_html + panels_html

    def plugins_html(self, variable_name: str = "") -> str:
        '''Recursive way to do plugin sections'''
        if variable_name == "" and self.var_name == "plugins":
            return self.__plugins_root_html()
        if self.many_section:
            return self.__plugin_multi_html(variable_name)
        return self.__section(variable_name)

    def __plugins_root_html(self) -> str:
        '''generates the whole plugin section code'''
        tabnavs = ""
        panels = ""
        first = True
        for obj in self._objects:
            if not isinstance(obj, ConfigListBase):
                raise ValueError(
                    "an unexpected item was found in plugin types")
            for sub_obj in self[obj.var_name]:
                if not isinstance(sub_obj, ConfigListBase):
                    raise ValueError(
                        "unexpected item was found in plugin names")
                name = "plugins_{}_{}".format(obj.var_name, sub_obj.var_name)
                tabnavs += HTMLSystem.part(
                    "section/tabbaritem",
                    NAME=name,
                    ACTIVE="active" if first else "",
                    LABEL="{} - {}".format(obj.label, sub_obj.label)
                )

                panels += HTMLSystem.part(
                    "section/tabpane" if sub_obj.many_section else "section/tabpanewithmargin",
                    NAME=name,
                    ACTIVE="active" if first else "",
                    HTML=sub_obj.plugins_html(name),
                )

            first = False

        return HTMLSystem.part(
            "section/tabsection",
            NAV=HTMLSystem.part(
                "section/tabbar",
                TABBARITEMS=tabnavs
            ),
            HTML=panels
        )

    def __plugin_multi_html(self, variable_name: str) -> str:
        '''deals with the multi instance plugins panel'''
        html = ""
        for obj in self._objects:
            if not isinstance(obj, ConfigListBase):
                raise ValueError("Object found where config lists should be")
            html += obj.panel(variable_name)

        html += self.__modal(variable_name)  # <- FIX MODAL NOT WORKING
        html += HTMLSystem.part(
            "inputs/button",
            LABEL="Add Instance",
            DATA=InputAttributes(
                data_toggle="modal",
                data_target="#{}_modal".format(variable_name)
            ).html()
        )

        return html

    def panel(self, variable_name: str) -> str:
        '''Generates a Single/Multi Instance Setion/Panel'''
        return HTMLSystem.part(
            "section/panel",
            CONTROL=self.__controls(
                variable_name) if self.many_section else "",
            VARIABLENAME=variable_name,
            SECTION=self.__section_data(variable_name),
            MODAL=self.__modal(variable_name)
        )

    def __modal(self, variable_name) -> str:
        '''grnerates the modal if needed'''
        return HTMLSystem.part(
            "section/modal",
            VARIABLENAME=variable_name,
            TITLE="Add New {}".format(self.label),
            BODY=self.__modal_body(),
            FOOTER=HTMLSystem.part(
                "inputs/button",
                LABEL="Add Instance",
                DATA=InputAttributes(
                    data_action="addMulti",
                    data_target=variable_name
                ).html()
            )
        )

    def __modal_body(self) -> str:
        '''generates the modal body and returns it'''
        input_html = ""
        if self.many_section_limit_list:
            options_html = HTMLSystem.part(
                "inputs/single/option",
                LABEL="Please Select An Option",
                input_attributes=InputAttributes("selected", "disabled").html()
            )
            for item in self.many_section_limit_list:
                attr = InputAttributes("disabled").html(
                ) if item in self.keys() else ""
                options_html += HTMLSystem.part(
                    "inputs/single/option",
                    VALUE=item,
                    LABEL=item,
                    input_attributes=attr
                )
            input_html = HTMLSystem.part(
                "inputs/select",
                OPTIONS=options_html,
                OTHER=InputAttributes("disabled").html()
            )
        else:
            input_html = HTMLSystem.part(
                "inputs/input",
                INPUTTYPE="text",
                OTHER=InputAttributes(
                    "disabled",
                    placeholder="Please Enter a name for your Instance"
                ).html()
            )

        return HTMLSystem.part(
            "section/modalbody",
            LABEL="Please Enter a Name for the Instance",
            INPUT=input_html
        )

    def __section_data(self, variable_name) -> str:
        '''pulls all objects out for inclusion in the section'''
        html = ""
        for obj in self._objects:
            html += obj.html(variable_name)
        return html

    def __controls(self, variable_name: str) -> str:
        '''creates the control buttons'''
        variables = variable_name.split("_")
        input_attributes = InputAttributes(
            action="delete_multi_plugin",
            data_plugin_type=variables[1],
            data_plugin_name=variables[2],
            data_plugin_instance=self.var_name
        ).html()

        return HTMLSystem.part(
            "input/button",
            BUTTONVALUE="Delete",
            DATA=input_attributes
        )

    def __section(self, variable_name: str) -> str:
        '''creates an Invisible to html section'''
        var = "{}_{}".format(
            variable_name, self.var_name) if variable_name != "" else self.var_name
        section_html = HTMLSystem.part(
            "section/section",
            SECTIONNAME=var,
            SECTION=self.__section_data(variable_name)
        )
        return section_html
