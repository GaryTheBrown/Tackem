'''Functions to deal with all the html template parts'''
from libs.startup_arguments import PROGRAMVERSION
#################
#MASTER TEMPLATE#
#################
def master_template(title, body, javascript_extra, baseurl, navbar):
    '''head section of the template'''
    head_page = str(open("www/html/pages/template.html", "r").read())
    head_page = head_page.replace("%%JAVASCRIPTEXTRA%%", javascript_extra)
    head_page = head_page.replace("%%NAVBAR%%", navbar)
    head_page = head_page.replace("%%BODY%%", body)
    head_page = head_page.replace("%%BASEURL%%", baseurl)
    head_page = head_page.replace("%%PROGRAMVERSION%%", PROGRAMVERSION)
    return head_page.replace("%%TITLE%%", title)

########
#NAVBAR#
########
def navbar_dropdown(title, dropdown_id, items):
    '''A Navber Item (not active)'''
    navbar_dropdown_html = str(open("www/html/navbar/dropdown.html", "r").read())
    navbar_dropdown_html = navbar_dropdown_html.replace("%%TITLE%%", title.title())
    navbar_dropdown_html = navbar_dropdown_html.replace("%%DROPDOWNID%%", dropdown_id)
    return navbar_dropdown_html.replace("%%ITEMS%%", items)

def navbar_dropdown_right(title, dropdown_id, items):
    '''A Navber Item (not active)'''
    navbar_dropdown_html = str(open("www/html/navbar/dropdownright.html", "r").read())
    navbar_dropdown_html = navbar_dropdown_html.replace("%%TITLE%%", title.title())
    navbar_dropdown_html = navbar_dropdown_html.replace("%%DROPDOWNID%%", dropdown_id)
    return navbar_dropdown_html.replace("%%ITEMS%%", items)

def navbar_item(title, url):
    '''A Navber Item (not active)'''
    navbar_item_html = str(open("www/html/navbar/item.html", "r").read())
    navbar_item_html = navbar_item_html.replace("%%TITLE%%", title.title())
    return navbar_item_html.replace("%%URL%%", url.replace(" ", "/"))

def navbar_item_active(title):
    '''A Navber Item (not active)'''
    navbar_item_html = str(open("www/html/navbar/itemactive.html", "r").read())
    return navbar_item_html.replace("%%TITLE%%", title.title())

def navbar_master(nav_bar_items):
    '''master file for the navbar'''
    navbar_master_html = str(open("www/html/navbar/master.html", "r").read())
    return navbar_master_html.replace("%%NAVBARITEMS%%", nav_bar_items)

#######
#PAGES#
#######
def plugin_config_page(tab_bar_tabs, sections):
    '''Plugin config page'''
    page = str(open("www/html/pages/pluginconfigpage.html", "r").read())
    page = page.replace("%%PANELTABS%%", tab_bar_tabs)
    return page.replace("%%PLUGINLIST%%", sections)

def root_config_page(sections):
    '''Root config page'''
    page = str(open("www/html/pages/rootconfigpage.html", "r").read())
    return page.replace("%%PLUGINLIST%%", sections)

##########
#SECTIONS#
##########
def form(return_url, hidden, button_label, page):
    '''A form with return url, hidden section customizable button label'''
    form_html = str(open("www/html/sections/form.html", "r").read())
    form_html = form_html.replace("%%RETURNURL%%", return_url)
    form_html = form_html.replace("%%HIDDEN%%", hidden)
    form_html = form_html.replace("%%BUTTONLABEL%%", button_label)
    return form_html.replace("%%PAGE%%", page)

def item(variable_name, label, help_text, input_html, not_in_config=False):
    ''' The whole section for each Config Object'''
    item_html = str(open("www/html/sections/item.html", "r").read())
    item_html = item_html.replace("%%VARNAME%%", variable_name)
    item_html = item_html.replace("%%LABEL%%", label)
    if isinstance(help_text, str):
        item_html = item_html.replace("%%HELP%%", help_text)
    else:
        item_html = item_html.replace("%%HELP%%", '')
    item_html = item_html.replace("%%INPUT%%", input_html)
    if not_in_config:
        item_html = item_html.replace("cs_", "")
    return item_html

def list_modal(title, variable_name, option_list):
    ''' Returnas a modal for a list of options for adding a multi plugin'''
    list_modal_html = str(open("www/html/sections/list_modal.html", "r").read())
    list_modal_html = list_modal_html.replace("%%TITLE%%", title.title())
    list_modal_html = list_modal_html.replace("%%VARIABLENAME%%", variable_name)
    return list_modal_html.replace("%%LIST%%", option_list)

def multi_modal(title, variable_name):
    '''Returnas a modal for adding a multi plugin'''
    multi_modal_html = str(open("www/html/sections/multi_modal.html", "r").read())
    multi_modal_html = multi_modal_html.replace("%%TITLE%%", title.title())
    return multi_modal_html.replace("%%VARIABLENAME%%", variable_name)

def multi_panel(variable_name, name, enable_option, delete_option, section_html, section_visible):
    '''Returns a panel for multi type plugin data'''
    multi_panel_html = str(open("www/html/sections/multi_panel.html", "r").read())
    multi_panel_html = multi_panel_html.replace("%%VARIABLENAME%%", variable_name)
    multi_panel_html = multi_panel_html.replace("%%NAME%%", name)
    multi_panel_html = multi_panel_html.replace("%%ENABLEDOPTION%%", enable_option)
    multi_panel_html = multi_panel_html.replace("%%DELETEOPTION%%", delete_option)
    multi_panel_html = multi_panel_html.replace("%%SECTION%%", section_html)
    if not section_visible:
        return multi_panel_html.replace("%%SECTIONHIDE%%", 'style="display:none"')
    return multi_panel_html.replace("%%SECTIONHIDE%%", "")

def panel(name, title, control, modal, variable_name, section_html, section_visible):
    '''A Panel for plugins or sections'''
    panel_html = str(open("www/html/sections/panel.html", "r").read())
    panel_html = panel_html.replace("%%NAME%%", name)
    panel_html = panel_html.replace("%%TITLE%%", title)
    panel_html = panel_html.replace("%%CONTROL%%", control)
    panel_html = panel_html.replace("%%MODAL%%", modal)
    panel_html = panel_html.replace("%%VARIABLENAME%%", variable_name)
    panel_html = panel_html.replace("%%SECTION%%", section_html)
    if not section_visible:
        return panel_html.replace("%%SECTIONHIDE%%", 'style="display:none"')
    return panel_html.replace("%%SECTIONHIDE%%", "")

def section(section_name, section_html, section_visible):
    '''A Panel for plugins or sections'''
    panel_html = str(open("www/html/sections/section.html", "r").read())
    panel_html = panel_html.replace("%%SECTIONNAME%%", section_name)
    panel_html = panel_html.replace("%%SECTION%%", section_html)
    if not section_visible:
        return panel_html.replace("%%SECTIONHIDE%%", 'style="display:none"')
    return panel_html.replace("%%SECTIONHIDE%%", "")

def tab_bar(tabs):
    '''Returns the tab bar section'''
    tab_bar_html = str(open("www/html/sections/tabbar.html", "r").read())
    return tab_bar_html.replace("%%TABBARITEMS%%", tabs)

def tab_bar_item(plugin_name, active=False):
    '''Returns a tab bar item'''
    tab_bar_item_html = str(open("www/html/sections/tabbaritem.html", "r").read())
    tab_bar_item_html = tab_bar_item_html.replace("%%PLUGINNAME%%", plugin_name)
    tab_bar_item_html = tab_bar_item_html.replace("%%PLUGINNAMECAPITALIZE%%",
                                                  plugin_name.title())
    if active:
        return tab_bar_item_html.replace("%%ACTIVE%%", "active")
    return tab_bar_item_html.replace("%%ACTIVE%%", "")

def tab_pane(plugin_name, plugin_html, active=False):
    '''Returns a tab pane'''
    tab_pane_html = str(open("www/html/sections/tabpane.html", "r").read())
    tab_pane_html = tab_pane_html.replace("%%PLUGINNAME%%", plugin_name)
    tab_pane_html = tab_pane_html.replace("%%PLUGINHTML%%", plugin_html)
    if active:
        return tab_pane_html.replace("%%ACTIVE%%", "active")
    return tab_pane_html.replace("%%ACTIVE%%", "")

########
#INPUTS#
########
def add_instance_button(plugin_name):
    '''returns the add instance button for multi plugins'''
    button_html = str(open("www/html/inputs/addinstancebutton.html", "r").read())
    return button_html.replace("%%PLUGINNAME%%", plugin_name)

def delete_instance_button(plugin_name, name):
    '''returns the add instance button for multi plugins'''
    button_html = str(open("www/html/inputs/deleteinstancebutton.html", "r").read())
    button_html = button_html.replace("%%PLUGINNAME%%", plugin_name)
    return button_html.replace("%%NAME%%", name)

def input_button(value, on_click):
    '''returns a button'''
    button_html = str(open("www/html/inputs/inputbutton.html", "r").read())
    button_html = button_html.replace("%%BUTTONVALUE%%", value)
    return button_html.replace("%%BUTTONONCLICK%%", on_click)

def checkbox(name, variable_name, checkbox_html):
    '''returns the outside tags of the checkbox'''
    checkbox_html = str(open("www/html/inputs/checkbox.html", "r").read())
    checkbox_html = checkbox_html.replace("%%VARIABLENAME%%", variable_name)
    checkbox_html = checkbox_html.replace("%%TITLE%%", name)
    return checkbox_html.replace("%%CHECKBOX%%", checkbox_html)

def checkbox_multi(label, variable_name, value, checked=True, disabled=False, read_only=False,
                   script=None):
    '''returns a multi checkbox'''
    multi_checkbox_html = str(open("www/html/inputs/multicheckbox.html", "r").read())
    if checked:
        checked = "checked"
    else:
        checked = ""
    if disabled:
        disabled = "disabled"
    else:
        disabled = ""
    if read_only:
        read_only = "readonly"
    else:
        read_only = ""
    multi_checkbox_html = multi_checkbox_html.replace("%%CHECKED%%", checked)
    multi_checkbox_html = multi_checkbox_html.replace("%%DISABLED%%", disabled)
    multi_checkbox_html = multi_checkbox_html.replace("%%READONLY%%", read_only)
    if script is None:
        script = "onchange='" + 'Switch("' + variable_name +'");' + "'"
    if script is True:
        script = "onchange='" + 'Switch("' + variable_name +'");'
        script += 'ToggleSection("' + variable_name[:-1] + '");' + "'"
    multi_checkbox_html = multi_checkbox_html.replace("%%SCRIPT%%", script)
    multi_checkbox_html = multi_checkbox_html.replace("%%SWITCH%%", "")
    multi_checkbox_html = multi_checkbox_html.replace("%%VALUE%%", value)
    multi_checkbox_html = multi_checkbox_html.replace("%%LABEL%%", label)
    return multi_checkbox_html.replace("%%VARIABLENAME%%", variable_name)

def checkbox_single(name, variable_name, checked=True, disabled=False, read_only=False,
                    script=None):
    '''returns a single checkbox'''
    single_checkbox_html = str(open("www/html/inputs/singlecheckbox.html", "r").read())
    if checked:
        checked = "checked"
        single_checkbox_html = single_checkbox_html.replace("%%ENABLED%%", "True")
    else:
        checked = ""
        single_checkbox_html = single_checkbox_html.replace("%%ENABLED%%", "False")
    if disabled:
        disabled = "disabled"
    else:
        disabled = ""
    if read_only:
        read_only = "readonly"
    else:
        read_only = ""
    single_checkbox_html = single_checkbox_html.replace("%%CHECKED%%", checked)
    single_checkbox_html = single_checkbox_html.replace("%%DISABLED%%", disabled)
    single_checkbox_html = single_checkbox_html.replace("%%READONLY%%", read_only)
    if script is None:
        script = "onchange='" + 'Switch("' + variable_name + name +'");' + "'"
    if script is True:
        script = "onchange='" + 'Switch("' + variable_name + name +'");'
        script += 'ToggleSection("' + variable_name[:-1] + '");' + "'"
    single_checkbox_html = single_checkbox_html.replace("%%SCRIPT%%", script)
    single_checkbox_html = single_checkbox_html.replace("%%SWITCH%%", "")
    return single_checkbox_html.replace("%%VARIABLENAME%%", variable_name + name)

def checkbox_switch(name, variable_name, checked=True, disabled=False, read_only=False,
                    script=None):
    '''returns a single checkbox'''
    single_checkbox_html = str(open("www/html/inputs/singlecheckbox.html", "r").read())
    switch_html = str(open("www/html/inputs/switchoptions.html", "r").read())
    checkbox_switch_html = single_checkbox_html.replace("%%SWITCH%%", switch_html)
    enabled = str(checked)
    if checked:
        checked = "checked"
    else:
        checked = ""
    if disabled:
        disabled = "disabled"
    else:
        disabled = ""
    if read_only:
        read_only = "readonly"
    else:
        read_only = ""
    checkbox_switch_html = checkbox_switch_html.replace("%%CHECKED%%", checked)
    checkbox_switch_html = checkbox_switch_html.replace("%%ENABLED%%", enabled)
    checkbox_switch_html = checkbox_switch_html.replace("%%DISABLED%%", disabled)
    checkbox_switch_html = checkbox_switch_html.replace("%%READONLY%%", read_only)
    if script is None:
        script = "onchange='" + 'Switch("' + variable_name + name +'");' + "'"
    if script is True:
        script = "onchange='" + 'Switch("' + variable_name + name +'");'
        script += 'ToggleSection("' + variable_name[:-1] + '");' + "'"
    checkbox_switch_html = checkbox_switch_html.replace("%%SCRIPT%%", script)
    checkbox_switch_html = checkbox_switch_html.replace("%%VARIABLENAME%%", variable_name + name)
    return checkbox_switch_html

def hidden_page_index(page_index):
    '''A hidden field for the page index'''
    hidden_html = str(open("www/html/inputs/hiddenpageindex.html", "r").read())
    return hidden_html.replace("%%PAGEINDEX%%", str(page_index))

def input_box(input_type, variable_name, value, script="", max_length=None, minimum=None,
              maximum=None, read_only=False, disabled=False, button=""):
    '''Returns an input object'''
    input_html = str(open("www/html/inputs/input.html", "r").read())
    input_html = input_html.replace("%%INPUTTYPE%%", input_type)
    input_html = input_html.replace("%%VARIABLENAME%%", variable_name)
    input_html = input_html.replace("%%VALUE%%", ' value="' + str(value) + '"')
    if isinstance(script, str):
        input_html = input_html.replace("%%SCRIPT%%", script)
    else:
        input_html = input_html.replace("%%SCRIPT%%", "")
    if isinstance(max_length, int):
        input_html = input_html.replace("%%MAXLENGTH%%", ' maxlength="' + str(max_length) + '"')
    else:
        input_html = input_html.replace("%%MAXLENGTH%%", "")
    if isinstance(minimum, int):
        input_html = input_html.replace("%%MIN%%", ' min="' + str(minimum) + '"')
    else:
        input_html = input_html.replace("%%MIN%%", "")
    if isinstance(maximum, int):
        input_html = input_html.replace("%%MAX%%", ' max="' + str(maximum) + '"')
    else:
        input_html = input_html.replace("%%MAX%%", "")
    if disabled:
        disabled = "disabled"
    else:
        disabled = ""
    input_html = input_html.replace("%%DISABLED%%", disabled)
    if read_only:
        read_only = "readonly"
    else:
        read_only = ""
    input_html = input_html.replace("%%READONLY%%", read_only)
    if button:
        return input_html.replace("%%BUTTON%%", button)
    else:
        return input_html.replace("%%BUTTON%%", "")

def radio_option(variable_name, name, label, checked=False, disabled=False,
                 read_only=False, script=""):
    '''makes a radio option'''
    #%%VARNAME%% %%NAME%% %%CHECKED%% %%DISABLED%% %%READONLY%% %%SCRIPT%%
    radio_html = str(open("www/html/inputs/radio.html", "r").read())
    radio_html = radio_html.replace("%%VARIABLENAME%%", variable_name)
    radio_html = radio_html.replace("%%NAME%%", name)
    radio_html = radio_html.replace("%%LABEL%%", label)
    if checked:
        checked = "checked"
    else:
        checked = ""
    radio_html = radio_html.replace("%%CHECKED%%", checked)
    if disabled:
        disabled = "disabled"
    else:
        disabled = ""
    radio_html = radio_html.replace("%%DISABLED%%", disabled)
    if read_only:
        read_only = "readonly"
    else:
        read_only = ""
    radio_html = radio_html.replace("%%READONLY%%", read_only)
    if isinstance(script, str):
        radio_html = radio_html.replace("%%SCRIPT%%", script)
    else:
        radio_html = radio_html.replace("%%SCRIPT%%", "")
    return radio_html

def select_box_option(name, label, selected=False,
                      disabled=False, read_only=False, script=""):
    '''makes an option for the selection box'''
    option_html = str(open("www/html/inputs/option.html", "r").read())
    if isinstance(name, str) and name is not "":
        option_html = option_html.replace("%%NAME%%", name)
        option_html = option_html.replace("%%NAMECAPITALIZE%%", label)
    else:
        option_html = option_html.replace("%%NAME%%", "")
        option_html = option_html.replace("%%NAMECAPITALIZE%%", " -- select an option -- ")
    if selected:
        selected = "selected"
    else:
        selected = ""
    option_html = option_html.replace("%%SELECTED%%", selected)
    if disabled:
        disabled = "disabled"
    else:
        disabled = ""
    option_html = option_html.replace("%%DISABLED%%", disabled)
    if read_only:
        read_only = "readonly"
    else:
        read_only = ""
    option_html = option_html.replace("%%READONLY%%", read_only)
    if isinstance(script, str):
        option_html = option_html.replace("%%SCRIPT%%", script)
    else:
        option_html = option_html.replace("%%SCRIPT%%", "")
    return option_html

def select_box(variable_name, value, options_html, multiple=False, box_size=0, script="",
               read_only=False, disabled=False):
    '''Makes A select box'''
    select_box_html = str(open("www/html/inputs/selectbox.html", "r").read())
    select_box_html = select_box_html.replace("%%VARIABLENAME%%", variable_name)
    if multiple:
        select_box_html = select_box_html.replace('%%MULTIPLE%%', 'multiple')
    else:
        select_box_html = select_box_html.replace(' %%MULTIPLE%%', '')
    if box_size > 1:
        select_box_html = select_box_html.replace('%%SIZE%%', 'size="' + box_size + '"')
    else:
        select_box_html = select_box_html.replace(' %%SIZE%%', '')
    if disabled:
        disabled = "disabled"
    else:
        disabled = ""
    select_box_html = select_box_html.replace("%%DISABLED%%", disabled)
    if read_only:
        read_only = "readonly"
    else:
        read_only = ""
    select_box_html = select_box_html.replace("%%READONLY%%", read_only)
    if isinstance(script, str):
        select_box_html = select_box_html.replace("%%SCRIPT%%", script)
    else:
        select_box_html = select_box_html.replace("%%SCRIPT%%", "")
    if value is None:
        blank_options_html = select_box_option(False, True, True)
    else:
        blank_options_html = ""
    return select_box_html.replace("%%OPTIONS%%", blank_options_html + options_html)

######
#TAGS#
######

def script_link(location):
    '''returns a script link item'''
    script_link_html = str(open("www/html/tags/scriptlink.html", "r").read())
    return script_link_html.replace("%%LOCATION%%", location)
