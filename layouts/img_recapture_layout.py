
# import PySimpleGUI as sg
#
# def create_re_cap_window():
#     layout = [
#         [sg.Button(image_data=consts.icon_close, button_color='red', tooltip='close', mouseover_colors='brown',
#                    key=consts.key_img_view_win_close, ), ],
#         [sg.Image(filename='', key=consts.key_recap_video_view_disply, size=(800,600) )],
#         [sg.Button(image_data=consts.icon_capture_image, button_color='red', tooltip='close', mouseover_colors='brown',
#                     ), ],
#     ]
#     return sg.Window("View You Image",
#                      layout,
#                      # # location=(10, 10),
#                      modal=True,
#
#                      element_justification='right',
#                      # disable_close=True,
#                      # disable_minimize=True,
#                      # resizable=False,
#                      # grab_anywhere=True,
#                      force_toplevel=True,
#                      finalize=True,
#                      size=(850,700),
#                      no_titlebar=True,
#
#                      )
