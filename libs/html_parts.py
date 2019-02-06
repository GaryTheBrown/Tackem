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
    '''A Navber Item (not active)'''
    html = str(open("www/html/navbar/dropdown.html", "r").read())
    html = html.replace("%%TITLE%%", title.title())
    html = html.replace("%%DROPDOWNID%%", dropdown_id)
    return html.replace("%%ITEMS%%", items)

def navbar_dropdown_right(title, dropdown_id, items):
    '''A Navber Item (not active)'''
    html = str(open("www/html/navbar/dropdownright.html", "r").read())
    html = html.replace("%%TITLE%%", title.title())
    html = html.replace("%%DROPDOWNID%%", dropdown_id)
    return html.replace("%%ITEMS%%", items)

def navbar_item(title, url):
    '''A Navber Item (not active)'''
    html = str(open("www/html/navbar/item.html", "r").read())
    html = html.replace("%%TITLE%%", title.title())
    return html.replace("%%URL%%", url.replace(" ", "/"))

def navbar_item_active(title):
    '''A Navber Item (not active)'''
    html = str(open("www/html/navbar/itemactive.html", "r").read())
    return html.replace("%%TITLE%%", title.title())

def navbar_master(nav_bar_items):
    '''master file for the navbar'''
    html = str(open("www/html/navbar/master.html", "r").read())
    return html.replace("%%NAVBARITEMS%%", nav_bar_items)

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
    if label != "":
        html = html.replace("%%LABEL%%", label)
    else:
        html = html.replace("%%LABEL%%:", "")
    if isinstance(help_text, str):
        html = html.replace("%%HELP%%", help_text)
    else:
        html = html.replace("%%HELP%%", '')
    html = html.replace("%%INPUT%%", input_html)
    if not_in_config:
        html = html.replace("cs_", "")
    return html

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

def multi_panel(variable_name, name, enable_option, delete_option, section_html, section_visible):
    '''Returns a panel for multi type plugin data'''
    html = str(open("www/html/sections/multi_panel.html", "r").read())
    html = html.replace("%%VARIABLENAME%%", variable_name)
    html = html.replace("%%NAME%%", name)
    html = html.replace("%%ENABLEDOPTION%%", enable_option)
    html = html.replace("%%DELETEOPTION%%", delete_option)
    html = html.replace("%%SECTION%%", section_html)
    if not section_visible:
        return html.replace("%%SECTIONHIDE%%", 'style="display:none"')
    return html.replace("%%SECTIONHIDE%%", "")

def panel(title, control, modal, variable_name, section_html, section_visible):
    '''A Panel for plugins or sections'''
    html = str(open("www/html/sections/panel.html", "r").read())
    html = html.replace("%%TITLE%%", title)
    if control == "":
        html = html.replace("<div>%%CONTROL%%</div>", "")
    else:
        html = html.replace("%%CONTROL%%", control)
    html = html.replace("%%MODAL%%", modal)
    if variable_name == "":
        html = html.replace('id="%%VARIABLENAME%%_section"', variable_name)
    else:
        html = html.replace("%%VARIABLENAME%%", variable_name)
    html = html.replace("%%SECTION%%", section_html)
    if not section_visible:
        return html.replace("%%SECTIONHIDE%%", 'style="display:none"')
    return html.replace("%%SECTIONHIDE%%", "")

def search_modal():
    '''Returnas a modal for adding a multi plugin'''
    return str(open("www/html/sections/search_modal.html", "r").read())

def section(section_name, section_html, section_visible):
    '''A Panel for plugins or sections'''
    html = str(open("www/html/sections/section.html", "r").read())
    html = html.replace("%%SECTIONNAME%%", section_name)
    html = html.replace("%%SECTION%%", section_html)
    if not section_visible:
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

def input_button(value, on_click):
    '''returns a button'''
    html = str(open("www/html/inputs/inputbutton.html", "r").read())
    html = html.replace("%%BUTTONVALUE%%", value)
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
    if disabled:
        disabled = "disabled"
    else:
        disabled = ""
    if read_only:
        read_only = "readonly"
    else:
        read_only = ""
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
    if isinstance(script, str):
        html = html.replace("%%SCRIPT%%", script)
    else:
        html = html.replace("%%SCRIPT%%", "")
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
    if disabled:
        disabled = "disabled"
    else:
        disabled = ""
    html = html.replace("%%DISABLED%%", disabled)
    if read_only:
        read_only = "readonly"
    else:
        read_only = ""
    html = html.replace("%%READONLY%%", read_only)
    if button:
        return html.replace("%%BUTTON%%", button)
    else:
        return html.replace("%%BUTTON%%", "")

def radio_option(variable_name, name, label, checked=False, disabled=False,
                 read_only=False, script=""):
    '''makes a radio option'''
    #%%VARNAME%% %%NAME%% %%CHECKED%% %%DISABLED%% %%READONLY%% %%SCRIPT%%
    html = str(open("www/html/inputs/radio.html", "r").read())
    html = html.replace("%%VARIABLENAME%%", variable_name)
    html = html.replace("%%NAME%%", name)
    html = html.replace("%%LABEL%%", label)
    if checked:
        checked = "checked"
    else:
        checked = ""
    html = html.replace("%%CHECKED%%", checked)
    if disabled:
        disabled = "disabled"
    else:
        disabled = ""
    html = html.replace("%%DISABLED%%", disabled)
    if read_only:
        read_only = "readonly"
    else:
        read_only = ""
    html = html.replace("%%READONLY%%", read_only)
    if isinstance(script, str):
        html = html.replace("%%SCRIPT%%", script)
    else:
        html = html.replace("%%SCRIPT%%", "")
    return html

def select_box_option(name, label, selected=False,
                      disabled=False, read_only=False, script=""):
    '''makes an option for the selection box'''
    html = str(open("www/html/inputs/option.html", "r").read())
    if isinstance(name, str) and name is not "":
        html = html.replace("%%NAME%%", name)
        html = html.replace("%%NAMECAPITALIZE%%", label)
    else:
        html = html.replace("%%NAME%%", "")
        html = html.replace("%%NAMECAPITALIZE%%", " -- select an option -- ")
    if selected:
        selected = "selected"
    else:
        selected = ""
    html = html.replace("%%SELECTED%%", selected)
    if disabled:
        disabled = "disabled"
    else:
        disabled = ""
    html = html.replace("%%DISABLED%%", disabled)
    if read_only:
        read_only = "readonly"
    else:
        read_only = ""
    html = html.replace("%%READONLY%%", read_only)
    if isinstance(script, str):
        html = html.replace("%%SCRIPT%%", script)
    else:
        html = html.replace("%%SCRIPT%%", "")
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
    if disabled:
        disabled = "disabled"
    else:
        disabled = ""
    html = html.replace("%%DISABLED%%", disabled)
    if read_only:
        read_only = "readonly"
    else:
        read_only = ""
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
    else:
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
