import PySimpleGUI as sg
from helper import consts
from layouts import common_element_provider
from assets import icons_dark


def create_img_view_window():
    # sg.theme('my_light2')

    layout = [
        #close button implementation
        # [sg.Image(data=icons_dark.icon_close_view, tooltip='close', enable_events=True,
        #           key=consts.key_img_view_win_close, ), ],
        [
            sg.Frame(
                title='Edit Page Number',
                element_justification='c',
                size=(250, 730),
                layout=[
                    [sg.Column([[]], expand_y=True,
                               size=(250, 630), expand_x=True,
                               element_justification='center',
                               scrollable=True,
                               vertical_scroll_only=True,
                               key=consts.key_page_editlist_col), ],

                    [common_element_provider.del_btn(),
                     sg.Button(image_data=icons_dark.icon_save,
                               key=consts.key_save_page_no,
                               enable_events=True,
                               tooltip=' Save Page Number ', expand_x=True), ],
                    [sg.Button(' Sort-LRLR ', key=consts.key_page_edit_lrlr, expand_x=True, expand_y=True),
                     sg.Button(' Sort-LRRL ', key=consts.key_page_edit_lrrl, expand_x=True, expand_y=True,
                               disabled=True
                               ), ]
                ]
            ),
            sg.Frame(
                title='',
                element_justification='c',
                size=(850, 730),
                layout=[
                    common_element_provider.graph_header(),

                    [

                        common_element_provider.previous_btn(),
                        sg.Graph(canvas_size=(720, 720),
                                 graph_bottom_left=(-0, -0),
                                 graph_top_right=(720, 720),
                                 key=consts.key_img_view_graph, enable_events=False,
                                 pad=(0, 0)
                                 ),
                        common_element_provider.next_btn()
                    ],

                ]
            )
        ],
        [

        ]
    ]

    return sg.Window("View You Image",
                     layout,
                     # # location=(10, 10),
                     modal=True,
                     element_justification='right',
                     # disable_close=True,
                     # disable_minimize=True,
                     resizable=False,
                     grab_anywhere=True,
                     # force_toplevel=True,
                     finalize=True,

                     # no_titlebar=True,

                     )

# create_img_view_window()
