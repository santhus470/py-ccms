from helper import consts
import PySimpleGUI as sg
from assets import icons_dark


def waiting_window(text='Processing'):
    layout = [

        [
            sg.Text(text=f'\n{text}\n', font=consts.normal_font, text_color='white',
                    background_color=consts.popup_back_color)
        ],

    ]

    return sg.Window('Waiting', layout, use_default_focus=False,
                     element_justification='c', border_depth=3,
                     background_color=consts.popup_back_color,
                     finalize=True, modal=True,
                     force_toplevel=True,
                     no_titlebar=True,
                     keep_on_top=True,
                     size=(200, 90),
                     element_padding=10, )


# def waiting_window():
#     for i in range(10):
#         if not sg.popup_animated(
#                 gifs.loading_gif,
#                 time_between_frames=30, text_color='green',
#                 background_color='white'):
#             break


def ok_success_popup(text, title):
    return sg.PopupOK(text, title=title,
                      keep_on_top=True, background_color=consts.popup_back_color, no_titlebar=True)


def ok_error_popup(text, title):
    return sg.PopupOK(f'\n{text}\n', title=title, text_color='white',
                      keep_on_top=True, background_color='red', no_titlebar=True)


def ok_cancel_popup(text, title):
    return sg.PopupOKCancel(F'\n{text}\n', title=title, text_color=consts.popup_text_color, no_titlebar=True,
                            keep_on_top=True, background_color=consts.popup_back_color, )


def yes_no_popup(text, title):
    return sg.PopupYesNo(F'\n{text}\n', title=title, text_color=consts.popup_text_color,
                         keep_on_top=True, background_color=consts.popup_back_color, no_titlebar=True)


def no_btn_success_popup(text: object, duration=1) -> object:
    sg.popup_no_buttons(F'\n{text}\n', text_color='white',
                        keep_on_top=True, background_color=consts.popup_back_color,
                        no_titlebar=True, auto_close=True, auto_close_duration=duration)


def no_btn_error_popup(text, duration=1.2):
    sg.popup_no_buttons(F'\n{text}\n', text_color=consts.popup_text_color,
                        keep_on_top=True, background_color='red', font=consts.heading_fonts,
                        no_titlebar=True, auto_close=True, auto_close_duration=duration
                        )

def start_win():
    sg.popup_no_buttons('Starting CCMS Please wait ', image=icons_dark.default_img, no_titlebar=True, auto_close=True,
                        auto_close_duration=25)


def close_win_pop():
    return sg.PopupYesNo('\nDo You really  want to exit this window ?\n', title='Closing', text_color=consts.popup_text_color,
                         keep_on_top=True, background_color='red', no_titlebar=True)
