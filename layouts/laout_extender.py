import os
import PySimpleGUI as sg
import cv2
from layouts import common_element_provider
from helper import consts, image_processor
from assets import icons_dark


def add_img_list_to_col3(key, page_no) -> object:
    layout = [
        [
            sg.Frame(
                pad=(0, 8),
                title='',
                expand_x=True,
                # this key is used to hide the row from the column3
                background_color=consts.theme_dark_color,
                relief=consts.frame_relief_main,
                key=consts.key_raw_img_thump_holder_frame_offset + key,
                layout=

                [[
                    sg.Image(data=icons_dark.doc_icon, key=key, enable_events=True, tooltip=' view image ', pad=(0, 5)),
                    sg.Text(f'Page   {page_no}', size=(10, 1), background_color=consts.theme_dark_color, ),
                    sg.Image(data=icons_dark.icon_del_red, key=consts.key_delete_thump_offset+key, enable_events=True)
                    # common_element_provider.del_btn(),

                ]]

            )
        ],
    ]

    return layout


def doc_disply_layout(doc_no, color='white'):
    return sg.Text(doc_no, key=doc_no, pad=(2, 0), text_color=color,
                   enable_events=True, font=consts.normal_font,
                   size=(12, 1))


def add_doc_colum1(doc_no, vol=''):
    layout = [
        [
            sg.Frame(
                relief=consts.frame_relief_main,
                pad=(0, 8),
                title='',
                expand_x=True,
                # used to get the frame to remove when the img capturing completed
                key=consts.key_doc_number_holder_frame_offset + doc_no,
                layout=

                [
                    [doc_disply_layout(doc_no), ],
                    [sg.Text('Volume:'), sg.Text(vol, size=(5, 1), key=consts.key_volume_no),
                     sg.Button(image_data=icons_dark.icon_del_red,
                               pad=(0, 0), enable_events=True,
                               key=consts.key_del_doc_frm_col_1 + doc_no, )]
                ]

            )
        ],
    ]

    return layout


def add_doc_colum1_with_cap_completed(doc_no, volume):
    layout = [
        [
            sg.Frame(
                pad=(0, 8),
                relief=consts.frame_relief_main,
                title='',
                expand_x=True,
                # used to get the frame to remove when the img capturing completed
                key=consts.key_doc_number_holder_frame_offset + doc_no,
                layout=

                [
                    [doc_disply_layout(doc_no, color='light green'), ],
                    [sg.Text('Volume:'), sg.Text(volume, size=(5, 1)), sg.Button(image_data=icons_dark.icon_done_all,
                                                                                 key=consts.key_del_doc_frm_col_1 + doc_no,
                                                                                 pad=(0, 0), disabled=True)]
                ]

            )
        ],
    ]

    return layout


def add_img_list_to_edit_window(key, page_no):
    layout = [
        [
            sg.Frame(
                pad=(0, 5),

                # background_color='black',
                title='',
                expand_x=True,
                key=consts.key_raw_img_thump_holder_frame_offset + page_no,
                layout=

                [
                    [
                        sg.Image(data=icons_dark.icon_raw_img, key=key, enable_events=True, pad=(0, 0)),
                        sg.Text(f'- {page_no}', enable_events=True, ),

                    ]
                ]

            )
        ],
    ]
    return layout


def add_captured_document_to_col4(doc, ):
    # print(doc)
    layout = [
        [
            sg.Frame(
                pad=(0, 5),
                title='',
                expand_x=True,
                layout=

                [
                    [
                        doc_disply_layout(doc),
                        sg.Image(data=icons_dark.icon_done_all, )

                    ]
                ]

            )
        ],
    ]

    return layout


def add_doc_to_menu(doc_list, page_count):
    size_l = (12, 1)
    size_s = (8, 1)
    layout = [
        [
            sg.Frame(
                pad=(0, 5),
                # background_color='black',
                title='',
                expand_x=True,
                # used to get the frame to remove when the img capturing completed
                key=consts.key_menu_list_doc_frame_offset + doc_list[0],
                layout=

                [
                    [sg.Text(doc_list[0], size=size_l),
                     sg.Text(doc_list[1], size=(15, 1)),
                     sg.Text(page_count, size=(15, 1)),
                     # sg.Image(data=icons_dark.icon_check_grren, pad=(20, 1)) if doc_list[3] else sg.Image(
                     #     data=icons_dark.icon_close_red_small, pad=(20, 1)),
                     # sg.Image(data=icons_dark.icon_check_grren, pad=(30, 1)) if doc_list[4] else sg.Image(
                     #     data=icons_dark.icon_close_red_small, pad=(30, 1)),
                     # sg.Image(data=icons_dark.icon_check_grren, pad=(20, 1)) if doc_list[5] else sg.Image(
                     #     data=icons_dark.icon_close_red_small, pad=(20, 1)),
                     sg.Image(data=icons_dark.icon_pdf_sml_red, pad=((0, 25), (1, 1))) if doc_list[5] else sg.Image(
                         data=icons_dark.icon_img_red_small, pad=((0, 25), (1, 1))),
                     # sg.Image(data=icons_dark.icon_edit_red_sml, pad=(45, 1)),

                     sg.Image(data=icons_dark.icon_del_red_sml, pad=((80, 0), (1, 1)),
                              key=consts.key_menu_del_doc + doc_list[0],
                              enable_events=True)

                     ]
                ]

            )
        ],
    ]

    return layout


def add_doc_edit_pages(image, pageNo):
    key = consts.key_page_no + str(pageNo)
    layouts = [
                  sg.Frame(
                      pad=(5, 10),
                      title='',
                      expand_x=True,
                      layout=

                      [
                          [
                              sg.Image(data=image_processor.resize_image_reduce_for_sg(cv2.imread(image), (60, 80)),
                                       pad=(60, 1)),
                              sg.Text(str(pageNo), pad=(50, 1)),

                          ]
                      ]

                  )
              ],

    return layouts


def add_page_edit_box(page_no, ):
    key = consts.key_page_no + str(page_no)
    layout = [
                 sg.Frame(
                     pad=(5, 10),
                     title='',
                     expand_x=True,
                     key=consts.key_page_edit_frame_offset + str(page_no),
                     layout=

                     [
                         [
                             sg.Text('Old No', pad=(5, 10), text_color='light green'),
                             sg.Input(size=(4, 5), pad=(0, 0), default_text=page_no, disabled=True,
                                      key=consts.key_org_page_no + str(page_no)),
                             sg.Text('New No', pad=(5, 10), ),
                             sg.Input(size=(4, 5), pad=(0, 0), default_text=page_no, key=key),

                         ]

                     ]

                 )
             ],
    return layout
