'''Functions to deal with all the html template parts'''
from typing import Union
from libs.startup_arguments import PROGRAMVERSION
from libs.html_system import HTMLSystem

#################
#MASTER TEMPLATE#
#################


def master_template(
        title: str,
        body: str,
        javascript_extra: str,
        stylesheet_extra: str,
        baseurl: str,
        navbar: str
    ) -> str:
    '''head section of the template'''
    return HTMLSystem.part(
        "template",
        JAVASCRIPTEXTRA=javascript_extra,
        STYLESHEETEXTRA=stylesheet_extra,
        NAVBAR=navbar,
        BODY=body,
        BASEURL=baseurl,
        PROGRAMVERSION=PROGRAMVERSION,
        TITLE=title
    )


########
#NAVBAR#
########


def navbar_dropdown(title: str, dropdown_id: str, items: str) -> str:
    '''A Navbar Item (not active)'''
    return HTMLSystem.part(
        "navbar/dropdown",
        TITLE=title.title(),
        DROPDOWNID=dropdown_id,
        ITEMS=items
    )


def navbar_dropdown_left(title: str, dropdown_id: str, items: str) -> str:
    '''A Navbar Item left aligned (not active)'''
    return HTMLSystem.part(
        "navbar/dropdownleft",
        TITLE=title.title(),
        DROPDOWNID=dropdown_id,
        ITEMS=items
    )


def navbar_dropdown_right(title: str, dropdown_id: str, items: str) -> str:
    '''A Navbar Item right aligned (not active)'''
    return HTMLSystem.part(
        "navbar/dropdownright",
        TITLE=title.title(),
        DROPDOWNID=dropdown_id,
        ITEMS=items
    )


def navbar_drop_left(title: str, dropdown_id: str, items: str) -> str:
    '''A Navbar Item (not active)'''
    return HTMLSystem.part(
        "navbar/dropleft",
        TITLE=title.title(),
        DROPDOWNID=dropdown_id,
        ITEMS=items
    )


def navbar_drop_right(title: str, dropdown_id: str, items: str) -> str:
    '''A Navbar Item (not active)'''
    return HTMLSystem.part(
        "navbar/dropright",
        TITLE=title.title(),
        DROPDOWNID=dropdown_id,
        ITEMS=items
    )


def navbar_item(title: str, url: str) -> str:
    '''A Navbar Item (not active)'''
    return HTMLSystem.part(
        "navbar/item",
        TITLE=title.title(),
        URL=url.replace(" ", "/")
    )


def navbar_item_active(title: str) -> str:
    '''A Navbar Item (not active)'''
    return HTMLSystem.part(
        "navbar/itemactive",
        TITLE=title.title()
    )


def navbar_master(navbar_items: str, navbar_right_items: str) -> str:
    '''master file for the navbar'''
    return HTMLSystem.part(
        "navbar/master",
        NAVBARRIGHT=navbar_right_items,
        NAVBARITEMS=navbar_items
    )


#######
#PAGES#
#######


def plugin_config_page(tab_bar_tabs: str, sections: str) -> str:
    '''Plugin config page'''
    return HTMLSystem.part(
        "pages/pluginconfigpage",
        PANELTABS=tab_bar_tabs,
        PLUGINLIST=sections
    )


def root_config_page(sections: str) -> str:
    '''Root config page'''
    return HTMLSystem.part(
        "pages/rootconfigpage",
        PLUGINLIST=sections
    )


def login_page(return_url: str) -> str:
    '''Root config page'''
    return HTMLSystem.part(
        "pages/login",
        RETURNURL=return_url
    )


def password_page() -> str:
    '''Root config page'''
    return HTMLSystem.part("pages/password")


##########
#SECTIONS#
##########


def accordian(accordian_name: str, accordian_cards: str) -> str:
    '''outside of the accordian'''
    return HTMLSystem.part(
        "sections/accordian",
        ACCORDIANNAME=accordian_name,
        ACCORDIANCARDS=accordian_cards
    )


def accordian_card(
        accordian_name: str,
        number: int,
        header: str,
        button: str,
        body: str,
        show: bool = False
    ) -> str:
    '''section for the accordian'''
    return HTMLSystem.part(
        "sections/accordiancard",
        ACCORDIANNAME=accordian_name,
        CARDNUMBER=str(number),
        CARDHEADER=header,
        CARDBUTTON=button,
        CARDBODY=body,
        CARDOPEN="true" if show else "false",
        CARDSHOW="show" if show else ""
    )


def form(
        return_url: str,
        hidden_html: str,
        button_label: str,
        page: str
    ) -> str:
    '''A form with return url, hidden section customizable button label'''
    return HTMLSystem.part(
        "sections/form",
        RETURNURL=return_url,
        HIDDEN=hidden_html,
        BUTTONLABEL=button_label,
        PAGE=page
    )


def item(
        variable_name: str,
        label: str,
        help_text: str,
        input_html: str,
        not_in_config: bool = False
    ) -> str:
    ''' The whole section for each Config Object'''
    html = HTMLSystem.part(
        "sections/item",
        VARNAME=variable_name,
        LABEL=label if isinstance(label, str) else "",
        HELP=help_text if isinstance(help_text, str) else "",
        INPUT=input_html)
    #TODO need to remove this cs_ stuff
    if not_in_config:
        html = html.replace("cs_", "")
    return html


def modal(
        title: str,
        variable_name: str,
        modal_body: str,
        modal_footer: str,
        closeable: bool = True
    ) -> str:
    ''' Returnas a modal'''
    return HTMLSystem.part(
        "sections/modal",
        TITLE=title.title(),
        VARIABLENAME=variable_name,
        CLOSEABLE="" if closeable else 'style="display:none"',
        MODALBODY=modal_body,
        MODALFOOTER=modal_footer
    )


def list_modal(
        title: str,
        variable_name: str,
        option_list: str
    ) -> str:
    ''' Returnas a modal for a list of options for adding a multi plugin'''
    return HTMLSystem.part(
        "sections/list_modal",
        TITLE=title.title(),
        VARIABLENAME=variable_name,
        LIST=option_list
    )


def multi_modal(
        title: str,
        variable_name: str
    ) -> str:
    '''Returnas a modal for adding a multi plugin'''
    return HTMLSystem.part(
        "sections/multi_modal",
        TITLE=title.title(),
        VARIABLENAME=variable_name
    )


def multi_panel(
        variable_name: str,
        name: str,
        enable_option: str,
        delete_option: str,
        section_html: str,
        visible: bool = True
    ) -> str:
    '''Returns a panel for multi type plugin data'''
    return HTMLSystem.part(
        "sections/multi_panel",
        VARIABLENAME=variable_name,
        NAME=name,
        ENABLEDOPTION=enable_option,
        DELETEDOPTION=delete_option,
        SECTION=section_html,
        SECTIONHIDE="" if visible else 'style="display:none"'
    )


def panel(
        title: str,
        control: str,
        modal_obj: str,
        variable_name: str,
        section_html: str,
        visible: bool = True
    ) -> str:
    '''A Panel for plugins or sections'''
    titleb = "Tackem-Plugin-" + title.replace(" - ", "-")
    return HTMLSystem.part(
        "sections/panel",
        TITLE=title,
        TITLEB=titleb,
        CONTROL=control,
        MODAL=modal_obj,
        VARIABLENAME=variable_name if variable_name != "" else titleb,
        SECTION=section_html,
        SETIONHIDE=""if visible else 'style="display:none"'
    )


def plugin_panel(
        title: str,
        description: str,
        clear_config: str,
        clear_database: str,
        start_stop: str,
        add_remove: str
    ) -> str:
    '''A Panel for plugins or sections'''
    return HTMLSystem.part(
        "sections/plugin_panel",
        TITLE=title,
        DESCRIPTION=description,
        CLEARCONFIG=clear_config,
        CLEARDATABASE=clear_database,
        STARTSTOP=start_stop,
        ADDREMOVE=add_remove
    )


def search_modal() -> str:
    '''Returnas a modal for adding a multi plugin'''
    return HTMLSystem.part("sections/seaarch_modal")


def section(
        section_name: str,
        section_html: str,
        visible: bool = True
    ) -> str:
    '''A Panel for plugins or sections'''
    return HTMLSystem.part(
        "sections/section",
        SECTIONNAME=section_name,
        SECTION=section_html,
        SETIONHIDE=""if visible else 'style="display:none"'
    )


def tab_bar(tabs: str) -> str:
    '''Returns the tab bar section'''
    return HTMLSystem.part(
        "sections/tabbar",
        TABBARITEMS=tabs
    )


def tab_bar_item(plugin_name: str, active: bool = False) -> str:
    '''Returns a tab bar item'''
    return HTMLSystem.part(
        "sections/tabbaritem",
        PLUGINNAME=plugin_name,
        PLUGINNAMECAPITALIZE=plugin_name.title(),
        ACTIVE="active" if active else ""
    )


def tab_pane(plugin_name: str, plugin_html: str, active: bool = False) -> str:
    '''Returns a tab pane'''
    return HTMLSystem.part(
        "sections/tabpane",
        PLUGINNAME=plugin_name,
        PLUGINHTML=plugin_html,
        ACTIVE="active" if active else ""
    )


def text_item(text: str) -> str:
    ''' The whole section for each Config Object'''
    return HTMLSystem.part(
        "sections/text_item",
        TEXT=text
    )


########
#INPUTS#
########


def add_instance_button(plugin_name: str) -> str:
    '''returns the add instance button for multi plugins'''
    return HTMLSystem.part(
        "inputs/addinstancebutton",
        PLUGINNAME=plugin_name
    )


def delete_instance_button(plugin_name: str, name: str) -> str:
    '''returns the add instance button for multi plugins'''
    return HTMLSystem.part(
        "inputs/deleteinstancebutton",
        PLUGINNAME=plugin_name,
        NAME=name
    )


def input_button_with_data(
        value: str,
        id_name: str = "",
        class_name: str = "",
        data: bool = False,
        outer_div: bool = True,
        enabled: bool = True,
        visible: bool = True
    ) -> str:
    '''returns a button'''
    data_r = ""
    if isinstance(data, tuple):
        data_r = "data-" + data[0] + '="' + data[1] + '"'
    elif isinstance(data, dict):
        for key, value in data.items():
            data_r += " data-" + str(key) + '="' + str(value) + '"'

    return HTMLSystem.part(
        "inputs/inputbuttonwithdataappend" if outer_div else "inputs/inputbuttonwithdata",
        BUTTONVALUE=value,
        IDNAME=id_name,
        CLASSNAME=class_name,
        DATA=data_r,
        ENABLED="" if enabled else "disabled",
        VISIBLE="" if visible else 'style="display:none;"'
    )


def input_button(value: str, on_click: Union[str, bool] = False, outer_div: bool = True) -> str:
    '''shortcut for input_button_on_click'''
    return input_button_on_click(value, on_click, outer_div)


def input_button_on_click(value: str, on_click: Union[str, bool], outer_div: bool = True) -> str:
    '''returns a button'''
    return HTMLSystem.part(
        "inputs/inputbuttononclickappend" if outer_div else "inputs/inputbuttononclick",
        BUTTONVALUE=value,
        BUTTONCLICK=on_click
    )


def checkbox(name: str, variable_name: str, checkbox_html: str) -> str:
    '''returns the outside tags of the checkbox'''
    return HTMLSystem.part(
        "inputs/checkbox",
        VARIABLENAME=variable_name,
        TITLE=name,
        CHECKBOX=checkbox_html
    )

def _script(script_string, variable_name):
    '''Script Code For Multiple Functions'''
    if isinstance(script_string, str):
        return script_string
    if script_string is None:
        return "onchange='" + 'Switch("' + variable_name +'");' + "'"
    if script_string is True:
        script_string = "onchange='" + 'Switch("' + variable_name +'");'
        return script_string + 'ToggleSection("' + variable_name[:-1] + '");' + "'"

def checkbox_multi(
        label: str,
        variable_name: str,
        value: str,
        checked: bool = True,
        disabled: bool = False,
        read_only: bool = False,
        script: Union[str, bool, None] = None
    ) -> str:
    '''returns a multi checkbox'''
    return HTMLSystem.part(
        "inputs/multicheckbox",
        CHECKED="checked" if checked else "",
        DISABLED="disabled" if disabled else "",
        READONLY="readonly" if read_only else "",
        SCRIPT=_script(script, variable_name),
        SWITCH="",
        VALUE=value,
        LABEL=label,
        VARIABLENAME=variable_name
    )


def checkbox_single(
        name: str,
        variable_name: str,
        checked: bool = True,
        disabled: bool = False,
        read_only: bool = False,
        script: Union[str, bool, None] = None
    ) -> str:
    '''returns a single checkbox'''
    return HTMLSystem.part(
        "inputs/singlecheckbox",
        ENABLED=str(checked),
        CHECKED="checked" if checked else "",
        DISABLED="disabled" if disabled else "",
        READONLY="readonly" if read_only else "",
        SCRIPT=_script(script, variable_name),
        SWITCH="",
        VARIABLENAME=variable_name + name
    )


def checkbox_switch(
        name: str,
        variable_name: str,
        checked: bool = True,
        disabled: bool = False,
        read_only: bool = False,
        script: Union[str, bool, None] = None
    ) -> str:
    '''returns a single checkbox'''
    return HTMLSystem.part(
        "inputs/singlecheckbox",
        ENABLED=str(checked),
        CHECKED="checked" if checked else "",
        DISABLED="disabled" if disabled else "",
        READONLY="readonly" if read_only else "",
        SCRIPT=_script(script, variable_name),
        SWITCH=HTMLSystem.open("inputs/switchoptions"),
        VARIABLENAME=variable_name + name
    )


def hidden(name: str, value: str, not_in_config: bool = False) -> str:
    '''A hidden field for the page index'''
    html = HTMLSystem.part(
        "inputs/hidden",
        NAME=name,
        VALUE=value
    )

    #TODO need to remove this cs_ stuff
    if not_in_config:
        html = html.replace("cs_", "")
    return html


def hidden_page_index(page_index: int) -> str:
    '''A hidden field for the page index'''
    return HTMLSystem.part(
        "inputs/hiddenpageindex",
        PAGEINDEX=page_index
    )


def input_box(
        input_type: str,
        variable_name: str,
        value: str,
        script: str = "",
        max_length: Union[int, None] = None,
        minimum: Union[int, None] = None,
        maximum: Union[int, None] = None,
        read_only: bool = False,
        disabled: bool = False,
        button: str = ""
    ) -> str:
    '''Returns an input object'''
    return HTMLSystem.part(
        "inputs/input",
        INPUTTYPE=input_type,
        VARIABLENAME=variable_name,
        VALUE=value,
        SCRIPT=script if isinstance(script, str) else "",
        MAXLENGTH=' maxlength="' + str(max_length) + '"' if isinstance(max_length, int) else "",
        MIN=' min="' + str(minimum) + '"' if isinstance(minimum, int) else "",
        MAX=' max="' + str(maximum) + '"' if isinstance(maximum, int) else "",
        DISABLED="disabled" if disabled else "",
        READONLY="readonly" if read_only else "",
        BUTTON=button if button else ""
    )


def radio_option(
        variable_name: str,
        name: str,
        label: str,
        checked: bool = False,
        disabled: bool = False,
        read_only: bool = False,
        script: str = ""
    ) -> str:
    '''makes a radio option'''
    return HTMLSystem.part(
        "inputs/radio",
        VARIABLENAME=variable_name,
        NAME=name,
        LABEL=label,
        CHECKED="checked" if checked else "",
        DISABLED="disabled" if disabled else "",
        READONLY="readonly" if read_only else "",
        SCRIPT=script if isinstance(script, str) else ""
    )


def select_box_option(
        name: str,
        label: str,
        selected: bool = False,
        disabled: bool = False,
        read_only: bool = False,
        script: str = ""
    ) -> str:
    '''makes an option for the selection box'''
    select_option = " -- select an option -- "
    return HTMLSystem.part(
        "inputs/option",
        NAME=name if isinstance(name, str) and name != "" else "",
        NAMECAPITALIZE=label if isinstance(name, str) and name != "" else select_option,
        SELECTED="selected" if selected else "",
        DISABLED="disabled" if disabled else "",
        READONLY="readonly" if read_only else "",
        SCRIPT=script if isinstance(script, str) else ""
    )


def select_box(
        variable_name: str,
        value: Union[str, None],
        options_html: Union[str, list],
        multiple: bool = False,
        box_size: int = 0,
        script: str = "",
        read_only: bool = False,
        disabled: bool = False
    ) -> str:
    '''Makes A select box'''
    options_out_html = ""
    blank_options_html = select_box_option(False, True, True) if value is None else ""
    if isinstance(options_html, str):
        options_out_html = options_html
    else:
        for option in options_html:
            options_out_html += option.html_option(value)

    return HTMLSystem.part(
        "inputs/selectbox",
        VARIABLENAME=variable_name,
        MULTIPLE='multiple' if multiple else "",
        SIZE='size="' + box_size + '"' if box_size > 1 else "",
        DISABLED="disabled" if disabled else "",
        READ_ONLY="readonly" if read_only else "",
        SCRIPT=script if isinstance(script, str) else "",
        OPTIONS=blank_options_html + options_out_html
    )


######
#TAGS#
######


def script_link(location: str) -> str:
    '''returns a script link item'''
    return HTMLSystem.part(
        "tags/scriptlink",
        LOCATION=location
    )


def stylesheet_link(location: str) -> str:
    '''returns a script link item'''
    return HTMLSystem.part(
        "tags/stylesheetlink",
        LOCATION=location
    )


#########
##OTHER##
#########


def quick_table(data: dict) -> str:
    '''creates a table from a dictionary'''
    table_body_html = HTMLSystem.open("other/tablebody")
    table_head_html = HTMLSystem.open("other/tablehead")
    head_html = ""
    body_html = ""
    for key in data:
        head_html += table_head_html.replace("%%HEADER%%", key)
        body_html += table_body_html.replace("%%VALUE%%", str(data[key]))

    return HTMLSystem.part(
        "other/table",
        HEADERS=head_html,
        VALUES=body_html
    )


def progress_bar(label: str, value, max_value: int, percent: Union[int, float]) -> str:
    '''creates a progress bar'''
    return HTMLSystem.part(
        "other/progressbar",
        LABEL=label,
        VALUE=value,
        MAX=max_value,
        PARCENT=percent
    )


def dim_screen() -> str:
    '''creates system for a dimmed screen'''
    return HTMLSystem.part("other/dimscreen")


#########
##ADMIN##
#########


def users_page(users_html: str) -> str:
    '''creates a users page'''
    return HTMLSystem.part(
        "admin/users",
        USERSHTML=users_html
    )


def user_page(user_id: int, username: str, is_admin: bool) -> str:
    '''creates a user page'''
    return HTMLSystem.part(
        "admin/user",
        USERID=user_id,
        USERNAME=username,
        ADMINTRUE="checked" if is_admin else "",
        ADMINFALSE="" if is_admin else "checked"
    )
