'''drives pages'''
import os
import json
import cherrypy
from libs import html_parts
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
    item_html = item_html.replace("%%LABEL%%", label.replace("_", " "))
    item_html = item_html.replace("%%INFO%%", info.replace("_", " "))
    return item_html

def labeler_items(data, baseurl, vertical=False):
    '''returns the group of labeler items html'''
    group_html = str(open(DIR + 'labeler/group.html', "r").read())
    data_html = ""
    for d_item in data:
        data_html += labeler_item(d_item, baseurl, vertical)
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
    for d_item in disc_type.TYPES:
        item_html += labeler_disctype_start_item(d_item, disc_type.TYPES[item], magic)
    return disc_type_html.replace("%%STARTLINKS%%", item_html)

def labeler_disctype_start_item(d_item, icon, magic):
    '''labeler disc type starting section'''
    disc_type_html = get_page("labeler/edit/disctype/startitem")
    disc_type_html = disc_type_html.replace("%%STARTSIZE%%", str(magic))
    disc_type_html = disc_type_html.replace("%%STARTICON%%", icon)
    disc_type_html = disc_type_html.replace("%%STARTTYPE%%", d_item)
    disc_type_html = disc_type_html.replace("%%STARTTYPESAFE%%", d_item.replace(" ", "").lower())
    return disc_type_html

def labeler_disctype_template(label, disc_type_label, rip_data, search=True):
    '''labeler disc type templated section'''
    disc_type_html = get_page("labeler/edit/disctype/template")
    disc_type_html = disc_type_html.replace("%%DISCTYPE%%", disc_type_label)
    disc_type_html = disc_type_html.replace("%%DISCLABEL%%", label)
    disc_type_html = disc_type_html.replace("%%PANEL%%", rip_data.get_edit_panel(search))
    return disc_type_html

def labeler_tracktype_start():
    '''labeler track type starting section'''
    track_type_html = get_page("labeler/edit/tracktype/start")
    magic = 2
    item_html = ""
    for d_item in video_track_type.TYPES:
        item_html += labeler_tracktype_start_item(d_item, video_track_type.TYPES[item], magic)
    return track_type_html.replace("%%STARTLINKS%%", item_html)

def labeler_tracktype_start_item(d_item, icon, magic):
    '''labeler track type starting section'''
    track_type_html = get_page("labeler/edit/tracktype/startitem")
    track_type_html = track_type_html.replace("%%STARTSIZE%%", str(magic))
    track_type_html = track_type_html.replace("%%STARTICON%%", icon)
    track_type_html = track_type_html.replace("%%STARTTYPE%%", d_item)
    return track_type_html

def panel(panel_head, section_name, section_html):
    '''A Panel for track sections'''
    if section_name == "":
        panel_html = get_page("labeler/edit/sectiontype/panel")
    else:
        panel_html = get_page("labeler/edit/tracktype/panel")
    panel_html = panel_html.replace("%%PANELHEAD%%", panel_head)
    if section_name != "":
        panel_html = panel_html.replace("%%SECTIONNAME%%", section_name)
    return panel_html.replace("%%SECTION%%", section_html)

def labeler_tracktype_template(track_index, rip_data):
    '''labeler track type templated section'''
    track_type_html = get_page("labeler/edit/tracktype/template")
    track_type_html = track_type_html.replace("%%TRACKTYPE%%", rip_data.video_type())
    track_type_html = track_type_html.replace("%%PANEL%%", rip_data.get_edit_panel())
    track_type_html = track_type_html.replace("%%TRACKINDEX%%", str(track_index))
    return track_type_html

def stream_panel(ffprobeinfo, options):
    '''panel for the stream info'''
    html = get_page("labeler/edit/tracktype/streampanel")
    html = html.replace("%%FFPROBEINFO%%", _ffprobe_info_panel(ffprobeinfo))
    html = html.replace("%%PANELOPTIONS%%", options)
    return html

def _ffprobe_info_panel(data):
    '''generates the ffprobe info panel for the stream section'''
    html = '<div class="row border mb-2">'
    for key in data:
        html += '<div class="col-sm-4 col-6 border-right font-weight-bold">' + key + '</div>'
        html += '<div class="col-sm-8 col-6">' + str(data[key]) + '</div>'
    html += '</div>'
    return html

def item(variable_name, label, help_text, input_html, not_in_config=False):
    ''' The whole section for each Config Object'''
    html = get_page("labeler/edit/tracktype/item")
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

def converter_item(data):
    '''return html for converter item'''
    item_html = str(open(DIR + 'converter/item.html', "r").read())
    item_html = item_html.replace("%%ITEMID%%", str(data['id']))
    item_html = item_html.replace("%%DISCID%%", str(data['discid']))
    item_html = item_html.replace("%%TRACKID%%", str(data['trackid']))
    item_html = item_html.replace("%%CONVERTING%%", str(data['converting']))
    if data['converting']:
        progress_string = str(data['process']) + "/" + str(data['count'])
        progress_string += "(" + str(data['percent']) + "%)"
        progress_bar = html_parts.progress_bar(progress_string, data['process'], data['count'],
                                               data['percent'])
        item_html = item_html.replace("%%PROGRESS%%", progress_bar)
    else:
        item_html = item_html.replace("%%PROGRESS%%", "")
    return item_html

def converter_items(data):
    '''returns the group of converter items html'''
    group_html = str(open(DIR + 'converter/group.html', "r").read())
    data_html = ""
    for d_item in data:
        data_html += converter_item(d_item)
    return group_html.replace("%%ITEMS%%", data_html)
