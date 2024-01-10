import PySimpleGUI as sg
from helper import consts
from assets import icons_dark


def create_main_win():
    col_1 = [[]]

    col_2 = [
        [sg.Image(data=icons_dark.default_img, key=consts.key_video_view_disply, expand_x=True, expand_y=True, )],
    ]

    col_3 = [[]]

    return [
        sg.Menu(
            menu_definition=[
                ['View' , [consts.key_menu_view_docs, consts.key_menu_view_generated_doc]],
                ['Add Document',[ consts.key_menu_read_file]],
                # ['Print CC'],
                ['About', [consts.key_menu_about]],

            ]
        ),

        sg.Frame(
            relief=consts.frame_relief_main,
            font=consts.heading_fonts,
            border_width=consts.frame_border_main_wind_size,
            title='Documents',
            expand_x=True,
            expand_y=True,
            layout=[
                [sg.Column(col_1, expand_y=True,
                           size=consts.side_col_size, expand_x=True,
                           element_justification='center',
                           scrollable=True,
                           vertical_scroll_only=True,
                           key=consts.key_col_add_doc), ],
                [sg.Button('Add Document', key=consts.key_btn_add_doc, expand_x=True,
                           font=consts.heading_fonts, ), ]
            ]
        ),

        sg.Frame(
            relief=consts.frame_relief_main,
            border_width=consts.frame_border_main_wind_size,
            font=consts.heading_fonts,
            title='Camera ',
            expand_x=True,
            expand_y=True,
            element_justification='c',
            layout=[
                [
                    sg.Text(' Current Document : ', font=consts.heading_fonts),
                    sg.Text(text='', font=consts.heading_fonts_LARGE, key=consts.key_disply_selected_doc, size=(13, 1),
                            text_color='white'),

                ],
                [
                    sg.Column(col_2, expand_y=True, expand_x=True, element_justification='c',
                              size=(consts.center_column_width, 1), key=consts.key_col_camera),
                ],
                [
                    sg.Button('Preview', key=consts.key_preview, expand_x=True,
                              font=consts.heading_fonts,disabled_button_color='red' ),

                    sg.Button(button_text='Capture Image', expand_x=True, key=consts.key_capture_image,
                              font=consts.heading_fonts, ),

                ]
            ]
        ),
        sg.Frame(
            relief=consts.frame_relief_main,
            border_width=consts.frame_border_main_wind_size,
            font=consts.heading_fonts,
            title='Images',
            expand_x=True,
            expand_y=True,
            layout=[
                [
                    sg.Column(col_3, expand_y=True, size=consts.side_col_size, expand_x=True,

                              scrollable=True, vertical_scroll_only=True, key=consts.key_col3_raw_img_thump_col, ),
                ], [
                    sg.Button('Save All',
                              font=consts.heading_fonts, expand_x=True, key=consts.key_save_all_raw_img_btn,
                              disabled=True)
                ]
            ]
        ),

    ]


def main_window():
    layout = [
        create_main_win(),
    ]
    return sg.Window('CCMS', layout, resizable=True, margins=(0, 20),
                     # background_color='white',
                     relative_location=(0, 0),
                     # size=(consts.screen_width, consts.screen_height),
                     # size=(500, 500),

                     icon=icons_dark.main_icon,
                     titlebar_icon=icons_dark.main_icon,
                     finalize=True)
