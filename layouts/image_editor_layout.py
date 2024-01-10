from tkinter import image_names
import PySimpleGUI as sg
from helper import consts, config_helps
from layouts import common_element_provider
from assets import icons_dark
from data_classes import my_themes


def create_inner_column(component, text):
    btn_text_font = 'ubuntu 10'
    return sg.Column(
        element_justification='c',
        # pad=((4,2),(6,3)),
        size=(100, 60),
        layout=[[component], [sg.Text(text, font=btn_text_font)]]
    )


def create_white_bord_frame(text, value, key, default_value):
    return [sg.Text(text, size=(10, 1)),
            sg.DropDown(values=value, key=key, default_value=default_value, size=(4, 1))],


def image_editing_window():
    frame_pad = (5, 10)
    btn_frame_pad = (0, 10)
    img_btn_pad = (13, 6)
    btn_pad = (10, 8)
    title_color = 'grey'
    text_size = (15, 1)
    inner_colum_pad = ((10, 5), (10, 5))
    bw_text_size = (12, 1)

    default_values = config_helps.get_user_data_from_config_file()
    # sg.theme('my_light1')

    image_view = [
        [
            sg.Frame(
                pad=btn_frame_pad,
                title='',
                expand_y=True,
                expand_x=True,
                layout=[
                    # common_element_provider.graph_header(),
                    [
                        sg.Graph(canvas_size=(720, 720),
                                 graph_bottom_left=(-0, -0),
                                 graph_top_right=(720, 720),
                                 key=consts.key_graph, enable_events=True,
                                 # drag_submits=True,
                                 pad=(0, 0))
                    ],
                ]
            )
        ]

    ]

    button__process_view = [
        [
            sg.Frame(
                element_justification='c',
                pad=btn_frame_pad,
                title='',
                expand_y=True,
                expand_x=True,
                relief='flat',
                layout=[
                    [
                        sg.Frame(
                            pad=btn_frame_pad, title='Current Doc', expand_y=True,
                            expand_x=True, element_justification='c', title_color='grey',
                            layout=[common_element_provider.graph_header(), ]
                        )

                    ],
                    [sg.Frame(
                        title='Rotation', expand_y=True,
                        element_justification='c', title_color=title_color,
                        expand_x=True,
                        layout=[
                            [
                                create_inner_column(sg.Button(image_data=icons_dark.icon_rot_left_90,
                                                              key=consts.key_rot_left_90, ), "Rotate left"),
                                create_inner_column(sg.Button(image_data=icons_dark.icon_rot_right_90,
                                                              key=consts.key_rot_right_90, ), "Rotate Right", )

                            ],

                        ]
                    )],
                    [sg.Frame(
                        title='Cropping',
                        expand_y=True,
                        pad=((5, 5), (10, 10)),
                        element_justification='c',
                        title_color=title_color,
                        expand_x=True,
                        layout=[
                            [create_inner_column(sg.Button(image_data=icons_dark.icon_undo, key=consts.key_crop_undo,
                                                           disabled=True, ), "Undo cropping", ),
                             create_inner_column(sg.Button(image_data=icons_dark.icon_select_point,
                                                           key=consts.key_crop_selct_point,
                                                           ), "Select points")
                             ],
                            [
                                create_inner_column(sg.Button(image_data=icons_dark.icon_crop, key=consts.key_crop_only,
                                                              disabled=True, ), "Just Crop only", ),
                                create_inner_column(sg.Button(image_data=icons_dark.icon_crop, key=consts.key_crop_btn,
                                                              disabled=True, ), "Crop & Process", )

                            ],

                        ]
                    )],

                    [sg.Frame(
                        pad=btn_frame_pad, title='Miscellaneous', expand_y=True,
                        element_justification='c', title_color=title_color,
                        expand_x=True,
                        layout=[

                            [
                                create_inner_column(sg.Image(data=icons_dark.icon_edit, key=consts.key_edit_page_no,
                                                             enable_events=True), 'Edit PageNo'),
                                create_inner_column(
                                    sg.Image(data=icons_dark.icon_crete_pdf, pad=img_btn_pad, enable_events=True,
                                             key=consts.key_create_doc, ), 'Preview PDF')
                            ],
                            [
                                create_inner_column(common_element_provider.del_btn(), 'Delete image'),
                                create_inner_column(sg.Image(data=icons_dark.icon_capture_image,
                                                             enable_events=True, key=consts.key_capture_again),
                                                    'Capture Image')
                            ],
                            [
                                create_inner_column(
                                    sg.Image(data=icons_dark.icon_previous, key=consts.key_pre_doc, enable_events=True),
                                    'Prev Document'),

                                create_inner_column(
                                    sg.Image(data=icons_dark.icon_next, key=consts.key_next_doc, enable_events=True),
                                    'Next Document')

                            ],

                        ]
                    )],
                    [sg.Frame(
                        pad=btn_frame_pad, title='CC Generation', expand_y=True,
                        element_justification='c', title_color=title_color,
                        expand_x=True,
                        layout=[
                            [sg.Button('Generate CC', expand_x=True, key=consts.key_generate_CC,
                                       button_color=consts.popup_back_color)]

                        ]
                    )],
                ]
            )

        ],

    ]
    syntersizer_btn = [
        [
            sg.Frame(
                pad=frame_pad, title='Synthesizing',
                expand_y=True, title_color=title_color,
                expand_x=True, element_justification='left',
                layout=[

                    [sg.Text('Filter Value', size=bw_text_size, pad=frame_pad, ),
                     sg.DropDown(values=[1, 2, 3, 4, 5, 6, 7, 8, 9], default_value=default_values['hvalue'],
                                 readonly=True, key=consts.key_h_value, size=(5, 1), pad=frame_pad, disabled=True), ],

                    [sg.Text('Constant', size=bw_text_size, pad=frame_pad),
                     sg.DropDown(values=[1, 2, 3, 4, 5, 6, 7, 8, 9], default_value=default_values['const'],
                                 readonly=True, key=consts.key_thresh_const, size=(5, 1),
                                 pad=frame_pad, disabled=True), ],

                    [sg.Text('Block Size', size=bw_text_size, pad=frame_pad),
                     sg.DropDown(values=[3, 5, 7, 9, 11, 13, 15, 17, 19], default_value=default_values['block'],
                                 size=(5, 1), pad=frame_pad,
                                 readonly=True, key=consts.key_thresh_block, disabled=True)],

                    [sg.Text('Template Size.', size=bw_text_size,
                             pad=frame_pad),
                     sg.DropDown(values=[3, 5, 7, 9, 11, 13, 15, 17, 19, 21],
                                 default_value=default_values['twind'],
                                 readonly=True,
                                 key=consts.key_thresh_Templ_wind, size=(5, 1),
                                 pad=frame_pad, disabled=True)],

                    [sg.Text('Search Size.', size=bw_text_size, pad=frame_pad),
                     sg.DropDown(values=[7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39],
                                 default_value=default_values['swind'], disabled=True,
                                 size=(5, 1), readonly=True, pad=frame_pad,
                                 key=consts.key_thresh_search_wind)],

                    # Daptive threshoding
                    [sg.Button('B&W-INV-1', expand_x=True, key=consts.key_thresh_meanc_inv, pad=frame_pad,
                               disabled=True, size=(9,1)),
                     sg.Button('B&W-1', expand_x=True, key=consts.key_thresh_meanc, pad=frame_pad,
                               disabled=True, size=(9,1))],

                    # gausien thresholding
                    [sg.Button('B&W-INV-2', expand_x=True, key=consts.key_thresh_gauss_inv, pad=frame_pad,
                               disabled=True,  size=(9,1)),
                     sg.Button('B&W-1', expand_x=True, key=consts.key_thresh_gauss, pad=frame_pad,
                               disabled=True,  size=(9,1))],

                    [sg.Frame(
                        pad=btn_frame_pad, title='Brightness', expand_y=True,
                        expand_x=True, title_color=title_color,element_justification='c',
                        layout=[
                            [sg.Slider(range=(1, 100), orientation='h', key=consts.key_bright_control,
                                       enable_events=True, disabled=True,
                                       relief='raised', tooltip='Brightness')],

                        ]
                    ), ],
                    [sg.Frame(
                        pad=btn_frame_pad, title='Contrast', expand_y=True,
                        expand_x=True, title_color=title_color,element_justification='c',
                        layout=[
                            [sg.Slider(range=(1, 100), orientation='h', key=consts.key_contrast_control,
                                       enable_events=True, disabled=True,
                                       tooltip='Contrast')],

                        ]
                    )],
                    [
                        sg.Frame(
                            pad=btn_frame_pad, title='Saving', expand_y=True,
                            expand_x=True, element_justification='c', title_color=title_color,
                            layout=[
                                [
                                    create_inner_column(sg.Button(image_data=icons_dark.icon_save_all,
                                                                  key=consts.key_save_all_processed_img, disabled=True,
                                                                  enable_events=True,
                                                                  pad=img_btn_pad, ), 'Save All'),

                                    create_inner_column(sg.Button(image_data=icons_dark.icon_save,
                                                                  key=consts.key_save_processed_img, pad=img_btn_pad,
                                                                  disabled=True), 'Save Image'),

                                ],

                            ]
                        ),
                    ],
                    [
                        sg.Frame(
                            pad=btn_frame_pad, title='Original Image', expand_y=True,
                            expand_x=True, element_justification='c', title_color=title_color,
                            layout=[

                                [sg.Button('Get Original image', expand_x=True, button_color='red',
                                           key=consts.key_View_original_img, pad=btn_pad, ), ]

                            ]
                        ),
                    ]

                ]

            ),

        ]
    ]

    graph_only_layout = [
        # [sg.Image(data=icons_dark.icon_close_edit, key=consts.key_img_edit_win_close, enable_events=True)],
        [
            sg.Frame(

                pad=(0, 0),
                title='',
                expand_y=True,
                expand_x=True,
                title_color=title_color,
                layout=[

                    [

                        sg.Column(button__process_view, size=(240, 740), element_justification='center', ),
                        sg.Column([[common_element_provider.previous_btn()]], size=(30, 30),
                                  element_justification='bottom', ),
                        sg.Column(image_view, size=(730, 740), element_justification='center', ),
                        sg.Column([[common_element_provider.next_btn()]], size=(30, 30),
                                  element_justification='bottom', ),
                        # sg.Column(img_list_col, element_justification='center', expand_x=True, expand_y=True)
                        sg.Column(syntersizer_btn, size=(250, 740), element_justification='center', )
                    ],

                ]
            ),
            # Close button Implementation
            # sg.Column(
            #
            #     [
            #         [
            #             sg.Image(data=icons_dark.icon_close_edit, key=consts.key_img_edit_win_close, enable_events=True)
            #         ]
            #     ],
            #     vertical_alignment='top'
            # )
        ],
    ]

    return sg.Window("Edit Your Image",
                     graph_only_layout,
                     relative_location=(0, 0),
                     disable_close=False,
                     element_justification='right',
                     modal=True,
                     finalize=True,
                     icon=icons_dark.main_icon,
                     resizable=False,
                     # grab_anywhere=True,
                     # element_justification='left',
                     # disable_close=False,
                     # disable_minimize=True,
                     # no_titlebar=True,
                     # keep_on_top=True,
                     # grab_anywhere=True,
                     # force_toplevel=True,
                     # disable_minimize=True,
                     # resizable=False,
                     # grab_anywhere=True,
                     # location=(10, 10),
                     )
