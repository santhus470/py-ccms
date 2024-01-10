import PySimpleGUI as sg
from helper import consts

def create_list_for_doc_view(doc_list):
    menu_item_list = []
    for document in doc_list:
        menu_item_list.append([
            document.get_doc_number(),
            document.get_volume(),
            document.get_page_count(),
            document.get_is_capture_completed(),
            document.get_is_proess_completed(),
            document.get_is_document_created(),


        ])
    return menu_item_list

def get_page_count_for_menu(doc_list, doc):
    return doc_list[doc_list.index(doc)].get_page_count()