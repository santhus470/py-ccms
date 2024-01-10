import PySimpleGUI as sg
from helper import consts
from assets import icons_dark


def create_menu_doc_view_win():
    text_color = 'grey'
    size = (12, 1)
    col1 = [
        [
            sg.Text('Document No.', text_color=text_color, size=size),
            sg.Text('Volume No', text_color=text_color, size=size),
            sg.Text('Total Pages', text_color=text_color, size=size),
            # sg.Text('Captured', text_color=text_color, size=(8, 1)),
            # sg.Text('Processed', text_color=text_color, size=(10, 1)),
            # sg.Text('Pdf', text_color=text_color, size=size),
            sg.Text('Current Status', text_color=text_color, size=size),
            sg.Text('Delete document', text_color=text_color, size=size),

        ],
        [sg.HorizontalSeparator(pad=((0, 0), (5, 5)), color=text_color)]
    ]
    layout1 = [
        [sg.Column(
            [
                [sg.Image(data=icons_dark.icon_close_red_small, key=consts.key_menu_all_doc_win_close,
                          enable_events=True, tooltip=' Close ', pad=(10, 5))],
            ],
            element_justification='right', expand_x=True, background_color=consts.theme_light1,
        )],
        [sg.Frame(
            font=consts.heading_fonts,
            border_width=consts.frame_border_main_wind_size,
            title='',
            element_justification='c',
            size=(650, 600),
            layout=[
                [sg.Column(col1, expand_y=True,
                           size=(6650, 600), expand_x=True,
                           element_justification='center',
                           scrollable=True,
                           vertical_scroll_only=True,
                           key=consts.key_menu_column
                           ), ],

            ],

        ), ],
        [sg.Text('The List of document currently in process ', text_color=text_color,
                 background_color=consts.theme_light1, ), ]
    ]

    return sg.Window('CCMS', layout1, resizable=True, margins=(0, 10),
                     relative_location=(0, 0),
                     size=(690, 700),
                     icon=icons_dark.main_icon,
                     element_justification='center',
                     background_color=consts.theme_light1,
                     force_toplevel=True,
                     modal=True,
                     no_titlebar=True,
                     scaling=True,
                     finalize=True)


def create_generated_document_window(data):
    heading = ['Sl No', 'Document No', ' Generated Date & time']
    table_layout = [
        [sg.Image(data=icons_dark.icon_close_red_small, key=consts.key_menu_gerated_doc_win_close,
                  enable_events=True, tooltip=' Close ', pad=(15, 5))],

        [
            sg.Table(
                values=data, headings=heading,
                alternating_row_color='black',
                hide_vertical_scroll=True,
                # display_row_numbers=True,
                max_col_width=25,
                vertical_scroll_only=True,
                num_rows=20,
                row_height=30,
                justification='left',
                pad=(20, 2),
            )
        ],
        [sg.Text('The List of generated document ',
                 background_color=consts.theme_light1, text_color='grey', pad=(18, 0)), ],

    ]

    return sg.Window('CCMS', table_layout, resizable=True, margins=(0, 10),
                     relative_location=(0, 0),
                     size=(450, 700),
                     icon=icons_dark.main_icon,
                     element_justification='right',
                     background_color=consts.theme_light1,
                     force_toplevel=True,
                     grab_anywhere=True,
                     modal=True,
                     no_titlebar=True,
                     finalize=True)

