import PySimpleGUI as sg
from helper import consts

def create_file_browse_win():
    layout = [
        [sg.Text('Please selct a  file to read the document Number ', background_color=consts.theme_light_2,)],
        [sg.Text('File path ',size=(7,1), pad=(20,30), background_color=consts.theme_light_2,),
         sg.Input(key=consts.key_file_path),
         sg.FileBrowse()
         ],
        [ sg.Button('Cancel'),sg.Button('Read', key=consts.key_read_file_browse)]

    ]

    return sg.Window("browse file",
                     layout, use_default_focus=False,
                     background_color=consts.theme_light_2,
                     finalize=True, modal=True, force_toplevel=True, no_titlebar=True,
                     keep_on_top=True, size=(750, 300), margins=(30, 10), element_padding=10, )

