import os
import stat
import threading
import PySimpleGUI as sg
import cv2
from data_classes import database_class, my_themes
from data_classes.document import Document, CapturedImages
from helper import consts, image_processor, video_capture, graph_img_helper, menu_helper, add_doc_helper, config_helps, \
    btn_enable_disable, original_img_provider
from layouts import primary_window, about
from layouts.document_number_input_popup import popup_document_input_receiver
from layouts.image_editor_layout import image_editing_window
from layouts.image_view import create_img_view_window
from layouts.laout_extender import add_img_list_to_col3, add_doc_to_menu, add_page_edit_box
from layouts.menu_doc_all_view import create_menu_doc_view_win, create_generated_document_window
from layouts import my_popups, file_browse
from assets import icons_dark
import shutil
import imutils

sg.theme_add_new('my_dark', my_themes.blue_grey_theme_dark)
sg.theme_add_new('my_light1', my_themes.blue_grey_theme_light1)
sg.theme_add_new('my_light2', my_themes.blue_grey_theme_light2)
sg.theme('my_dark')
sg.set_global_icon(icons_dark.main_icon)
sg.set_options(font='ubuntu 11 ')
sg.set_options()


def get_directory(name):
    my_dir_path = os.path.join(os.getcwd(), name)
    if not os.path.exists(my_dir_path):
        os.mkdir(my_dir_path)
        os.chmod(my_dir_path, 777)
    # os.chmod(my_dir_path, stat.S_IWRITE)
    return my_dir_path


consts.thresh_dir = get_directory('thresholded')
consts.raw_dir = get_directory('raw_documents')
consts.processed_dir = get_directory('processed_img')
consts.json_dir = get_directory('json_files')
consts.db_dir = get_directory('my_db')
consts.pdf_dir = get_directory('created_pdf')


def main():
    if not video_capture.check_for_digicam_presence():
        sg.PopupOK(consts.digicam_msg,
                   no_titlebar=True,
                   background_color='red',
                   font=consts.normal_font,
                   icon=icons_dark.main_icon
                   )

    db_connection = database_class.connect()
    database_class.create_primary_table(db_connection)
    database_class.create_final_table(db_connection)
    global img_for_editing
    current_doc_no = None
    set_curent_document = Document('01/01/0101')
    current_doc = set_curent_document
    image_caputr_count = 0
    page_no = 0
    cropped = False
    brightness = 1
    contrast = 1
    threshold = ()
    is_doc_genration_list = False
    list_of_doc_for_generation = []
    is_raw_img_save_all_btn_enabled = False  # used to control the save all button state
    draw_points = False
    hided_doc_list = []
    crop_point_list = []
    crop_point_id_list = []
    crop_point_line_id_list = []
    current_image_index = 0
    recapture = False
    recapture_img_list = []
    # creating window
    recording = False

    main_window, doc_input_win, img_edit_window, img_view_window, menu_generated_doc_win, \
    cam_select_win, camera_start_win, recap_win, menu_alldoc_view_win, my_pop, page_edit_win = primary_window.main_window(), None, None, None, None, None, None, None, None, None, None
    file_browser_win = None
    waiting_window = None
    about_window = None
    main_window.maximize()
    main_window.ding()

    document_list = add_doc_helper.get_document_from_db(db_connection, main_window)

    # cursor creation
    main_window[consts.key_btn_add_doc].set_cursor(cursor='hand2')
    main_window[consts.key_capture_image].set_cursor(cursor='hand2')
    main_window[consts.key_preview].set_cursor(cursor='hand2')
    main_window[consts.key_save_all_raw_img_btn].set_cursor(cursor='hand2')

    def reset_for_next_and_prev():
        img_edit_window[consts.key_crop_selct_point].update(disabled=False)
        img_edit_window[consts.key_crop_btn].update(disabled=True)
        img_edit_window[consts.key_crop_only].update(disabled=True)
        img_edit_window[consts.key_bright_control].update(value=1)
        img_edit_window[consts.key_contrast_control].update(value=1)
        img_edit_window[consts.key_graph].set_cursor(cursor='arrow', cursor_color='blue')

    while True:
        window, event, values = sg.read_all_windows(timeout=20)
        if event == sg.WINDOW_CLOSED:
            input = my_popups.close_win_pop()
            if input == 'Yes':
                if window == doc_input_win:
                    doc_input_win = None
                if window == img_edit_window:
                    current_doc = set_curent_document
                    current_doc_no = None
                    current_doc_index = None
                    is_doc_genration_list = False
                    list_of_doc_for_generation = []
                    main_window[consts.key_disply_selected_doc].update(value='')
                    page_no = 1
                    crop_point_list = []
                    crop_point_id_list = []
                    img_edit_window.close()
                    cropped = False
                    brightness = 1
                    contrast = 1
                    threshold = []
                    img_edit_window.close()
                    img_edit_window = None
                if window == img_view_window:
                    img_view_window.close()
                    img_view_window = None
                    current_image_index = 0
                    page_no = 0
                    if img_edit_window is not None:
                        img_edit_window.force_focus()
                        img_edit_window[consts.key_graph].erase()
                        img_for_editing = graph_img_helper.draw_graph_img(img_edit_window, consts.key_graph,
                                                                          current_doc.get_raw_image_by_index(
                                                                              0), current_doc)
                        graph_img_helper.graph_header_update(img_edit_window, current_doc_no,
                                                             current_doc.get_page_number_from_img_at_index(0),
                                                             current_doc.get_page_count())
                if window == cam_select_win:
                    img_view_window.close()
                    cam_select_win = None
                if window == camera_start_win:
                    camera_start_win.close()
                    camera_start_win = None
                if window == menu_alldoc_view_win:
                    menu_alldoc_view_win.close()
                    menu_alldoc_view_win = None
                if window == menu_generated_doc_win:
                    menu_generated_doc_win.close()
                    menu_generated_doc_win = None
                if window == my_pop:
                    my_pop.close()
                    my_pop = None
                if window == page_edit_win:
                    page_edit_win.close()
                    page_edit_win = None
                if window == about_window:
                    about_window.close()
                    about_window = None
                elif window == main_window:
                    break

        if event == consts.key_btn_add_doc:
            doc_input_win = popup_document_input_receiver()
            doc_input_win[consts.key_doc_input_doc].set_focus()
            # doc_input_win[consts.key_btn_add_doc_save].bind("<Return>", "_Enter")

        if event == consts.key_btn_add_doc_save:
            add_doc_helper.save_document_no(values, document_list, main_window, db_connection, hided_doc_list)
            doc_input_win[consts.key_doc_input_doc].set_focus()
            # print(database_class.get_doc_from_primary(db_connection))

        # ---------------------------------------------------------------------------------------------------------------------
        #                       TODO DOCUMENT SELECTION
        # ----------------------------------------------------------------------------------------------------------------------
        if event in document_list:
            if current_doc_no is None:
                current_doc = document_list[document_list.index(event)]
                current_doc_no = current_doc.get_doc_number()
                main_window[consts.key_disply_selected_doc].update(value=event)
                if current_doc.get_is_capture_started() and not current_doc.get_is_capture_completed():
                    main_window[consts.key_save_all_raw_img_btn].update(disabled=False)
                    main_window[consts.key_disply_selected_doc].update(current_doc_no)
                    image_caputr_count = current_doc.get_page_count()
                    if current_doc_no not in hided_doc_list:
                        for count, img in enumerate(current_doc.get_raw_image_list()):
                            window.extend_layout(window[consts.key_col3_raw_img_thump_col],
                                                 add_img_list_to_col3(key=img, page_no=count + 1))
                            window[current_doc.get_raw_image_by_index(count)].set_cursor(cursor='hand2', )

                    else:
                        for frame_count in range(image_caputr_count):
                            main_window[consts.key_raw_img_thump_holder_frame_offset
                                        + current_doc.get_raw_image_by_index(frame_count)].unhide_row()
                    my_popups.no_btn_success_popup(f'{current_doc_no} selected ')
                    window.refresh()
                    window[consts.key_col3_raw_img_thump_col].contents_changed()

                elif not current_doc.get_is_capture_started():
                    image_caputr_count = 0
                    main_window[consts.key_disply_selected_doc].update(current_doc_no)
                    main_window.ding()
                    my_popups.no_btn_success_popup(f'{current_doc_no} selected ')

                elif current_doc.get_is_capture_completed():
                    img_edit_window = image_editing_window()
                    current_image_index = 0
                    img_for_editing = graph_img_helper.prepare_graph_for_editing(img_edit_window, current_doc)
                    window.refresh()
                    window[consts.key_col3_raw_img_thump_col].contents_changed()

            else:
                if event != current_doc_no:
                    if not current_doc.get_is_capture_started() or current_doc.get_is_capture_completed():
                        current_doc = document_list[document_list.index(event)]
                        current_doc_no = current_doc.get_doc_number()
                        if not current_doc.get_is_capture_started():
                            current_image_index = 0
                            image_caputr_count = 0
                            main_window[consts.key_disply_selected_doc].update(current_doc_no)
                            main_window.ding()
                        if current_doc.get_is_capture_started() and not current_doc.get_is_capture_completed():
                            image_caputr_count = current_doc.get_page_count()
                            if current_doc_no not in hided_doc_list:
                                for count, img in enumerate(current_doc.get_raw_image_list()):
                                    window.extend_layout(window[consts.key_col3_raw_img_thump_col],
                                                         add_img_list_to_col3(key=img, page_no=count + 1))
                                    window[current_doc.get_raw_image_by_index(count)].set_cursor(cursor='hand2', )
                            else:
                                for frame_count in range(image_caputr_count):
                                    main_window[consts.key_raw_img_thump_holder_frame_offset +
                                                current_doc.get_raw_image_by_index(frame_count)].unhide_row()

                        if current_doc.get_is_capture_completed():
                            img_edit_window = image_editing_window()
                            current_image_index = 0
                            img_for_editing = graph_img_helper.prepare_graph_for_editing(img_edit_window, current_doc)
                        my_popups.no_btn_success_popup(f'{current_doc_no} selected ')

                    if current_doc.get_is_capture_started() and not current_doc.get_is_capture_completed():
                        image_caputr_count = current_doc.get_page_count()
                        for frame_count in range(image_caputr_count):
                            main_window[consts.key_raw_img_thump_holder_frame_offset +
                                        current_doc.get_raw_image_by_index(frame_count)].hide_row()
                            window[current_doc.get_raw_image_by_index(frame_count)].set_cursor(cursor='hand2',
                                                                                               cursor_color='red')

                        if current_doc_no not in hided_doc_list:
                            hided_doc_list.append(current_doc_no)

                        current_doc = document_list[document_list.index(event)]
                        current_doc_no = current_doc.get_doc_number()
                        main_window[consts.key_disply_selected_doc].update(value=current_doc_no)
                        main_window[consts.key_video_view_disply].update(data=icons_dark.default_img)
                        my_popups.no_btn_success_popup(f'{current_doc_no} selected ')
                        if not current_doc.get_is_capture_started():
                            current_image_index = 0
                            image_caputr_count = 0
                            main_window[consts.key_disply_selected_doc].update(current_doc_no)
                            main_window.ding()

                        if current_doc.get_is_capture_started() and not current_doc.get_is_capture_completed():
                            image_caputr_count = current_doc.get_page_count()
                            if current_doc_no not in hided_doc_list:
                                for count, img in enumerate(current_doc.get_raw_image_list()):
                                    window.extend_layout(window[consts.key_col3_raw_img_thump_col],
                                                         add_img_list_to_col3(key=img,
                                                                              page_no=count + 1))
                                    window[current_doc.get_raw_image_by_index(count)].set_cursor(cursor='hand2',
                                                                                                 cursor_color='red')
                            else:
                                for frame_count in range(image_caputr_count):
                                    main_window[consts.key_raw_img_thump_holder_frame_offset +
                                                current_doc.get_raw_image_by_index(frame_count)].unhide_row()
                            window.refresh()
                            window[consts.key_col3_raw_img_thump_col].contents_changed()

                            my_popups.no_btn_success_popup(f'{current_doc_no} selected ')

                        if current_doc.get_is_capture_completed():
                            current_image_index = 0
                            img_edit_window = image_editing_window()
                            img_for_editing = graph_img_helper.prepare_graph_for_editing(img_edit_window, current_doc)
                            window.refresh()
                            window[consts.key_col3_raw_img_thump_col].contents_changed()



                elif event == current_doc_no:
                    if current_doc.get_is_capture_completed():
                        current_image_index = 0
                        img_edit_window = image_editing_window()
                        img_for_editing = graph_img_helper.prepare_graph_for_editing(img_edit_window, current_doc)

        # ---------------------------------------------------------------------------
        #                       TODO CAPTURING AND PEVIEWING
        # -------------------------------------------------------------------------------

        if event == consts.key_preview:
            if current_doc_no is not None:
                im_captured, img_path, _ = video_capture.capture_img(current_doc_no, preview=True, window=main_window)
                if im_captured is not None:
                    main_window[consts.key_video_view_disply].update(
                        data=cv2.imencode('.png', im_captured)[1].tobytes())
                    os.remove(img_path)

            else:
                my_popups.ok_error_popup('Please select a document first', 'Preview')

        if event == consts.key_capture_image:
            if current_doc_no is not None:
                frame, current_img_path, thresh_path = video_capture.capture_img(current_doc_no, image_caputr_count,
                                                                                 preview=False, window=main_window)
                # sg.PopupAnimated(None)
                if frame is not None:
                    image_caputr_count += 1
                    main_window[consts.key_video_view_disply].update(data=cv2.imencode('.png', frame)[1].tobytes())
                    window.extend_layout(window[consts.key_col3_raw_img_thump_col],
                                         add_img_list_to_col3(key=thresh_path, page_no=image_caputr_count))
                    if recapture:
                        recapture_img_list.append(thresh_path)
                    window[thresh_path].set_cursor(cursor='hand2')
                    current_doc.add_raw_image(CapturedImages(thresh_path))
                    window.refresh()
                    main_window[consts.key_col3_raw_img_thump_col].contents_changed()

                    if not current_doc.get_is_capture_started():
                        database_class.set_capture_start(db_connection, current_doc_no)
                        current_doc.set_capture_started()

                    if not is_raw_img_save_all_btn_enabled:
                        main_window[consts.key_save_all_raw_img_btn].update(disabled=False)


            else:
                my_popups.ok_error_popup('Select a document first ', title='Stop')

        # --------------------------------------------------------------------------------------------------------------------
        #                       TODO SAVE ALL IMAGE
        # --------------------------------------------------------------------------------------------------------------------

        if event == consts.key_save_all_raw_img_btn:  # when the user click on the save all button in col3
            #     what will happen here is
            #  first confirm the user to save the details by  a popup
            # 1.clear the colum3 - delete the list of all raw image
            # 2.clear the selected image for capturing (camera heading)
            # 3. delete the document number from the document list column(column 1)
            # 4. set the capture_complete to True in the current document
            # 6. set this button to disabled
            # 7. add the document to the 7th column- thats capture completed Documents
            result = sg.popup_yes_no('Document capturing completed..?\n', title='Image', keep_on_top=True,
                                     no_titlebar=True,
                                     modal=True, background_color=consts.popup_back_color)


            if result == 'Yes':
                if not recapture:
                    for frame_count in range(current_doc.get_page_count()):
                        main_window[consts.key_raw_img_thump_holder_frame_offset +
                                    current_doc.get_raw_image_by_index(frame_count)].hide_row()
                else:
                    for img in recapture_img_list:
                        main_window[consts.key_raw_img_thump_holder_frame_offset + img].hide_row()
                    recapture_img_list.clear()
                main_window[consts.key_del_doc_frm_col_1 + current_doc_no].update(image_data=icons_dark.icon_done_all)
                main_window[consts.key_del_doc_frm_col_1 + current_doc_no].update(disabled=True)
                main_window[current_doc_no].update(text_color='light green')
                current_doc.set_capture_completed(True)
                database_class.set_capture_complete(db_connection, current_doc_no)
                current_doc_no = None
                current_image_index = 0
                image_caputr_count = 0
                main_window[consts.key_disply_selected_doc].update(value='')
                main_window[consts.key_save_all_raw_img_btn].update(disabled=True)
                is_raw_img_save_all_btn_enabled = False
                main_window[consts.key_video_view_disply].update(data=icons_dark.default_img)
                recapture = False

        # -----------------------------------------------------------------------------------------------------
        #                       TODO         OPEN IMAGE FOR VIEW
        # ---------------------------------------------------------------------------------------------------
        if event in current_doc.get_raw_image_list():
            page_no = current_doc.get_page_number_of_image(event)
            all_page = current_doc.get_page_count()
            current_image_index = current_doc.get_index_of_raw_img(event)
            img_view_window = create_img_view_window()
            graph_img_helper.draw_graph_img(img_view_window, consts.key_img_view_graph, event, current_doc)
            graph_img_helper.graph_header_update(img_view_window,
                                                 current_doc_no,
                                                 page_no, current_doc.get_page_count())
            for i in range(all_page):
                img_view_window.extend_layout(img_view_window[consts.key_page_editlist_col], add_page_edit_box(
                    current_doc.get_page_number_from_img_at_index(i), ))
            img_view_window.refresh()
            img_view_window[consts.key_page_editlist_col].contents_changed()
        # -------------------------------------------------------------------------------------------------------
        #                         TODO NEXT AND PREVIOUS
        # ---------------------------------------------------------------------------------------------------------
        if event == consts.key_img_view_next:  # when user click on the next button on the imgae_view_window
            page_count = current_doc.get_page_count() - 1
            if current_image_index < page_count:
                current_image_index = current_image_index + 1
                if window == img_view_window:
                    page_no = current_doc.get_page_number_from_img_at_index(current_image_index)
                    img_view_window[consts.key_img_view_graph].erase()
                    graph_img_helper.draw_graph_img(window=img_view_window, key=consts.key_img_view_graph,
                                                    image_path=current_doc.get_raw_image_by_index(
                                                        current_image_index), current_doc=current_doc)

                    graph_img_helper.graph_header_update(img_view_window, current_doc_no, page_no,
                                                         current_doc.get_page_count())

                if window == img_edit_window:
                    img_edit_window[consts.key_graph].erase()
                    img_for_editing = graph_img_helper.draw_graph_img(img_edit_window, consts.key_graph,
                                                                      current_doc.get_raw_image_by_index(
                                                                          current_image_index), current_doc)
                    graph_img_helper.graph_header_update(img_edit_window, current_doc_no,
                                                         consts.current_image_obj.get_page_number(),
                                                         current_doc.get_page_count())
                    crop_point_list.clear()
                    crop_point_id_list.clear()
                    crop_point_line_id_list.clear()
                    draw_points = False
                    brightness = 1
                    contrast = 1
                    threshold = ()
                    cropped = False
                    reset_for_next_and_prev()
                    if consts.current_image_obj:
                        if consts.current_image_obj.get_process_completed_value():  # get true or false (cropped or not)
                            btn_enable_disable.enable_edit_win_btn(img_edit_window)
                        else:
                            btn_enable_disable.disable_edit_win_btn(img_edit_window)

        if event == consts.key_img_view_prev:
            page_count = current_doc.get_page_count() - 1
            if current_image_index <= page_count and current_image_index != 0:
                current_image_index = current_image_index - 1
                if window == img_view_window:
                    img_view_window[consts.key_img_view_graph].erase()
                    page_no = current_doc.get_page_number_from_img_at_index(current_image_index)
                    graph_img_helper.draw_graph_img(window=img_view_window, key=consts.key_img_view_graph,
                                                    image_path=current_doc.get_raw_image_by_index(
                                                        current_image_index), current_doc=current_doc)
                    graph_img_helper.graph_header_update(img_view_window, current_doc_no,
                                                         current_doc.get_page_number_from_img_at_index(
                                                             current_image_index), current_doc.get_page_count())
                if window == img_edit_window:
                    img_edit_window[consts.key_graph].erase()

                    img_for_editing = graph_img_helper.draw_graph_img(img_edit_window, consts.key_graph,
                                                                      current_doc.get_raw_image_by_index(
                                                                          current_image_index), current_doc)
                    graph_img_helper.graph_header_update(img_edit_window, current_doc_no,
                                                         consts.current_image_obj.get_page_number()
                                                         , current_doc.get_page_count())

                    crop_point_list.clear()
                    crop_point_id_list.clear()
                    crop_point_line_id_list.clear()
                    draw_points = False
                    brightness = 1
                    contrast = 1
                    threshold = ()
                    cropped = False
                    reset_for_next_and_prev()
                    if consts.current_image_obj:
                        if consts.current_image_obj.get_process_completed_value():  # get true or false (cropped or not)
                            btn_enable_disable.enable_edit_win_btn(img_edit_window)
                        else:
                            btn_enable_disable.disable_edit_win_btn(img_edit_window)

        if event == consts.key_next_doc:
            current_doc_index = document_list.index(current_doc_no)
            if current_doc_index == len(document_list) - 1:
                my_popups.ok_success_popup('No process completed document left for editing', 'Next Doc.')
            else:
                current_doc_index += 1
                for i in range(current_doc_index, len(document_list)):
                    current_doc = document_list[i]
                    if current_doc.get_is_capture_completed():
                        current_doc_no = current_doc.get_doc_number()
                        current_image_index = 0
                        current_doc_index = i
                        img_edit_window[consts.key_graph].erase()
                        img_for_editing = graph_img_helper.draw_graph_img(img_edit_window, consts.key_graph,
                                                                          current_doc.get_raw_image_by_index(0),
                                                                          current_doc)
                        graph_img_helper.graph_header_update(img_edit_window, current_doc_no,
                                                             current_doc.get_page_number_from_img_at_index(
                                                                 0), current_doc.get_page_count())
                        crop_point_list.clear()
                        crop_point_id_list.clear()
                        crop_point_line_id_list.clear()
                        draw_points = False
                        brightness = 1
                        contrast = 1
                        threshold = ()
                        cropped = False
                        reset_for_next_and_prev()
                        break
                    else:
                        i += 1

        if event == consts.key_pre_doc:
            current_doc_index = document_list.index(current_doc_no)
            # print(current_doc_index)
            if current_doc_index == 0:
                my_popups.ok_success_popup('This is the first capture completed document', 'Stop')
            else:
                pre_index = current_doc_index - 1
                for i in range(current_doc_index):
                    if pre_index < 0:
                        break
                    else:
                        current_doc = document_list[pre_index]
                    if current_doc.get_is_capture_completed():
                        current_doc_no = current_doc.get_doc_number()
                        current_image_index = 0
                        current_doc_index = pre_index
                        img_edit_window[consts.key_graph].erase()
                        img_for_editing = graph_img_helper.draw_graph_img(img_edit_window, consts.key_graph,
                                                                          current_doc.get_raw_image_by_index(0),
                                                                          current_doc)
                        graph_img_helper.graph_header_update(img_edit_window, current_doc_no,
                                                             current_doc.get_page_number_from_img_at_index(
                                                                 0), current_doc.get_page_count())
                        crop_point_list.clear()
                        crop_point_id_list.clear()
                        crop_point_line_id_list.clear()
                        draw_points = False
                        brightness = 1
                        contrast = 1
                        threshold = ()
                        cropped = False
                        reset_for_next_and_prev()
                        break
                    else:
                        pre_index -= 1

        # ------------------------------------------------------------------------------------------------------------
        #                                 TODO DELETE    IMAGE and DOC NO
        # -------------------------------------------------------------------------------------------------------------
        try:
            if event.startswith(consts.key_delete_thump_offset):
                # event is like this  - DELETE_RAW_THUMP#C:\ccms\thresholded\220-1-2019\220-1-2019-2.png
                result = sg.PopupYesNo('\nDo You really want to Delete  This image\n', title='Deleting', keep_on_top=True,
                                       modal=True, background_color=consts.popup_back_color, no_titlebar=True)
                if result == 'Yes':
                    page_count = current_doc.get_page_count()
                    selected_image = event.split('#')[1]
                    if page_count == 1:  # single page
                        main_window[consts.key_raw_img_thump_holder_frame_offset + current_doc.get_raw_image_by_index(
                            0)].hide_row()
                        main_window[consts.key_doc_number_holder_frame_offset + current_doc_no].hide_row()
                        hided_doc_list.append(current_doc_no)
                        document_list.remove(current_doc)
                        main_window[consts.key_video_view_disply].update(data=icons_dark.default_img)
                        main_window[consts.key_save_all_raw_img_btn].update(disabled=True)
                        # remove the folders
                        if os.path.exists(os.path.join(consts.raw_dir, current_doc_no)):
                            shutil.rmtree(os.path.join(consts.raw_dir, current_doc_no))
                        if os.path.exists(os.path.join(consts.thresh_dir, current_doc_no)):
                            shutil.rmtree(os.path.join(consts.thresh_dir, current_doc_no))

                        # remove it from database
                        try:
                            database_class.del_doc_from_primaryTb(db_connection, current_doc_no)
                        except:
                            my_popups.ok_error_popup('\n Cannot access database now.  Please Try again\n'
                                                     'or restart the application to effect the same .Thanks',
                                                     'deleting')
                        current_doc_no = None
                        current_doc = set_curent_document
                        main_window[consts.key_disply_selected_doc].update(value='')

                    else:  # more than one image
                        img_obj = current_doc.get_img_obj_from_path(selected_image)
                        main_window[consts.key_raw_img_thump_holder_frame_offset + selected_image].hide_row()
                        current_doc.remove_raw_image(img_obj)
        except:
            pass

        if event == consts.key_img_view_del:
            result = sg.PopupYesNo('\nDo You really want to Delete  This image\n', title='Deleting', keep_on_top=True,
                                   modal=True, background_color=consts.popup_back_color, no_titlebar=True)
            if result == 'Yes':
                all_page = current_doc.get_page_count()
                if window == img_edit_window:
                    img_edit_window.close()
                    img_edit_window = None
                    img_view_window = create_img_view_window()
                    current_doc_no = current_doc.get_doc_number()
                    graph_img_helper.draw_graph_img(img_view_window, consts.key_img_view_graph,
                                                    current_doc.get_raw_image_by_index(0), current_doc)
                    graph_img_helper.graph_header_update(img_view_window, current_doc_no, 1,
                                                         current_doc.get_page_count())
                    current_image_index = 0

                    for page in range(1, all_page + 1):
                        img_view_window.extend_layout(img_view_window[consts.key_page_editlist_col],
                                                      add_page_edit_box(page))
                    img_view_window.refresh()
                    img_view_window[consts.key_page_editlist_col].contents_changed()

                if window == img_view_window:
                    all_imgList = current_doc.get_raw_img_obj_list()
                    current_img_obj = consts.current_image_obj
                    curret_img_path = consts.current_graph_image_path
                    if len(all_imgList) == 1:
                        hided_doc_list.append(current_doc_no)
                        document_list.remove(current_doc)
                        current_doc.clear_img_list()
                        img_view_window[consts.key_img_view_graph].erase()
                        img_view_window.close()
                        img_view_window = None
                        # remove the folders
                        if os.path.exists(os.path.join(consts.raw_dir, current_doc_no)):
                            shutil.rmtree(os.path.join(consts.raw_dir, current_doc_no))
                        if os.path.exists(os.path.join(consts.thresh_dir, current_doc_no)):
                            shutil.rmtree(os.path.join(consts.thresh_dir, current_doc_no))

                        # remove it from database
                        try:
                            database_class.del_doc_from_primaryTb(db_connection, current_doc_no)
                        except:
                            my_popups.ok_error_popup('\n Cannot access database now.  Please Try again\n'
                                                     'or restart the application to effect the same .Thanks',
                                                     'deleting')
                        current_doc_no = None
                        current_doc = set_curent_document
                        main_window[consts.key_disply_selected_doc].update(value='')
                    else:
                        current_image_index = current_doc.get_index_of_raw_img(curret_img_path)
                        if current_image_index == 0:
                            current_image_index = current_image_index + 1
                        current_image_index = current_image_index - 1
                        img_view_window[consts.key_img_view_graph].erase()
                        current_doc.remove_raw_image(current_img_obj)
                        graph_img_helper.draw_graph_img(img_view_window, consts.key_img_view_graph,
                                                        current_doc.get_raw_image_by_index(current_image_index),
                                                        current_doc)
                        graph_img_helper.graph_header_update(img_view_window, current_doc_no,
                                                             current_doc.get_page_number_from_img_at_index(
                                                                 current_image_index), current_doc.get_page_count())

                        img_view_window[
                            consts.key_page_edit_frame_offset + str(current_img_obj.get_page_number())].hide_row()
                        img_view_window.refresh()
                        img_view_window[consts.key_page_editlist_col].contents_changed()
        try:
            if event.startswith(consts.key_del_doc_frm_col_1):  # when a user click on the delete button in the doc
                # 1.inform the user they reply want to delete the document
                # 2 if yes delete the document from list
                # 3. set the selected document for capture to '' if it selected for
                # 4 remove the document from the document list
                # 5. remove the frame that hold this document
                # TODO if a user first delete a document from col 1 after taking some image - the program will crash
                # print(event)
                # try:
                doc_no = event.split('_')[1]
                if doc_no:
                    confirm = my_popups.yes_no_popup(F'Do you want to delete  Document {doc_no}', 'Deleting')
                    if confirm == 'Yes':
                        pos = document_list.index(doc_no)
                        doc_obj = document_list[pos]
                        imgcount = doc_obj.get_page_count()
                        if doc_no == current_doc_no:
                            if imgcount > 0:
                                for img in doc_obj.get_raw_image_list():
                                    main_window[consts.key_raw_img_thump_holder_frame_offset + img].hide_row()

                        # main_window[event].hide_row()
                        hided_doc_list.append(doc_no)
                        document_list.remove(doc_no)
                        try:
                            database_class.del_doc_from_primaryTb(db_connection, doc_no)
                            main_window[
                                consts.key_doc_number_holder_frame_offset + doc_no].hide_row()
                        except:
                            my_popups.ok_error_popup('\n Cannot access database now.  Please Try again\n'
                                                     'or restart the application to effect the same .Thanks',
                                                     'deleting')
                        if os.path.exists(os.path.join(consts.raw_dir, doc_no)):
                            shutil.rmtree(os.path.join(consts.raw_dir, doc_no))
                        if os.path.exists(os.path.join(consts.thresh_dir, doc_no)):
                            shutil.rmtree(os.path.join(consts.thresh_dir, doc_no))
                        my_popups.no_btn_success_popup(f'Dcoument {doc_no} deleted successfully', )
                        if current_doc_no == doc_no:
                            current_doc_no = None
                            main_window[consts.key_disply_selected_doc].update(value='')
        except:
            pass
        try:
            # Delete document from menu list
            if event.startswith(consts.key_menu_del_doc):
                # the evenet us like   -DEL_DOC_FROM_MENU-.3353-1-2012
                selected_doc = event.split('.')[1]
                confirm = my_popups.yes_no_popup(F'Do you want to delete  Document {selected_doc}', 'Deleting')
                if confirm == 'Yes':
                    try:
                        menu_alldoc_view_win[consts.key_menu_list_doc_frame_offset + selected_doc].hide_row()
                        main_window[
                            consts.key_doc_number_holder_frame_offset + selected_doc].hide_row()
                        database_class.del_doc_from_primaryTb(db_connection, selected_doc)
                        document_list.remove(selected_doc)
                        if os.path.exists(os.path.join(consts.raw_dir, selected_doc)):
                            shutil.rmtree(os.path.join(consts.raw_dir, selected_doc))
                        if os.path.exists(os.path.join(consts.thresh_dir, selected_doc)):
                            shutil.rmtree(os.path.join(consts.thresh_dir, selected_doc))

                        my_popups.no_btn_success_popup(f'Dcoument {selected_doc} deleted successfully', )

                    except:
                        sg.popup_error("Sorry Can't delete the document now . Please try later ", 'error')
        except:
            pass

        # --------------------------------------------------------------------------------------------------------------
        #                            TODO DRAW POINTS AND CROPPING
        #  -----------------------------------------------------------------------------------------------------------
        if event == consts.key_crop_selct_point:
            draw_points = True
            img_edit_window[consts.key_graph].set_cursor(cursor='circle', cursor_color='blue')

        if event == consts.key_graph:  # if there's a "Graph" event, then it's a mouse
            # when a user click on the graph the following are happend
            # 1.get the x,y co-ordinates
            # 2.draw a point on the region and save the id of the point to circleIdlist for later user
            # 3.add the point to the crop_point_list (the y cordinates saved as 800-y becoze the grap size is 800*800
            # and start from bottom left corner . But the cv image start from topleft corner )for cropping the region
            # 4.when the selected point reach 4 stop drawing and the crop button will active
            if draw_points:
                x, y = values[consts.key_graph]
                if len(crop_point_list) <= 4:
                    circle_id = img_edit_window[consts.key_graph].draw_point(point=(x, y), size=10, color='red')
                    img_edit_window[consts.key_crop_undo].update(disabled=False)
                    crop_point_list.append([x, consts.graph_width - y])
                    crop_point_id_list.append(circle_id)
                    if len(crop_point_list) > 1:
                        line_id = window[consts.key_graph].draw_line(
                            point_from=(crop_point_list[-1][0], consts.graph_width - crop_point_list[-1][1]),
                            point_to=(crop_point_list[-2][0], consts.graph_width - crop_point_list[-2][1]),
                            color='red', width=2)
                        crop_point_line_id_list.append(line_id)
                if len(crop_point_list) == 4:
                    line_id = window[consts.key_graph].draw_line(
                        point_from=(crop_point_list[0][0], consts.graph_width - crop_point_list[0][1]),
                        point_to=(crop_point_list[3][0], consts.graph_width - crop_point_list[3][1]),
                        color='red', width=2)
                    crop_point_line_id_list.append(line_id)
                    img_edit_window[consts.key_graph].set_cursor(cursor='arrow', )
                    img_edit_window[consts.key_crop_btn].update(disabled=False)
                    img_edit_window[consts.key_crop_only].update(disabled=False)
                    img_edit_window[consts.key_crop_selct_point].update(disabled=True)
                    draw_points = False

        if event == consts.key_crop_btn:  # when the user click on the crop button
            if not cropped:
                result = my_popups.yes_no_popup('Do you actually want to crop the image', title='Cropping')
                if result == 'Yes':
                    if len(crop_point_list) == 4:
                        waiting_window = my_popups.waiting_window('Crop and processing')
                        img_for_editing = image_processor.crop_img(img_for_editing, crop_point_list)
                        crop_point_list = []
                        graph_img_helper.draw_graph_img(img_edit_window, consts.key_graph,
                                                        consts.current_graph_image_path, current_doc)
                        img_edit_window[consts.key_crop_btn].update(disabled=True)
                        img_edit_window[consts.key_crop_only].update(disabled=True)
                        img_edit_window[consts.key_crop_undo].update(disabled=False)
                        consts.current_image_obj.set_cropped(True)
                        cropped = True
                        consts.current_image_obj.set_process_completed(True)
                        waiting_window.close()
                        waiting_window = None
        if event == consts.key_crop_only:
            result = my_popups.yes_no_popup('Do you actually want to crop the image', title='Cropping')
            if result == 'Yes':
                if len(crop_point_list) == 4:
                    img_for_editing = image_processor.crop_img(img_for_editing, crop_point_list,
                                                               is_crop_and_process=False)
                    graph_img_helper.draw_graph_img(img_edit_window, consts.key_graph, consts.current_graph_image_path,
                                                    current_doc)
                    crop_point_list = []
                    img_edit_window[consts.key_crop_btn].update(disabled=True)
                    img_edit_window[consts.key_crop_only].update(disabled=True)
                    img_edit_window[consts.key_crop_undo].update(disabled=False)
                    consts.current_image_obj.set_cropped(True)
                    cropped = True
                    consts.current_image_obj.set_process_completed(True)
                    btn_enable_disable.enable_edit_win_btn(img_edit_window)
        # -------------------------------------------------------------------------------------------
        #      TODO CROP UNDO
        # ---------------------------------------------------------------------------------------

        if event == consts.key_crop_undo:
            # 1. enable the cropped button and point button
            # 2.if the image is cropped draw the original image and draw the given points saved inside the cropped dict
            # 3.set cropped to false
            number_of_line = len(crop_point_line_id_list)
            if number_of_line == 4:
                img_edit_window[consts.key_graph].delete_figure(crop_point_line_id_list[number_of_line - 1])
                crop_point_line_id_list.pop()
            if 0 < number_of_line < 4:
                img_edit_window[consts.key_graph].delete_figure(crop_point_id_list[number_of_line])
                img_edit_window[consts.key_graph].delete_figure(crop_point_line_id_list[number_of_line - 1])
                crop_point_line_id_list.pop()
                crop_point_id_list.pop()
                crop_point_list.pop()
            if number_of_line == 0 and len(crop_point_id_list) == 1:
                img_edit_window[consts.key_graph].delete_figure(crop_point_id_list[0])
                crop_point_line_id_list = []
                crop_point_id_list = []
                crop_point_list = []
            img_edit_window[consts.key_crop_selct_point].update(disabled=False)

            if cropped:
                img_path = current_doc.get_raw_image_by_index(current_image_index)
                img_for_editing = original_img_provider.get_org_img(img_path)
                consts.current_image_obj.set_cropped(False)
                img_edit_window[consts.key_graph].erase()
                # img_edit_window[consts.key_graph].draw_image(location=(0, consts.graph_width),
                #                                              data=cv2.imencode('.png', img_for_editing)[1].tobytes())
                # graph_img_helper.draw_graph_img(img_edit_window,consts.key_graph,img_path, current_doc)
                graph_img_helper.prepare_graph_for_editing(img_edit_window, current_doc)
                img_edit_window[consts.key_crop_btn].update(disabled=True)
                img_edit_window[consts.key_crop_selct_point].update(disabled=False)
                crop_point_list = []
                crop_point_id_list = []
                crop_point_line_id_list = []
                cropped = False
                consts.current_image_obj.set_process_completed(False)
                btn_enable_disable.disable_edit_win_btn(img_edit_window)

        # ---------------------------------------------------------------------
        #      TODO Contrast and BRIGHTNESS
        # ---------------------------------------------------------------------------------------
        if event == consts.key_contrast_control:
            contrast = 1 + (values[consts.key_contrast_control] / 50)
            # print('contrast-', contrast)
            img_edit_window[consts.key_graph].draw_image(
                location=(0, consts.graph_width),
                data=cv2.imencode('.png', cv2.convertScaleAbs(img_for_editing, alpha=contrast, beta=brightness))
                [1].tobytes())
            threshold = ()

        if event == consts.key_bright_control:
            brightness = 1 + (values[consts.key_bright_control])
            # print('brightness-', brightness)
            img_edit_window[consts.key_graph].draw_image(
                location=(0, consts.graph_width),
                data=cv2.imencode('.png', cv2.convertScaleAbs(img_for_editing, alpha=contrast, beta=brightness))[
                    1].tobytes())
            threshold = ()

        # -----------------------------------------------------------------------------------------------------------
        #                                    TODO ROTATION
        # -------------------------------------------------------------------------------------------------------------

        if event == consts.key_rot_right_90:
            img_for_editing = cv2.rotate(img_for_editing, cv2.ROTATE_90_CLOCKWISE)
            img_edit_window[consts.key_graph].erase()
            img_edit_window[consts.key_graph].draw_image(data=cv2.imencode('.png', img_for_editing)[1].tobytes(),
                                                         location=(0, consts.graph_width))
            # img_edit_window[consts.key_graph].draw_image(data=img_for_editing)

            crop_point_list = []
            crop_point_id_list = []
            window.perform_long_operation(image_processor.rotate_right, end_key='rotate_right')

        if event == consts.key_rot_left_90:
            img_for_editing = cv2.rotate(img_for_editing, cv2.ROTATE_90_COUNTERCLOCKWISE)
            img_edit_window[consts.key_graph].erase()
            img_edit_window[consts.key_graph].draw_image(data=cv2.imencode('.png', img_for_editing)[1].tobytes(),
                                                         location=(0, consts.graph_width))
            crop_point_list = []
            crop_point_id_list = []
            window.perform_long_operation(image_processor.rotate_left, end_key='rotate_left')

        # ------------------------------------------------------------------------------------------------------------
        #                 TODO THRESHOLDING
        # --------------------------------------------------------------------------------------------------------------

        if event == consts.key_thresh_meanc:
            block, const, t_win, s_win, h_value = config_helps.get_thresh_input_data(values)
            img_edit_window[consts.key_graph].erase()
            img_edit_window[consts.key_graph].draw_image(
                data=cv2.imencode('.png', image_processor.adaptive_threshold_meanc(img_for_editing, block, const, t_win,
                                                                                   s_win, h_value))[1].tobytes(),
                location=(0, consts.graph_width))
            threshold = (consts.key_thresh_meanc, block, const, t_win, s_win, h_value)
            brightness = contrast = 1

        if event == consts.key_thresh_meanc_inv:
            data = config_helps.get_thresh_input_data(values)  # test TODO
            block, const, t_win, s_win, h_value = config_helps.get_thresh_input_data(values)
            img_edit_window[consts.key_graph].erase()
            img_edit_window[consts.key_graph].draw_image(
                data=cv2.imencode('.png', image_processor.adaptive_threshold_meanc_inverse
                (img_for_editing, block, const, t_win, s_win, h_value))[1].tobytes(),
                location=(0, consts.graph_width))
            threshold = (consts.key_thresh_meanc_inv, block, const, t_win, s_win, h_value)
            brightness = contrast = 1
            config_helps.set_user_data_to_config_file(data)  # Test TODO

        if event == consts.key_thresh_gauss:
            block, const, t_win, s_win, h_value = config_helps.get_thresh_input_data(values)
            img_edit_window[consts.key_graph].erase()
            img_edit_window[consts.key_graph].draw_image(
                data=cv2.imencode('.png',
                                  image_processor.adaptive_threshold_guassian_c(img_for_editing, block, const, t_win,
                                                                                s_win, h_value))[
                    1].tobytes(),
                location=(0, consts.graph_width))
            threshold = (consts.key_thresh_gauss, block, const, t_win, s_win, h_value)
            brightness = contrast = 1

        if event == consts.key_thresh_gauss_inv:
            block, const, t_win, s_win, h_value = config_helps.get_thresh_input_data(values)
            img_edit_window[consts.key_graph].erase()
            img_edit_window[consts.key_graph].draw_image(
                data=cv2.imencode('.png',
                                  image_processor.adaptive_threshold_guassian_c_inverse(
                                      img_for_editing, block, const, t_win, s_win, h_value))[
                    1].tobytes(),
                location=(0, consts.graph_width))
            threshold = (consts.key_thresh_gauss_inv, block, const, t_win, s_win, h_value)
            brightness = contrast = 1

        # --------------------------------------------------------------------------------------------------------------
        #                                    TODO RECAPTURE
        # -----------------------------------------------------------------------------------------------------------

        # 1. close the edit window and open the main window
        # 2. set recapture to True
        #     set image capture count to the net number
        # 3. while capture add the image to row 3 and recapture list
        # 4. on save all hide the img from col 3 using the key from recapture_list and set recapture to false and
        #    clear the recapture_img_list

        if event == consts.key_capture_again:  # when user click to take photo of a page o  f the selected doc
            result = my_popups.yes_no_popup('Do You want to take picture again', 'Capture')
            if result == 'Yes':
                recapture = True
                img_edit_window.close()
                img_edit_window = None
                current_doc_no = current_doc.get_doc_number()
                image_caputr_count = current_doc.get_page_count()
                main_window[consts.key_col3_raw_img_thump_col].contents_changed()
                main_window[consts.key_save_all_raw_img_btn].update(disabled=False)

        # ---------------------------------------------------------------------------------------------------------------
        #                                           TODO SAVING AND PDF
        # --------------------------------------------------------------------------------------------------------------

        if event == consts.key_save_processed_img:
            if not consts.current_image_obj.is_cropped():
                my_popups.ok_error_popup('Please crop the document first and continue', 'error')
            else:
                waiting_window = my_popups.waiting_window()
                r_code = image_processor.save_changes_single_img(img_for_editing, current_doc, current_image_index,
                                                                 brightness, contrast, threshold)
                if r_code == 1:
                    database_class.set_process_start(db_connection, current_doc_no)
                    current_doc.set_process_started()
                    waiting_window.close()
                    waiting_window = None
                    my_popups.no_btn_success_popup('Image saved successfully')
                else:
                    waiting_window.close()
                    waiting_window = None
                    my_popups.no_btn_error_popup("Sorry \n I Can't complete the process now \n Please Try again")

        if event == consts.key_save_all_processed_img:
            non_cropped_list = []
            for img in current_doc.get_raw_img_obj_list():
                if not img.is_cropped():
                    non_cropped_list.append(img.get_page_number())
            if len(non_cropped_list) != 0:
                my_popups.ok_error_popup(
                    f'The following page are not cropped\nPage Numbers:-{non_cropped_list}\nPlease do cropping '
                    f'and try again', 'Saving')
            else:
                waiting_window = my_popups.waiting_window()
                image_processor.save_all_img(current_doc, brightness, contrast, threshold)
                current_doc.set_process_completed(True)
                database_class.set_process_cmplete(db_connection, current_doc_no)
                waiting_window.close()
                waiting_window = None
                my_popups.no_btn_success_popup('All Image saved successfully')

        if event == consts.key_create_doc:
            # window.perform_long_operation(image_processor.create_pdf_from_img(current_doc.get_raw_image_list(), current_doc_no), end_key=1)
            r_code = image_processor.create_pdf_from_img(current_doc.get_raw_image_list(), current_doc_no)
            if r_code:
                waiting_window = my_popups.waiting_window()
                database_class.set_pdf(db_connection, current_doc_no)
                current_doc.set_document_created(True)
                waiting_window.close()
                waiting_window = None

        if event == consts.key_del_entire_doc:
            result = my_popups.yes_no_popup('Do You want to delete the document ', 'Deletion')
            if result == 'Yes':
                database_class.del_doc_from_primaryTb(db_connection, current_doc_no)

        # ---------------------------------------------------------------------------------------------------------------
        #                                           TODO MENU ITEMS
        # --------------------------------------------------------------------------------------------------------------

        if event == consts.key_menu_view_docs:
            menu_alldoc_view_win = create_menu_doc_view_win()
            for doc in database_class.get_doc_from_primary(db_connection):
                pagecount = menu_helper.get_page_count_for_menu(document_list, doc[0])
                menu_alldoc_view_win.extend_layout(menu_alldoc_view_win[consts.key_menu_column],
                                                   add_doc_to_menu(doc, pagecount))
            menu_alldoc_view_win.refresh()
            menu_alldoc_view_win[consts.key_menu_column].contents_changed()
        if event == consts.key_menu_view_generated_doc:
            try:
                data = [[doc[0], doc[1], doc[2]] for doc in database_class.get_docs_from_final_table(db_connection)]
                menu_generated_doc_win = create_generated_document_window(data)
            except:
                my_popups.no_btn_success_popup('Sorry, No data found to display')

        if event == consts.key_menu_about:
            about_window = about.create_about_win()
            about_window[consts.url_sg].set_cursor('hand2')
            about_window[consts.url_cv].set_cursor('hand2')
            about_window[consts.url_mutils].set_cursor('hand2')
            about_window[consts.url_winapp].set_cursor('hand2')
            about_window[consts.url_pdf].set_cursor('hand2')
            about_window[consts.url_pillow].set_cursor('hand2')
            about_window[consts.url_digicam].set_cursor('hand2')
            about_window[consts.url_pearl].set_cursor('hand2')
            about_window[consts.url_watsaspp].set_cursor('hand2')
        try:
            if event.startswith('http'):
                waiting_window = my_popups.waiting_window('Opening')
                os.system(F"start \"\" {event}")
                waiting_window.close()
                waiting_window = None
        except:
            pass

        if event == consts.key_menu_read_file:
            # file_browser_win = file_browse.create_file_browse_win()
            file_path = sg.PopupGetFile(message='Select a file', initial_folder='Downloads',
                                        keep_on_top=True, modal=True,
                                        file_types=(
                                            ("Excel files", "*.xlsx",), ("CSV Files", "*.csv"),
                                            ("Excel files", "*.xls",))
                                        )
            if file_path:
                add_doc_helper.get_doc_from_file(file_path, document_list, db_connection, hided_doc_list, main_window, )
            print(file_path)
            # file_name = values[consts.key_file_path]
            # print(file_name)

        # -----------------------------------------------------------------------------------------------------------
        #                                           TODO PAGE NO EDITING
        # -----------------------------------------------------------------------------------------------------------

        if event == consts.key_edit_page_no:
            img_edit_window.close()
            img_edit_window = None
            img_view_window = create_img_view_window()
            graph_img_helper.draw_graph_img(img_view_window, consts.key_img_view_graph,
                                            current_doc.get_raw_image_by_index(0), current_doc)
            graph_img_helper.graph_header_update(img_view_window, current_doc_no, 1, current_doc.get_page_count())
            current_image_index = 0
            all_page = current_doc.get_page_count()
            for page in range(1, all_page + 1):
                img_view_window.extend_layout(img_view_window[consts.key_page_editlist_col], add_page_edit_box(page))
            img_view_window.refresh()
            img_view_window[consts.key_page_editlist_col].contents_changed()

        if event == consts.key_save_page_no:
            total_page = current_doc.get_page_count()
            edited_page_no = 0
            invalid_page = []

            for i in range(total_page):
                edited_page_no = values[consts.key_page_no + str(i + 1)]
                if not edited_page_no.isnumeric():
                    invalid_page.append(edited_page_no)

                elif int(edited_page_no) > total_page:
                    invalid_page.append(edited_page_no)

                elif edited_page_no == str(0):
                    invalid_page.append(edited_page_no)

                else:
                    if edited_page_no != current_doc.get_page_number_from_img_at_index(i):
                        current_doc.set_page_number_of_img(i, int(edited_page_no))
            if not invalid_page:
                my_popups.no_btn_success_popup('Page number saved successfully', )
                current_doc.sort_raw_image_list()
            else:
                my_popups.ok_error_popup(
                    F"{invalid_page} {'is' if len(invalid_page) == 1 else 'are'} incorrect page number ", 'Page No.')

        # starting from left . after one side completed again from left
        if event == consts.key_page_edit_lrlr:
            total_page = current_doc.get_page_count()
            first_half_start = 0
            second_half_start = 0
            if (total_page - 1) % 2 == 0:
                first_half_start = 2
                second_half_start = int((total_page - 1) / 2) + 2
            elif (total_page - 2) % 2 == 0:
                first_half_start = 2
                second_half_start = int((total_page - 1) / 2) + 2
            for img in current_doc.get_raw_img_obj_list():
                page_no = img.get_page_number()
                # print('selected page Number', page_no)
                if page_no != 1:
                    # print(f'The crrent Page no is -{page_no}')
                    if page_no % 2 == 0:
                        img.set_page_no(second_half_start)
                        img_view_window[consts.key_page_no + str(page_no)].update(str(second_half_start))
                        # print(f'the page{page_no} set to {second_half_start}')
                        second_half_start += 1

                    else:
                        img.set_page_no(first_half_start)
                        img_view_window[consts.key_page_no + str(page_no)].update(str(first_half_start))
                        # print(f'the page{page_no} set to {first_half_start}')
                        first_half_start += 1
            img_view_window[consts.key_img_view_graph].erase()
            graph_img_helper.draw_graph_img(img_view_window, consts.key_img_view_graph,
                                            current_doc.get_raw_image_by_index(0), current_doc)
            graph_img_helper.graph_header_update(img_view_window, current_doc_no,
                                                 current_doc.get_page_number_from_img_at_index(0),
                                                 current_doc.get_page_count())

        # starting from first page . after completing one side next starting form last page
        if event == consts.key_page_edit_lrrl:
            total_page = current_doc.get_page_count()
            first_half_start = 2
            second_half_start = int((total_page - 1) / 2) + 2

        # -----------------------------------------------------------------------------------------------------------
        #                                           TODO  view original image
        # -------------------------------------------------------------------------------------------------------------
        if event == consts.key_View_original_img:
            img_path = current_doc.get_raw_image_by_index(current_image_index)
            img_for_editing = original_img_provider.get_org_img(img_path)
            img_edit_window[consts.key_graph].erase()
            graph_img_helper.draw_graph_img(img_edit_window, consts.key_graph,
                                            consts.current_graph_image_path,
                                            current_doc)
            img_edit_window[consts.key_crop_btn].update(disabled=True)
            img_edit_window[consts.key_crop_selct_point].update(disabled=False)
            crop_point_list = []
            crop_point_id_list = []
            crop_point_line_id_list = []
            reset_for_next_and_prev()
            cropped = False
            consts.current_image_obj.set_cropped(False)
            consts.current_image_obj.set_process_completed(False)
            btn_enable_disable.disable_edit_win_btn(img_edit_window)

        # -----------------------------------------------------------------------------------------------------------
        #                                           TODO CC GENERATION
        # -------------------------------------------------------------------------------------------------------------

        if event == consts.key_generate_CC:
            if current_doc.get_is_document_created():
                result = sg.PopupYesNo(F'Do You want to generate CC for : {current_doc_no} ..?',
                                       title='Generating Doc',
                                       text_color=consts.popup_text_color,
                                       keep_on_top=True,
                                       background_color=consts.popup_back_color)
                if result == 'Yes':
                    waiting_window = my_popups.waiting_window()
                    current_doc.set_document_created(True)
                    rcode, path = image_processor.document_generation(current_doc.get_raw_image_list(), current_doc_no)
                    if rcode:
                        database_class.del_doc_from_primaryTb(db_connection, current_doc_no)
                        database_class.add_doc_to_final_tb(db_connection, current_doc_no)
                        main_window[consts.key_doc_number_holder_frame_offset + current_doc_no].hide_row()
                        if not is_doc_genration_list:
                            list_of_doc_for_generation = [doc for doc in document_list if
                                                          doc.get_is_capture_completed()]
                            is_doc_genration_list = True
                        current_doc_index = list_of_doc_for_generation.index(current_doc)
                        document_list.remove(current_doc)
                        list_of_doc_for_generation.remove(current_doc)

                        if len(list_of_doc_for_generation) == 0:
                            img_edit_window.close()
                            current_doc = set_curent_document
                            current_doc_no = None
                            main_window[consts.key_disply_selected_doc].update(value='')
                            is_doc_genration_list = False
                            list_of_doc_for_generation = []
                            current_image_index = 0
                            waiting_window.close()
                            waiting_window = None
                            my_popups.no_btn_success_popup(f'Document generated successfully \n\n Location: {path}',
                                                           duration=1.5)
                        else:
                            if current_doc_index == len(list_of_doc_for_generation):
                                current_doc_index -= 1

                            current_doc = list_of_doc_for_generation[current_doc_index]
                            current_doc_no = current_doc.get_doc_number()
                            current_image_index = 0
                            img_edit_window[consts.key_graph].erase()
                            img_for_editing = graph_img_helper.draw_graph_img(img_edit_window, consts.key_graph,
                                                                              current_doc.get_raw_image_by_index(
                                                                                  0), current_doc)
                            graph_img_helper.graph_header_update(img_edit_window, current_doc_no,
                                                                 current_doc.get_page_number_from_img_at_index(
                                                                     0), current_doc.get_page_count())
                            waiting_window.close()
                            waiting_window = None
                            my_popups.no_btn_success_popup(
                                f'\nDocument generated successfully\n\nLocation:{path}\n\nThe Document  [ {current_doc_no} ] Selected for '
                                f'processing \n', duration=2)
                            img_edit_window[consts.key_crop_selct_point].update(disabled=False)
                            cropped = False
                            crop_point_list = []
                            img_edit_window[consts.key_bright_control].update(value=1)
                            img_edit_window[consts.key_contrast_control].update(value=1)
                            threshold = ()


                    else:
                        my_popups.ok_error_popup('Please close the existing pdf of this document and try again',
                                                 'error')
            else:
                my_popups.ok_error_popup('Please preview the PDF  before creating document', 'Document creation')

        # ------------------------------------------------------------------------------------------------------------
        #                                     TODO CLOSING WINDOWS
        # ------------------------------------------------------------------------------------------------------
        if event == consts.key_img_edit_win_close:
            result = my_popups.yes_no_popup('Do You really want to close the window....', title='Exiting', )
            if result == 'Yes':
                current_doc = set_curent_document
                current_doc_no = None
                current_doc_index = None
                is_doc_genration_list = False
                list_of_doc_for_generation = []
                main_window[consts.key_disply_selected_doc].update(value='')
                page_no = 1
                crop_point_list = []
                crop_point_id_list = []
                img_edit_window.close()
                cropped = False
                brightness = 1
                contrast = 1
                threshold = []
                img_edit_window.close()
                img_edit_window = None

        if event == consts.key_img_view_win_close:
            result = my_popups.yes_no_popup('Do You really want to close the window....', title='Exiting', )
            print(result)
            if result == 'Yes':
                current_image_index = 0
                page_no = 0
                img_view_window.close()
                if img_edit_window is not None:
                    img_edit_window.force_focus()
                    img_edit_window[consts.key_graph].erase()
                    img_for_editing = graph_img_helper.draw_graph_img(img_edit_window, consts.key_graph,
                                                                      current_doc.get_raw_image_by_index(
                                                                          0), current_doc)
                    graph_img_helper.graph_header_update(img_edit_window, current_doc_no,
                                                         current_doc.get_page_number_from_img_at_index(0),
                                                         current_doc.get_page_count())

        if event == consts.key_menu_all_doc_win_close:
            result = my_popups.yes_no_popup('Do You really want to close the window....', title='Exiting', )
            if result == 'Yes':
                menu_alldoc_view_win.close()
        if event == consts.key_btn_add_doc_close:
            doc_input_win.close()

        if event == consts.key_menu_gerated_doc_win_close:
            result = my_popups.yes_no_popup('Do You really want to close the window....', title='Exiting', )
            if result == 'Yes':
                menu_generated_doc_win.close()
        if event == consts.key_about_close:
            about_window.close()

    window.close()


if __name__ == "__main__":
    main()
