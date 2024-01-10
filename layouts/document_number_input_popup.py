import PySimpleGUI as sg
from helper import consts


def popup_document_input_receiver():
    layout = [
        [sg.Text('Document', font=consts.heading_fonts, text_color='white', background_color=consts.theme_light_2, )],
        [sg.Text('Book no', size=consts.doc_read_Text_size, font=consts.normal_font,
                 background_color=consts.theme_light_2),
         sg.Spin(key=consts.key_doc_input_book, size=(17, 1), font=consts.normal_font,
                 background_color=consts.theme_light_2,
                 values=('1', '3', '4'), readonly=True,
                 initial_value='1')],
        [sg.Text('Doc Number', size=consts.doc_read_Text_size, font=consts.normal_font,
                 background_color=consts.theme_light_2),
         sg.Input(key=consts.key_doc_input_doc, size=consts.doc_read_input_size, font=consts.normal_font,
                  do_not_clear=False)],
        [sg.Text('Year', size=consts.doc_read_Text_size, font=consts.normal_font,
                 background_color=consts.theme_light_2),
         sg.Input(key=consts.key_doc_input_year, size=consts.doc_read_input_size, font=consts.normal_font,
                  do_not_clear=False)],
        [sg.Text('Volume', size=consts.doc_read_Text_size, font=consts.normal_font,
                 background_color=consts.theme_light_2),
         sg.Input(key=consts.key_doc_input_vol, size=consts.doc_read_input_size, font=consts.normal_font,
                  do_not_clear=False)],
        [
            sg.Button(key=consts.key_btn_add_doc_save, button_text='Save', size=(10, 2), expand_x=True,
                      enable_events=True, bind_return_key=True),
            sg.Button('Close',key = consts.key_btn_add_doc_close, size=(10, 2), expand_x=True, bind_return_key=True),
        ],

    ]
    return sg.Window("Add Documents", layout, use_default_focus=False,
                     background_color=consts.theme_light_2,
                     finalize=True, modal=True, force_toplevel=True, no_titlebar=True,
                     keep_on_top=True, size=(420, 300), margins=(30, 10), element_padding=10, )
