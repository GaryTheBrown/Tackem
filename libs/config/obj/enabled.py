"""Config Object Boolean"""
from libs.config.obj.boolean import ConfigObjBoolean
from libs.config.obj.data.input_attributes import InputAttributes


class ConfigObjEnabled(ConfigObjBoolean):
    """Config Item Boolean"""

    def __init__(self, default_value=False, disabled=False):
        super().__init__(
            "enabled",
            default_value,
            "Enabled",
            "",
            input_attributes=InputAttributes(
                "disabled" if disabled else "enabled",
                data_on="Enabled",
                data_off="Disabled",
                data_onstyle="success",
                data_offstyle="secondary",
                data_width="124",
            ),
        )

    def add_panel_toggle(self):
        """Adds the toggle command"""
        self.input_attributes.add_if_missing(data_toggle_panel="true")
