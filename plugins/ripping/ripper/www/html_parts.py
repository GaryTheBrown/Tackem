'''drives pages'''
import os

DIR = os.path.dirname(__file__) + "/html/"

def get_page(page, navbar_show=True):
    '''opens an page and returns it with the navbar sorted'''
    page_html = str(open(DIR + page + ".html", "r").read())
    if navbar_show:
        return page_html.replace("%%NAVBAR%%", navbar())
    return page_html

def navbar():
    '''creates the navbar section'''
    navbar_html = str(open(DIR + "navbar.html", "r").read())

    return navbar_html

def drive(drive_obj, drive_index, name, vertical=False):
    '''return html for Drive'''
    if vertical:
        drive_html = str(open(DIR + 'drivevertical.html', "r").read())
    else:
        drive_html = str(open(DIR + 'drive.html', "r").read())
    data = drive_obj.html_data(False)
    locked_html = ""
    if not data["traylock"]:
        locked_html = 'style="display:none"'
    name_html = ""
    if name != "":
        name_html += name + " ("
    name_html += drive_obj.get_device()
    if name != "":
        name_html += ")"
    drive_html = drive_html.replace("%%DRIVENUMBER%%", str(drive_index))
    drive_html = drive_html.replace("%%IMAGE%%", data["traystatus"])
    drive_html = drive_html.replace("%%LOCKED%%", locked_html)
    drive_html = drive_html.replace("%%NAME%%", name_html)
    drive_html = drive_html.replace("%%INFO%%", data["drivestatus"])
    return drive_html

def drives(drive_list, config_drives, vertical=False):
    '''returns the group of drives html'''
    drives_html = ""
    for drive_index, drive_obj in enumerate(drive_list):
        cfg_name = drive_obj.get_cfg_name()
        drives_html += drive(drive_obj, drive_index, config_drives[cfg_name]['name'], vertical)
    return drives_html
