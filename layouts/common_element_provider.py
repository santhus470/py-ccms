import PySimpleGUI as sg
from helper import consts
from assets import icons_dark

def next_btn():
    return  sg.Image(data=icons_dark.icon_next, key=consts.key_img_view_next, enable_events=True)

def previous_btn():
    return  sg.Image(data=icons_dark.icon_previous, key=consts.key_img_view_prev, enable_events=True)

def del_btn():
    return sg.Image(data=icons_dark.icon_del_red, key=consts.key_img_view_del, enable_events=True)

def graph_header():
    return [sg.Text(text='',  key=consts.key_graph_header,)]



