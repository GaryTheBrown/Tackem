'''Functions to deal with all the html template parts'''
from libs.startup_arguments import PROGRAMVERSION


#################
#MASTER TEMPLATE#
#################


def master_template(title, body, javascript_extra, stylesheet_extra, baseurl, navbar):
    '''head section of the template'''
    html = str(open("www/html/pages/template.html", "r").read())
    html = html.replace("%%JAVASCRIPTEXTRA%%", javascript_extra)
    html = html.replace("%%STYLESHEETEXTRA%%", stylesheet_extra)
    html = html.replace("%%NAVBAR%%", navbar)
    html = html.replace("%%BODY%%", body)
    html = html.replace("%%BASEURL%%", baseurl)
    html = html.replace("%%PROGRAMVERSION%%", PROGRAMVERSION)
    return html.replace("%%TITLE%%", title)


########
#NAVBAR#
########


def navbar_dropdown(title, dropdown_id, items):
    '''A Navbar Item (not active)'''
    html = str(open("www/html/navbar/dropdown.html", "r").read())
    html = html.replace("%%TITLE%%", title.title())
    html = html.replace("%%DROPDOWNID%%", dropdown_id)
    return html.replace("%%ITEMS%%", items)


def navbar_dropdown_left(title, dropdown_id, items):
    '''A Navbar Item left aligned (not active)'''
    html = str(open("www/html/navbar/dropdownleft.html", "r").read())
    html = html.replace("%%TITLE%%", title.title())
    html = html.replace("%%DROPDOWNID%%", dropdown_id)
    return html.replace("%%ITEMS%%", items)


def navbar_dropdown_right(title, dropdown_id, items):
    '''A Navbar Item right aligned (not active)'''
    html = str(open("www/html/navbar/dropdownright.html", "r").read())
    html = html.replace("%%TITLE%%", title.title())
    html = html.replace("%%DROPDOWNID%%", dropdown_id)
    return html.replace("%%ITEMS%%", items)


def navbar_drop_left(title, dropdown_id, items):
    '''A Navbar Item (not active)'''
    html = str(open("www/html/navbar/dropleft.html", "r").read())
    html = html.replace("%%TITLE%%", title.title())
    html = html.replace("%%DROPDOWNID%%", dropdown_id)
    return html.replace("%%ITEMS%%", items)


def navbar_drop_right(title, dropdown_id, items):
    '''A Navbar Item (not active)'''
    html = str(open("www/html/navbar/dropright.html", "r").read())
    html = html.replace("%%TITLE%%", title.title())
    html = html.replace("%%DROPDOWNID%%", dropdown_id)
    return html.replace("%%ITEMS%%", items)


def navbar_item(title, url):
    '''A Navbar Item (not active)'''
    html = str(open("www/html/navbar/item.html", "r").read())
    html = html.replace("%%TITLE%%", title.title())
    return html.replace("%%URL%%", url.replace(" ", "/"))


def navbar_item_active(title):
    '''A Navbar Item (not active)'''
    html = str(open("www/html/navbar/itemactive.html", "r").read())
    return html.replace("%%TITLE%%", title.title())


def navbar_master(navbar_items, navbar_right_items):
    '''master file for the navbar'''
    html = str(open("www/html/navbar/master.html", "r").read())
    html = html.replace("%%NAVBARRIGHT%%", navbar_right_items)
    return html.replace("%%NAVBARITEMS%%", navbar_items)


#######
#PAGES#
#######


def plugin_config_page(tab_bar_tabs, sections):
    '''Plugin config page'''
    html = str(open("www/html/pages/pluginconfigpage.html", "r").read())
    html = html.replace("%%PANELTABS%%", tab_bar_tabs)
    return html.replace("%%PLUGINLIST%%", sections)


def root_config_page(sections):
    '''Root config page'''
    html = str(open("www/html/pages/rootconfigpage.html", "r").read())
    return html.replace("%%PLUGINLIST%%", sections)


def login_page(return_url):
    '''Root config page'''
    html = str(open("www/html/pages/login.html", "r").read())
    return html.replace("%%RETURNURL%%", return_url)


def password_page():
    '''Root config page'''
    html = str(open("www/html/pages/password.html", "r").read())
    return html


##########
#SECTIONS#
##########


def accordian(accordian_name, accordian_cards):
    '''outside of the accordian'''
    html = str(open("www/html/sections/accordian.html", "r").read())
    html = html.replace("%%ACCORDIANNAME%%", accordian_name)
    return html.replace("%%ACCORDIANCARDS%%", accordian_cards)


def accordian_card(accordian_name, number, header, button, body, show=False):
    '''section for the accordian'''
    html = str(open("www/html/sections/accordiancard.html", "r").read())
    html = html.replace("%%ACCORDIANNAME%%", accordian_name)
    html = html.replace("%%CARDNUMBER%%", str(number))
    html = html.replace("%%CARDHEADER%%", header)
    html = html.replace("%%CARDBUTTON%%", button)
    html = html.replace("%%CARDBODY%%", body)
    if show:
        html = html.replace("%%CARDOPEN%%", "true")
        html = html.replace("%%CARDSHOW%%", "show")
    else:
        html = html.replace("%%CARDOPEN%%", "false")
        html = html.replace("%%CARDSHOW%%", "")
    return html


def form(return_url, hidden_html, button_label, page):
    '''A form with return url, hidden section customizable button label'''
    html = str(open("www/html/sections/form.html", "r").read())
    html = html.replace("%%RETURNURL%%", return_url)
    html = html.replace("%%HIDDEN%%", hidden_html)
    html = html.replace("%%BUTTONLABEL%%", button_label)
    return html.replace("%%PAGE%%", page)


def item(variable_name, label, help_text, input_html, not_in_config=False):
    ''' The whole section for each Config Object'''
    html = str(open("www/html/sections/item.html", "r").read())
    html = html.replace("%%VARNAME%%", variable_name)
    if not isinstance(label, str):
        label = ""
    html = html.replace("%%LABEL%%", label)
    if not isinstance(help_text, str):
        help_text = ""
    html = html.replace("%%HELP%%", help_text)
    html = html.replace("%%INPUT%%", input_html)
    if not_in_config:
        html = html.replace("cs_", "")
    return html


def modal(title, variable_name, modal_body, modal_footer, closeable=True):
    ''' Returnas a modal'''
    html = str(open("www/html/sections/modal.html", "r").read())
    html = html.replace("%%TITLE%%", title.title())
    html = html.replace("%%VARIABLENAME%%", variable_name)
    if closeable:
        html = html.replace("%%CLOSEABLE%%", "")
    else:
        html = html.replace("%%CLOSEABLE%%", 'style="display:none"')
    html = html.replace("%%MODALBODY%%", modal_body)
    return html.replace("%%MODALFOOTER%%", modal_footer)


def list_modal(title, variable_name, option_list):
    ''' Returnas a modal for a list of options for adding a multi plugin'''
    html = str(open("www/html/sections/list_modal.html", "r").read())
    html = html.replace("%%TITLE%%", title.title())
    html = html.replace("%%VARIABLENAME%%", variable_name)
    return html.replace("%%LIST%%", option_list)


def multi_modal(title, variable_name):
    '''Returnas a modal for adding a multi plugin'''
    html = str(open("www/html/sections/multi_modal.html", "r").read())
    html = html.replace("%%TITLE%%", title.title())
    return html.replace("%%VARIABLENAME%%", variable_name)


def multi_panel(variable_name, name, enable_option, delete_option, section_html, visible=True):
    '''Returns a panel for multi type plugin data'''
    html = str(open("www/html/sections/multi_panel.html", "r").read())
    html = html.replace("%%VARIABLENAME%%", variable_name)
    html = html.replace("%%NAME%%", name)
    html = html.replace("%%ENABLEDOPTION%%", enable_option)
    html = html.replace("%%DELETEOPTION%%", delete_option)
    html = html.replace("%%SECTION%%", section_html)
    if not visible:
        return html.replace("%%SECTIONHIDE%%", 'style="display:none"')
    return html.replace("%%SECTIONHIDE%%", "")


def panel(title, control, modal_obj, variable_name, section_html, visible=True):
    '''A Panel for plugins or sections'''
    html = str(open("www/html/sections/panel.html", "r").read())
    html = html.replace("%%TITLE%%", title)
    if control == "":
        html = html.replace('<div id="%%TITLEB%%_control">%%CONTROL%%</div>', "")
    else:
        html = html.replace("%%CONTROL%%", control)
        html = html.replace("%%TITLEB%%", "Tackem-Plugin-" + title.replace(" - ", "-"))
    html = html.replace("%%MODAL%%", modal_obj)
    if variable_name == "":
        html = html.replace('id="%%VARIABLENAME%%_section"', variable_name)
    else:
        html = html.replace("%%VARIABLENAME%%", variable_name)
    html = html.replace("%%SECTION%%", section_html)
    if not visible:
        return html.replace("%%SECTIONHIDE%%", 'style="display:none"')
    return html.replace("%%SECTIONHIDE%%", "")


def plugin_panel(title, description, clear_config, clear_database, start_stop, add_remove):
    '''A Panel for plugins or sections'''
    html = str(open("www/html/sections/plugin_panel.html", "r").read())
    html = html.replace("%%TITLE%%", title)
    html = html.replace("%%DESCRIPTION%%", description)
    html = html.replace("%%CLEARCONFIG%%", clear_config)
    html = html.replace("%%CLEARDATABASE%%", clear_database)
    html = html.replace("%%STARTSTOP%%", start_stop)
    return html.replace("%%ADDREMOVE%%", add_remove)


def search_modal():
    '''Returnas a modal for adding a multi plugin'''
    return str(open("www/html/sections/search_modal.html", "r").read())


def section(section_name, section_html, visible=True):
    '''A Panel for plugins or sections'''
    html = str(open("www/html/sections/section.html", "r").read())
    html = html.replace("%%SECTIONNAME%%", section_name)
    html = html.replace("%%SECTION%%", section_html)
    if not visible:
        return html.replace("%%SECTIONHIDE%%", 'style="display:none"')
    return html.replace("%%SECTIONHIDE%%", "")


def tab_bar(tabs):
    '''Returns the tab bar section'''
    html = str(open("www/html/sections/tabbar.html", "r").read())
    return html.replace("%%TABBARITEMS%%", tabs)


def tab_bar_item(plugin_name, active=False):
    '''Returns a tab bar item'''
    html = str(open("www/html/sections/tabbaritem.html", "r").read())
    html = html.replace("%%PLUGINNAME%%", plugin_name)
    html = html.replace("%%PLUGINNAMECAPITALIZE%%", plugin_name.title())
    if active:
        return html.replace("%%ACTIVE%%", "active")
    return html.replace("%%ACTIVE%%", "")


def tab_pane(plugin_name, plugin_html, active=False):
    '''Returns a tab pane'''
    html = str(open("www/html/sections/tabpane.html", "r").read())
    html = html.replace("%%PLUGINNAME%%", plugin_name)
    html = html.replace("%%PLUGINHTML%%", plugin_html)
    if active:
        return html.replace("%%ACTIVE%%", "active")
    return html.replace("%%ACTIVE%%", "")


def text_item(text):
    ''' The whole section for each Config Object'''
    html = str(open("www/html/sections/text_item.html", "r").read())
    html = html.replace("%%TEXT%%", text)
    return html


########
#INPUTS#
########


def add_instance_button(plugin_name):
    '''returns the add instance button for multi plugins'''
    html = str(open("www/html/inputs/addinstancebutton.html", "r").read())
    return html.replace("%%PLUGINNAME%%", plugin_name)


def delete_instance_button(plugin_name, name):
    '''returns the add instance button for multi plugins'''
    html = str(open("www/html/inputs/deleteinstancebutton.html", "r").read())
    html = html.replace("%%PLUGINNAME%%", plugin_name)
    return html.replace("%%NAME%%", name)


def input_button_with_data(value, id_name="", class_name="", data=False,
                           outer_div=True, enabled=True, visible=True):
    '''returns a button'''
    html = str(open("www/html/inputs/inputbuttonwithdata.html", "r").read())
    html = html.replace("%%BUTTONVALUE%%", value)
    if not outer_div:
        html = html.replace('<div class="input-group-append">', "")
        html = html.replace('</div>', "")
    html = html.replace("%%IDNAME%%", id_name)
    html = html.replace("%%CLASSNAME%%", class_name)
    if data is False:
        return html.replace(" %%DATA%%", "")
    data_r = ""
    if isinstance(data, tuple):
        data_r = "data-" + data[0] + '="' + data[1] + '"'
    elif isinstance(data, dict):
        for key, value in data.items():
            data_r += " data-" + str(key) + '="' + str(value) + '"'

    html = html.replace("%%DATA%%", data_r)

    if enabled:
        html = html.replace("%%ENABLED%%", "")
    else:
        html = html.replace("%%ENABLED%%", "disabled")
    if visible:
        html = html.replace("%%VISIBLE%%", "")
    else:
        html = html.replace("%%VISIBLE%%", "style='display:none;'")
    return html


def input_button(value, on_click=False, outer_div=True):
    '''shortcut for input_button_on_click'''
    return input_button_on_click(value, on_click, outer_div)


def input_button_on_click(value, on_click, outer_div=True):
    '''returns a button'''
    html = str(open("www/html/inputs/inputbuttononclick.html", "r").read())
    html = html.replace("%%BUTTONVALUE%%", value)
    if not outer_div:
        html = html.replace('<div class="input-group-append">', "")
        html = html.replace('</div>', "")
    return html.replace("%%BUTTONONCLICK%%", on_click)


def checkbox(name, variable_name, checkbox_html):
    '''returns the outside tags of the checkbox'''
    html = str(open("www/html/inputs/checkbox.html", "r").read())
    html = html.replace("%%VARIABLENAME%%", variable_name)
    html = html.replace("%%TITLE%%", name)
    return html.replace("%%CHECKBOX%%", checkbox_html)


def checkbox_multi(label, variable_name, value, checked=True, disabled=False, read_only=False,
                   script=None):
    '''returns a multi checkbox'''
    html = str(open("www/html/inputs/multicheckbox.html", "r").read())
    checked = "checked" if checked else ""
    disabled = "disabled" if disabled else ""
    read_only = "readonly" if read_only else ""
    html = html.replace("%%CHECKED%%", checked)
    html = html.replace("%%DISABLED%%", disabled)
    html = html.replace("%%READONLY%%", read_only)
    if script is None:
        script = "onchange='" + 'Switch("' + variable_name +'");' + "'"
    if script is True:
        script = "onchange='" + 'Switch("' + variable_name +'");'
        script += 'ToggleSection("' + variable_name[:-1] + '");' + "'"
    html = html.replace("%%SCRIPT%%", script)
    html = html.replace("%%SWITCH%%", "")
    html = html.replace("%%VALUE%%", value)
    html = html.replace("%%LABEL%%", label)
    return html.replace("%%VARIABLENAME%%", variable_name)


def checkbox_single(name, variable_name, checked=True, disabled=False, read_only=False,
                    script=None):
    '''returns a single checkbox'''
    html = str(open("www/html/inputs/singlecheckbox.html", "r").read())
    if checked:
        checked = "checked"
        html = html.replace("%%ENABLED%%", "True")
    else:
        checked = ""
        html = html.replace("%%ENABLED%%", "False")
    disabled = "disabled" if disabled else ""
    read_only = "readonly" if read_only else ""
    html = html.replace("%%CHECKED%%", checked)
    html = html.replace("%%DISABLED%%", disabled)
    html = html.replace("%%READONLY%%", read_only)
    if script is None:
        script = "onchange='" + 'Switch("' + variable_name + name +'");' + "'"
    if script is True:
        script = "onchange='" + 'Switch("' + variable_name + name +'");'
        script += 'ToggleSection("' + variable_name[:-1] + '");' + "'"
    html = html.replace("%%SCRIPT%%", script)
    html = html.replace("%%SWITCH%%", "")
    return html.replace("%%VARIABLENAME%%", variable_name + name)


def checkbox_switch(name, variable_name, checked=True, disabled=False, read_only=False,
                    script=None):
    '''returns a single checkbox'''
    single_checkbox_html = str(open("www/html/inputs/singlecheckbox.html", "r").read())
    switch_html = str(open("www/html/inputs/switchoptions.html", "r").read())
    html = single_checkbox_html.replace("%%SWITCH%%", switch_html)
    enabled = str(checked)
    checked = "checked" if checked else ""
    disabled = "disabled" if disabled else ""
    read_only = "readonly" if read_only else ""
    html = html.replace("%%CHECKED%%", checked)
    html = html.replace("%%ENABLED%%", enabled)
    html = html.replace("%%DISABLED%%", disabled)
    html = html.replace("%%READONLY%%", read_only)
    if script is None:
        script = "onchange='" + 'Switch("' + variable_name + name +'");' + "'"
    if script is True:
        script = "onchange='" + 'Switch("' + variable_name + name +'");'
        script += 'ToggleSection("' + variable_name[:-1] + '");' + "'"
    html = html.replace("%%SCRIPT%%", script)
    html = html.replace("%%VARIABLENAME%%", variable_name + name)
    return html


def hidden(name, value, not_in_config=False):
    '''A hidden field for the page index'''
    html = str(open("www/html/inputs/hidden.html", "r").read())
    html = html.replace("%%NAME%%", name)
    html = html.replace("%%VALUE%%", value)
    if not_in_config:
        html = html.replace("cs_", "")
    return html


def hidden_page_index(page_index):
    '''A hidden field for the page index'''
    html = str(open("www/html/inputs/hiddenpageindex.html", "r").read())
    return html.replace("%%PAGEINDEX%%", str(page_index))


def input_box(input_type, variable_name, value, script="", max_length=None, minimum=None,
              maximum=None, read_only=False, disabled=False, button=""):
    '''Returns an input object'''
    html = str(open("www/html/inputs/input.html", "r").read())
    html = html.replace("%%INPUTTYPE%%", input_type)
    html = html.replace("%%VARIABLENAME%%", variable_name)
    html = html.replace("%%VALUE%%", ' value="' + str(value) + '"')
    if not isinstance(script, str):
        script = ""
    html = html.replace("%%SCRIPT%%", script)
    if isinstance(max_length, int):
        html = html.replace("%%MAXLENGTH%%", ' maxlength="' + str(max_length) + '"')
    else:
        html = html.replace("%%MAXLENGTH%%", "")
    if isinstance(minimum, int):
        html = html.replace("%%MIN%%", ' min="' + str(minimum) + '"')
    else:
        html = html.replace("%%MIN%%", "")
    if isinstance(maximum, int):
        html = html.replace("%%MAX%%", ' max="' + str(maximum) + '"')
    else:
        html = html.replace("%%MAX%%", "")
    disabled = "disabled" if disabled else ""
    read_only = "readonly" if read_only else ""
    html = html.replace("%%DISABLED%%", disabled)
    html = html.replace("%%READONLY%%", read_only)
    if button:
        return html.replace("%%BUTTON%%", button)
    return html.replace("%%BUTTON%%", "")


def radio_option(variable_name, name, label, checked=False, disabled=False,
                 read_only=False, script=""):
    '''makes a radio option'''
    html = str(open("www/html/inputs/radio.html", "r").read())
    html = html.replace("%%VARIABLENAME%%", variable_name)
    html = html.replace("%%NAME%%", name)
    html = html.replace("%%LABEL%%", label)
    checked = "checked" if checked else ""
    disabled = "disabled" if disabled else ""
    read_only = "readonly" if read_only else ""
    html = html.replace("%%CHECKED%%", checked)
    html = html.replace("%%DISABLED%%", disabled)
    html = html.replace("%%READONLY%%", read_only)
    if not isinstance(script, str):
        script = ""
    html = html.replace("%%SCRIPT%%", script)
    return html


def select_box_option(name, label, selected=False,
                      disabled=False, read_only=False, script=""):
    '''makes an option for the selection box'''
    html = str(open("www/html/inputs/option.html", "r").read())
    if isinstance(name, str) and name != "":
        html = html.replace("%%NAME%%", name)
        html = html.replace("%%NAMECAPITALIZE%%", label)
    else:
        html = html.replace("%%NAME%%", "")
        html = html.replace("%%NAMECAPITALIZE%%", " -- select an option -- ")
    selected = "selected" if selected else ""
    disabled = "disabled" if disabled else ""
    read_only = "readonly" if read_only else ""
    html = html.replace("%%SELECTED%%", selected)
    html = html.replace("%%DISABLED%%", disabled)
    html = html.replace("%%READONLY%%", read_only)
    if not isinstance(script, str):
        script = ""
    html = html.replace("%%SCRIPT%%", script)
    return html


def select_box(variable_name, value, options_html, multiple=False, box_size=0, script="",
               read_only=False, disabled=False):
    '''Makes A select box'''
    html = str(open("www/html/inputs/selectbox.html", "r").read())
    html = html.replace("%%VARIABLENAME%%", variable_name)
    if multiple:
        html = html.replace('%%MULTIPLE%%', 'multiple')
    else:
        html = html.replace(' %%MULTIPLE%%', '')
    if box_size > 1:
        html = html.replace('%%SIZE%%', 'size="' + box_size + '"')
    else:
        html = html.replace(' %%SIZE%%', '')
    disabled = "disabled" if disabled else ""
    read_only = "readonly" if read_only else ""
    html = html.replace("%%DISABLED%%", disabled)
    html = html.replace("%%READONLY%%", read_only)
    if isinstance(script, str):
        html = html.replace("%%SCRIPT%%", script)
    else:
        html = html.replace("%%SCRIPT%%", "")
    if value is None:
        blank_options_html = select_box_option(False, True, True)
    else:
        blank_options_html = ""
    if isinstance(options_html, str):
        return html.replace("%%OPTIONS%%", blank_options_html + options_html)
    options_out_html = ""
    for option in options_html:
        options_out_html += option.html_option(value)
    return html.replace("%%OPTIONS%%", blank_options_html + options_out_html)


######
#TAGS#
######


def script_link(location):
    '''returns a script link item'''
    html = str(open("www/html/tags/scriptlink.html", "r").read())
    return html.replace("%%LOCATION%%", location)


def stylesheet_link(location):
    '''returns a script link item'''
    html = str(open("www/html/tags/stylesheetlink.html", "r").read())
    return html.replace("%%LOCATION%%", location)


#########
##OTHER##
#########


def quick_table(data):
    '''creates a table from a dictionary'''
    html = str(open("www/html/other/table.html", "r").read())
    table_body_html = str(open("www/html/other/tablebody.html", "r").read())
    table_head_html = str(open("www/html/other/tablehead.html", "r").read())
    head_html = ""
    body_html = ""
    for key in data:
        head_html += table_head_html.replace("%%HEADER%%", key)
        body_html += table_body_html.replace("%%VALUE%%", str(data[key]))
    return html.replace("%%HEADERS%%", head_html).replace("%%VALUES%%", body_html)


def progress_bar(label, value, max_value, percent):
    '''creates a progress bar'''
    html = str(open("www/html/other/progressbar.html", "r").read())
    html = html.replace("%%LABEL%%", str(label))
    html = html.replace("%%VALUE%%", str(value))
    html = html.replace("%%MAX%%", str(max_value))
    html = html.replace("%%PERCENT%%", str(percent))
    return html


def dim_screen():
    '''creates system for a dimmed screen'''
    return '<div id="dim_screen"></div>'


#########
##ADMIN##
#########


def users_page(users_html):
    '''creates a progress bar'''
    html = str(open("www/html/admin/users.html", "r").read())
    html = html.replace("%%USERSHTML%%", users_html)
    return html


def user_page(user_id, username, is_admin):
    '''creates a progress bar'''
    html = str(open("www/html/admin/user.html", "r").read())
    html = html.replace("%%USERID%%", str(user_id))
    html = html.replace("%%USERNAME%%", str(username))
    if is_admin:
        html = html.replace("%%ADMINTRUE%%", "checked")
        html = html.replace("%%ADMINFALSE%%", "")
    else:
        html = html.replace("%%ADMINTRUE%%", "")
        html = html.replace("%%ADMINFALSE%%", "checked")
    return html
