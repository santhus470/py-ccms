import PySimpleGUI as sg
from helper import consts
from assets import icons_dark


def url_link_text(text, url):
    return [sg.Text(text=text, pad=((20, 5), (5, 5)), size=(20, 1)),
            sg.Text(text=url, text_color='light green', pad=((20, 5), (5, 5)), enable_events=True, key=url)]


def create_about_win():
    head_text = 'Certified copy Management system'
    text_short = 'CCMS'

    layout = [
        [sg.Text(text=text_short, font='courier  14 bold')],
        [sg.Text(text=head_text, font='courier  14 bold')],
        [sg.Frame(
            title='Libraries / Utilities Used ', size=(500, 280),
            element_justification='left', title_color='grey',
            expand_x=True,
            pad=(10, 10),
            layout=[
                url_link_text('PysimpleGui 4.60.1', consts.url_sg),
                url_link_text('OpenCV 4.5.5.64', consts.url_cv),
                url_link_text('winapps 0.2.0', consts.url_winapp),
                url_link_text('imutils 0.5.4', consts.url_mutils),
                url_link_text('Pillow 9.2.0', consts.url_pillow),
                url_link_text('PyPDF2  2.10.3 ', consts.url_pdf),
                url_link_text('digicamcontroller 2.0.0', consts.url_digicam),

            ]
        )],
        [
            sg.Frame(
                title='Design and development ', size=(500, 180),
                element_justification='c', title_color='grey',
                expand_x=True,
                vertical_alignment='center',
                pad=(10, 10),
                layout=[
                    [sg.Text(text='State IT Cell ', font='courier 12')],
                    [sg.Text(text='Registration Department Kerala', font='courier 13')],
                    [sg.Image(data=icons_dark.ico_call), sg.Image(data=icons_dark.icon_msg),
                     sg.Text(text='8547344357 ', key=consts.url_watsaspp, font='courier 12',
                             enable_events=True,text_color='light green')],
                    [sg.Image(data=icons_dark.icon_mail),
                     sg.Text(text='itcell.regn@kerala.gov.in ', font='courier 12')],
                    [sg.Image(data=icons_dark.icon_web),
                     sg.Text(text=consts.url_pearl, enable_events=True, key=consts.url_pearl, text_color='light green',
                             font='courier 12')],

                ]
            )
        ],
        [
            sg.Frame(
                title='System Requirements', size=(500, 120),
                element_justification='c', title_color='grey',
                expand_x=True,
                vertical_alignment='center',
                # pad=(10, 10),
                layout=[
                    [sg.Text(text='Windows 7 Service Pack 1 or above', font='courier 12')],
                    [sg.Text(text='python3.8', font='courier 12')],
                    [sg.Text(text='Digicamcontroller2.0.0.0', font='courier 12')],

                ]
            )
        ],
        # [sg.Button('close', key=consts.key_about_close, size=(10,2))]
    ]

    return sg.Window('About', layout, use_default_focus=False,
                     element_justification='c', border_depth=3,
                     finalize=True, modal=True,
                     force_toplevel=True,
                     keep_on_top=True,
                     # size=(600, 700),
                     element_padding=2,
                     # no_titlebar=True,
                     resizable=False,
                     icon=icons_dark.main_icon,
                     grab_anywhere=True
                     )
