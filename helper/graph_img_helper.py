from helper import consts
import cv2
from layouts import image_editor_layout
import imutils

def draw_graph_img(window, key, image_path,current_doc ):
    # print('image path in draw grapgh image  ', image_path)
    consts.current_graph_image_path = image_path
    consts.current_image_obj = current_doc.get_img_obj_from_path(image_path)
    # print(consts.current_image_obj.get_image())
    img = cv2.imread(image_path, 0)
    width, height = img.shape
    if width > height:
        img = imutils.resize(cv2.imread(image_path, 0), width=480, height=720)
    else:
        img = imutils.resize(cv2.imread(image_path, 0), width=720, height=480)
    # print(img)
    window[key].erase()
    window[key].draw_image(
            data=cv2.imencode('.png', img)[1].tobytes(),
            location=(0, consts.graph_width))
    return img



def graph_header_update(window, docNo, pageNo, tot_page):
    window[consts.key_graph_header].update(
        value=f'{docNo} Page {pageNo} of {tot_page}')
    # print(f'Document: {docNo} Page {pageNo} of {tot_page}')
    # window[consts.key_total_page].update(value=tot_page)



def prepare_graph_for_editing(window, current_doc):
    # window[consts.key_total_page].update(value=current_doc.get_page_count())
    # print(current_doc.get_raw_image_by_index(0))
    img_for_editing = draw_graph_img(window, consts.key_graph,current_doc.get_raw_image_by_index(0), current_doc)
    graph_header_update(window, current_doc.get_doc_number(), 1,current_doc.get_page_count())
    return img_for_editing


def open_img_editor_layout(current_doc):
    img_edit_window = image_editor_layout.image_editing_window()
    img_for_editing = prepare_graph_for_editing(img_edit_window, current_doc)
    return img_for_editing
