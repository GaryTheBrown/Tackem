'''Config List Class'''
from libs.config.obj.enabled import ConfigObjEnabled
from libs.config.obj.data.input_attributes import InputAttributes
from libs.html_system import HTMLSystem
from libs.config.list.base import ConfigListBase

class ConfigListHtml(ConfigListBase):
    '''Config List Class'''

    def html(self, variable_name: str = "", first_block = False) -> str:
        '''Returns the html for the config option'''
        if variable_name == "" and self.var_name == "root":
            return self.__root_html()
        if self.is_section:
            return self.__section(variable_name)
        if first_block:
            return self.__first_block(variable_name)
        return self.__block(variable_name)

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
                single_html += obj.html(first_block=True)
                continue

            panels_html += HTMLSystem.part(
                "section/tabpane" if obj.var_name == "plugins" else "section/tabpanewithmargin",
                NAME=obj.var_name,
                ACTIVE="active" if first else "",
                HTML=obj.html(obj.var_name, True),
            )
            first = False
        return single_html + panels_html

    def panel(self, variable_name: str, title: str = "") -> str:
        '''Generates a Single/Multi Instance Setion/Panel'''
        variable_name += f"_{title.lower()}"
        return HTMLSystem.part(
            "section/panel",
            TITLE=title,
            CONTROL=self.__controls(variable_name) if self.many_section else "",
            VARIABLENAME=variable_name,
            PANELNAME=f"{variable_name}_panel",
            SECTION=self.__section_data(variable_name),
            MODAL=self.__modal(variable_name)
        )

    def __modal(self, variable_name: str) -> str:
        '''grnerates the modal if needed'''
        return HTMLSystem.part(
            "section/modal",
            VARIABLENAME=variable_name,
            TITLE=f"Add New {self.label}",
            BODY=self.__modal_body(variable_name),
        )

    def __modal_body(self, variable_name: str) -> str:
        '''generates the modal body and returns it'''
        input_html = ""
        if self.many_section_limit_list:
            options_html = HTMLSystem.part(
                "inputs/single/option",
                LABEL="Please Select An Option",
                input_attributes=InputAttributes("required", "selected", "disabled").html()
            )
            for item in self.many_section_limit_list:
                attr = InputAttributes("disabled", "required").html(
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

        input_html += HTMLSystem.part(
            "inputs/button",
            LABEL="Add Instance",
            DATA=InputAttributes(
                data_click_action="addMulti",
                data_target=variable_name
            ).html()
        )

        return HTMLSystem.part(
            "section/modalbody",
            LABEL="Please Enter a Name for the Instance",
            INPUT=input_html
        )

    def __section_data(self, variable_name: str, skip_enabled=False) -> str:
        '''pulls all objects out for inclusion in the section'''
        html = ""
        for obj in self._objects:
            if skip_enabled and isinstance(obj, ConfigObjEnabled):
                continue
            html += obj.html(variable_name)

        #TODO MANY SECTION MISSING FROM HERE

        return html

    def __controls(self, variable_name: str) -> str:
        '''creates the control buttons'''

        variables = variable_name.split("_")
        input_attributes = InputAttributes(
            data_click_action="deleteMulti",
            data_plugin_type=variables[1],
            data_plugin_name=variables[2],
            data_plugin_instance=self.var_name
        ).html()

        return HTMLSystem.part(
            "inputs/button",
            LABEL="Delete",
            DATA=input_attributes
        )

    def __section(self, variable_name: str) -> str:
        '''creates an Invisible to html section'''

        var = f"{variable_name}_{self.var_name}" if variable_name != "" else self.var_name
        section_html = HTMLSystem.part(
            "section/section",
            SECTIONNAME=var,
            SECTION=self.__section_data(variable_name)
        )
        return section_html

    def __block(self, variable_name: str) -> str:
        '''creates an Invisible to html section'''
        variable_name += f"_{self.var_name}"
        control = ""
        if "enabled" in self.keys():
            self["enabled"].add_panel_toggle()
            control += self["enabled"].item_html(f"{variable_name}_enabled")

        label = self.label
        if new_label := self.get("label"):
            if new_label.value != "":
                label = new_label.value
        return HTMLSystem.part(
            "section/panel",
            TITLE=label,
            CONTROL=control,
            VARIABLENAME=variable_name,
            PANELNAME=f"{variable_name}_panel",
            SECTION=self.__section_data(variable_name, skip_enabled=True),
        )

    def __first_block(self, variable_name: str) -> str:
        '''creates an Invisible to html section'''
        if self.var_name != variable_name:
            variable_name += f"_{self.var_name}"

        if "enabled" in self.keys():
            self["enabled"].add_panel_toggle()
            return HTMLSystem.part(
                "section/firstblockpanel",
                ENABLED=self["enabled"].html(variable_name),
                VARIABLENAME=variable_name,
                PANELNAME=f"{variable_name}_panel",
                SECTION=self.__section_data(variable_name, skip_enabled=True),
            )
        else:
            return self.__section_data(variable_name)
