'''drives pages'''
import os
import json
import cherrypy
from ..data import disc_type, video_track_type
DIR = os.path.dirname(__file__) + "/html/"

def get_page(page, system=None):
    '''opens an page and returns it with the navbar sorted'''
    page_html = str(open(DIR + page + ".html", "r").read())
    if system:
        return page_html.replace("%%NAVBAR%%", navbar(system))
    return page_html

def navbar(system):
    '''creates the navbar section'''
    navbar_html = str(open(DIR + "navbar.html", "r").read())
    labeler_count = system.get_labeler().get_count("WWW" + cherrypy.request.remote.ip)
    if labeler_count > 0:
        navbar_html = navbar_html.replace("%%LABLERCOUNT%%", str(labeler_count))
    else:
        navbar_html = navbar_html.replace(" (%%LABLERCOUNT%%)", "")
    return navbar_html

def drive(drive_obj, drive_index, name, vertical=False):
    '''return html for Drive'''
    if vertical:
        drive_html = str(open(DIR + 'drives/itemvertical.html', "r").read())
    else:
        drive_html = str(open(DIR + 'drives/item.html', "r").read())
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

def labeler_item(data, baseurl, vertical=False):
    '''return html for labeler item'''
    if vertical:
        item_html = str(open(DIR + 'labeler/itemvertical.html', "r").read())
    else:
        item_html = str(open(DIR + 'labeler/item.html', "r").read())

    disc_type_img = baseurl + "ripping/ripper/static/images/" + data['disc_type'] + "-video.png"
    if data['rip_data'] is None:
        info = "NEW"
        label = data['label']
    else:
        rip_data = disc_type.make_disc_type(json.loads(data['rip_data']))
        info = rip_data.info()
        label = rip_data.name()
    item_html = item_html.replace("%%ITEMID%%", str(data['id']))
    item_html = item_html.replace("%%IMAGE%%", disc_type_img)
    item_html = item_html.replace("%%LABEL%%", label)
    item_html = item_html.replace("%%INFO%%", info)
    return item_html

def labeler_items(data, baseurl, vertical=False):
    '''returns the group of labeler items html'''
    group_html = str(open(DIR + 'labeler/group.html', "r").read())
    data_html = ""
    for item in data:
        data_html += labeler_item(item, baseurl, vertical)
    if vertical:
        group_html = group_html.replace("%%LAYOUT%%", "true/")
    else:
        group_html = group_html.replace("%%LAYOUT%%", "")
    return group_html.replace("%%ITEMS%%", data_html)

def labeler_disctype_start():
    '''labeler disc type starting section'''
    disc_type_html = get_page("labeler/edit/disctype/start")
    magic = 3
    item_html = ""
    for item in disc_type.TYPES:
        item_html += labeler_disctype_start_item(item, disc_type.TYPES[item], magic)
    return disc_type_html.replace("%%STARTLINKS%%", item_html)

def labeler_disctype_start_item(item, icon, magic):
    '''labeler disc type starting section'''
    disc_type_html = get_page("labeler/edit/disctype/startitem")
    disc_type_html = disc_type_html.replace("%%STARTSIZE%%", str(magic))
    disc_type_html = disc_type_html.replace("%%STARTICON%%", icon)
    disc_type_html = disc_type_html.replace("%%STARTTYPE%%", item)
    return disc_type_html

def labeler_disctype_template(label, disc_type_label, rip_data):
    '''labeler disc type templated section'''
    disc_type_html = get_page("labeler/edit/disctype/template")
    disc_type_html = disc_type_html.replace("%%DISCTYPE%%", disc_type_label)
    disc_type_html = disc_type_html.replace("%%DISCLABEL%%", label)
    disc_type_html = disc_type_html.replace("%%PANEL%%", rip_data.get_edit_panel())
    return disc_type_html

def labeler_tracktype_start():
    '''labeler track type starting section'''
    track_type_html = get_page("labeler/edit/tracktype/start")
    magic = 2
    item_html = ""
    for item in video_track_type.TYPES:
        item_html += labeler_tracktype_start_item(item, video_track_type.TYPES[item], magic)
    return track_type_html.replace("%%STARTLINKS%%", item_html)

def labeler_tracktype_start_item(item, icon, magic):
    '''labeler track type starting section'''
    track_type_html = get_page("labeler/edit/tracktype/startitem")
    track_type_html = track_type_html.replace("%%STARTSIZE%%", str(magic))
    track_type_html = track_type_html.replace("%%STARTICON%%", icon)
    track_type_html = track_type_html.replace("%%STARTTYPE%%", item)
    return track_type_html

def panel(panel_head, section_name, section_html):
    '''A Panel for track sections'''
    panel_html = get_page("labeler/edit/tracktype/panel")
    panel_html = panel_html.replace("%%PANELHEAD%%", panel_head)
    panel_html = panel_html.replace("%%SECTIONNAME%%", section_name)
    return panel_html.replace("%%SECTION%%", section_html)

def labeler_tracktype_template(track_index, rip_data):
    '''labeler track type templated section'''
    track_type_html = get_page("labeler/edit/tracktype/template")
    ##TODO Make this line look better
    track_type_html = track_type_html.replace("%%TRACKTYPE%%", rip_data.video_type())
    ##TODO Make this line look better 
    track_type_html = track_type_html.replace("%%PANEL%%", rip_data.get_edit_panel())
    track_type_html = track_type_html.replace("%%TRACKINDEX%%", str(track_index))
    return track_type_html
