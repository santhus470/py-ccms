
from helper import consts

# if event in document_list:
#     if current_doc_no is None:
#         current_doc = document_list[document_list.index(event)]
#         current_doc_no = current_doc.get_doc_number()
#         main_window[consts.key_disply_selected_doc].update(value=event)
#         if current_doc.get_is_capture_started() and not current_doc.get_is_capture_completed():
#             if current_doc_no not in hided_doc_list:
#                 for count, img in enumerate(current_doc.get_raw_image_list()):
#                     window.extend_layout(window[consts.key_col3_raw_img_thump_col],
#                                          add_img_list_to_col3(key=img, image=cv2.imread(img),
#                                                               doc_num=current_doc_no, page_no=count))
#             else:
#                 for frame_count in range(current_doc.get_page_count()):
#                     main_window[consts.key_raw_img_thump_holder_frame_offset + current_doc_no +
#                                 str(frame_count)].unhide_row()
#             window[consts.key_col3_raw_img_thump_col].contents_changed()
#             window.refresh()
#             main_window[consts.key_save_all_raw_img_btn].update(disabled=False)
#             main_window[consts.key_disply_selected_doc].update(current_doc_no)
#             image_caputr_count = current_doc.get_page_count()
#         elif not current_doc.get_is_capture_started():
#             image_caputr_count = 0
#             main_window[consts.key_disply_selected_doc].update(current_doc_no)
#             main_window.ding()
#
#         elif current_doc.get_is_capture_completed():
#             my_popups.waiting_window()
#             img_edit_window = image_editing_window()
#             current_image_index = 0
#             img_for_editing = graph_img_helper.start_img_edit_window(img_edit_window, current_doc)
#             sg.popup_animated(None)
#
#     else:
#         if event != current_doc_no:
#             # if not current_doc.get_is_process_statred() and (document_list[document_list.index(event)].get_is_capture_started() and not document_list[document_list.index(event)].get_is_capture_completed()):
#             if current_doc.get_is_capture_started() and not current_doc.get_is_capture_completed():
#                 image_caputr_count = current_doc.get_page_count()
#                 for frame_count in range(image_caputr_count):
#                     main_window[consts.key_raw_img_thump_holder_frame_offset + current_doc_no +
#                                 str(frame_count)].hide_row()
#
#                 if current_doc_no not in hided_doc_list:
#                     hided_doc_list.append(current_doc_no)
#                 current_doc = document_list[document_list.index(event)]
#
#                 current_doc_no = current_doc.get_doc_number()
#                 main_window[consts.key_disply_selected_doc].update(value=current_doc_no)
#
#                 if current_doc.get_is_capture_started() and not current_doc.get_is_capture_completed():
#                     if current_doc_no not in hided_doc_list:
#                         for count, img in enumerate(current_doc.get_raw_image_list()):
#                             window.extend_layout(window[consts.key_col3_raw_img_thump_col],
#                                                  add_img_list_to_col3(key=img, image=cv2.imread(img),
#                                                                       doc_num=current_doc_no, page_no=count))
#                     else:
#                         for frame_count in range(current_doc.get_page_count()):
#                             main_window[consts.key_raw_img_thump_holder_frame_offset + current_doc_no +
#                                         str(frame_count)].unhide_row()
#                     image_caputr_count = current_doc.get_page_count()
#                     main_window[consts.key_save_all_raw_img_btn].update(disabled=False)
#                     main_window[consts.key_disply_selected_doc].update(current_doc_no)
#                 window[consts.key_col3_raw_img_thump_col].contents_changed()
#                 window.refresh()
#             else:
#                 current_doc = document_list[document_list.index(event)]
#                 current_doc_no = current_doc.get_doc_number()
#                 # main_window[consts.key_disply_selected_doc].update(current_doc_no)
#             if not current_doc.get_is_capture_started():
#                 image_caputr_count = 0
#                 main_window[consts.key_disply_selected_doc].update(current_doc_no)
#                 main_window.ding()
#
#             if current_doc.get_is_capture_completed():
#                 my_popups.waiting_window()
#                 img_edit_window = image_editing_window()
#                 current_image_index = 0
#                 img_for_editing = graph_img_helper.start_img_edit_window(img_edit_window, current_doc)
#                 sg.popup_animated(None)
#         if event == current_doc_no:
#             if current_doc.get_is_capture_completed():
#                 my_popups.waiting_window()
#                 img_edit_window = image_editing_window()
#                 current_image_index = 0
#                 img_for_editing = graph_img_helper.start_img_edit_window(img_edit_window, current_doc)
#                 sg.popup_animated(None)
