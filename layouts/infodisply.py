

import PySimpleGUI as sg
from helper import consts
from assets import icons_dark


def create():
    layout = [

        [
            sg.Image(data=icons_dark.default_img)
        ],


    ]
    return sg.Window("Add Documents", layout, use_default_focus=False,
                     background_color=consts.theme_light_2,
                     finalize=True, modal=True, force_toplevel=True, no_titlebar=True,
                     keep_on_top=True,
                     )
