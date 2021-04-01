"""Config List Class"""
from libs.config.list.base import ConfigListBase

# from libs.config.obj.data.input_attributes import InputAttributes
# from libs.config.obj.enabled import ConfigObjEnabled


class ConfigListHtml(ConfigListBase):
    """Config List Class"""

    def html_dict(self, variable_name: str = "") -> dict:
        """returns the required Data for the html template to use"""
        var = ""
        if self.var_name != "root":
            var = f"{variable_name}_{self.var_name}" if variable_name != "" else self.var_name

        return_dict = {
            "type": "list",
            "var_name": var,
            "label": self.label,
            "objects": [obj.html_dict(var) for obj in self._objects if not obj.hide_on_html],
            "is_section": self.is_section,
        }

        for obj in self._objects:
            if obj.var_name == "enabled":
                return_dict["enabled_obj"] = obj.html_dict(f"{var}")
        return_dict.update(ConfigListBase.html_dict(self, variable_name))
        for obj in self._objects:
            if obj.var_name == "label":
                return_dict["label"] = obj.value
                break

        return return_dict

    # def panel(self, variable_name: str, title: str = "") -> str:
    #     """Generates a Single/Multi Instance Setion/Panel"""
    #     variable_name += f"_{title.lower()}"
    #     return HTMLSystem.part(
    #         "section/panel",
    #         TITLE=title,
    #         CONTROL=self.__controls(variable_name) if self.many_section else "",
    #         VARIABLENAME=variable_name,
    #         PANELNAME=f"{variable_name}_panel",
    #         SECTION=self.__section_data(variable_name),
    #         MODAL=self.__modal(variable_name),
    #     )

    # def __modal(self, variable_name: str) -> str:
    #     """grnerates the modal if needed"""
    #     return HTMLSystem.part(
    #         "section/modal",
    #         VARIABLENAME=variable_name,
    #         TITLE=f"Add New {self.label}",
    #         BODY=self.__modal_body(variable_name),
    #     )

    # def __modal_body(self, variable_name: str) -> str:
    #     """generates the modal body and returns it"""
    #     input_html = ""
    #     if self.many_section_limit_list:
    #         options_html = HTMLSystem.part(
    #             "inputs/single/option",
    #             LABEL="Please Select An Option",
    #             input_attributes=InputAttributes("required", "selected", "disabled").html(),
    #         )
    #         for item in self.many_section_limit_list:
    #           attr = InputAttributes("disabled", "required").html() if item in self.keys() else ""
    #             options_html += HTMLSystem.part(
    #                 "inputs/single/option",
    #                 VALUE=item,
    #                 LABEL=item,
    #                 input_attributes=attr,
    #             )
    #         input_html = HTMLSystem.part(
    #             "inputs/select",
    #             OPTIONS=options_html,
    #             OTHER=InputAttributes("disabled").html(),
    #         )
    #     else:
    #         input_html = HTMLSystem.part(
    #             "inputs/input",
    #             INPUTTYPE="text",
    #             OTHER=InputAttributes(
    #                 "disabled", placeholder="Please Enter a name for your Instance"
    #             ).html(),
    #         )

    #     input_html += HTMLSystem.part(
    #         "inputs/button",
    #         LABEL="Add Instance",
    #         DATA=InputAttributes(data_click_action="addMulti", data_target=variable_name).html(),
    #     )

    #     return HTMLSystem.part(
    #         "section/modalbody",
    #         LABEL="Please Enter a Name for the Instance",
    #         INPUT=input_html,
    #     )
