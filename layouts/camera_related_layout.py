import PySimpleGUI as sg

from helper import consts

camera_dict = {'video0': 0, 'video1': 1, 'video2': 2, 'video3': 3}


def create_cam_select_win(cam_list):

    layout = [
        [sg.Text('Select the Camera', font=consts.normal_font,background_color = consts.theme_light_2,)],
        [sg.Text('Camera', background_color = consts.theme_light_2,),
         sg.DropDown(values=cam_list, size=(50, 1), default_value=cam_list[0], key=consts.key_availabele_camera,
                     readonly=True)],
        [sg.Button(button_text='Ok', enable_events=True, key=consts.key_camera_select_ok),
         sg.Cancel('Cancel')]
    ]

    return sg.Window('Camera Selector', layout, use_default_focus=False,
                     element_justification='c',
                     background_color = consts.theme_light_2,
                     finalize=True, modal=True, force_toplevel=True, no_titlebar=True,
                     keep_on_top=True, size=(300, 150), margins=(10, 10), element_padding=10, )


def camera_start_info_win():
    layout = [

        [
         sg.Text('Starting the camera. Please wait .....!', text_color='White', background_color='red',
                 font=consts.heading_fonts)],

    ]

    return sg.Window('Camera Selector', layout, use_default_focus=False,

                     element_justification='c',border_depth=3,
                     background_color='red',
                     finalize=True, modal=True, force_toplevel=True, no_titlebar=True,
                     keep_on_top=True, size=(400, 70), element_padding=10, )

# create_cam_select_win(camera_dict)
