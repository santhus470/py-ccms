import os
import platform
import shutil
import time

import imutils
import PySimpleGUI as sg
import cv2

import helper.page_editor
from data_classes import database_class, my_themes
from data_classes.document import Document, CapturedImages
from helper import consts, image_processor, video_capture, graph_img_helper, menu_helper, add_doc_helper
from layouts import primary_window, camera_related_layout, my_popups
from layouts.document_number_input_popup import popup_document_input_receiver
from layouts.image_editor_layout import image_editing_window
from layouts.image_view import create_img_view_window
from layouts.laout_extender import add_img_list_to_col3, add_doc_to_menu, add_doc_edit_pages
from layouts.menu_doc_all_view import create_menu_doc_view_win
from layouts import my_popups
from assets import gifs, icons_dark

# from pygrabber.dshow_graph import FilterGraph    TODO Enable for windows


sg.theme_add_new('my_dark', my_themes.blue_grey_theme_dark)
sg.theme_add_new('my_light1', my_themes.blue_grey_theme_light1)
sg.theme_add_new('my_light2', my_themes.blue_grey_theme_light2)
sg.theme('my_dark')

cap = ''
# document_list = []
captured_doc_list = []


def main():
    my_popups.waiting_window(gifs.main_gif)
    db_connection = database_class.connect()
    database_class.create_primary_table(db_connection)
    database_class.create_final_table(db_connection)
    # database_class.del_doc_from_primaryTb(db_connection, '77-1-2020')
    global img_for_editing
    camera_index = 0
    cap = None
    current_doc_no = None
    set_curent_document = Document('01/01/0101')
    current_doc = set_curent_document
    image_caputr_count = 0
    page_no = 0
    frame = ''
    recording = False
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
    img_for_view = ''
    cam_dict = {}


    main_window, doc_input_win, img_edit_window, img_view_window, \
    cam_select_win, camera_start_win, recap_win, menu_alldoc_view_win, my_pop, page_edit_win = primary_window.main_window(), None, None, None, None, None, None, None, None, None
    document_list = add_doc_helper.get_document_from_db(db_connection, main_window)
    sg.popup_animated(None, )
    while True:

        window, event, values = sg.read_all_windows(timeout=20)

        if event == sg.WINDOW_CLOSED or event == 'Cancel' or event == '-CLOSE-' or event is None:
            window.close()
            if window == doc_input_win:
                doc_input_win = None
            if window == img_edit_window:
                img_edit_window = None
            if window == img_view_window:
                img_view_window = None
            if window == cam_select_win:
                cam_select_win = None
            if window == camera_start_win:
                camera_start_win = None
            if window == menu_alldoc_view_win:
                menu_alldoc_view_win = None
            if window == my_pop:
                my_pop = None
            if window == page_edit_win:
                page_edit_win = None
            elif window == main_window:
                break
        main_window[consts.key_btn_add_doc].bind("<Return>", "_Enter")
        if event == consts.key_start_camera:
            if not recording:
                cam_dict = video_capture.camera_selector() 
                cam_dict = {'Camera': 1}
                if cam_dict:
                    cam_select_win = camera_related_layout.create_cam_select_win(list(cam_dict.keys()))
                else:
                    my_popups.ok_error_popup('No connected camera found. Please try..', title='camera')

        if event == consts.key_camera_select_ok:
            
            selected_cam = values[consts.key_availabele_camera]
            camera_index = cam_dict[selected_cam]
            # camera_index = 0
            recording = True
            cam_select_win.close()
            try:
                camera_start_win = camera_related_layout.camera_start_info_win()
                cap = cv2.VideoCapture(camera_index)
                # print('cap is ', cap.isOpened())
                cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)  # disable Autofocus
                camera_start_win.close()
            except:
                recording = False
                my_popups.ok_success_popup('Please switch on the camera......', title='Camera ')

        if recording:
            try:
                ret, frame = cap.read()
                # frame = imutils.resize(frame, width=800)
                # consts.init_img_height = frame.shape[1]
                # frame = frame[0:720, 100:1180]
                frame = imutils.resize(frame, width=750)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                main_window[consts.key_video_view_disply].update(data=cv2.imencode('.png', frame)[1].tobytes())

            except:
                recording = False
                my_popups.ok_success_popup('cannot open camera, Please try again', title='Camera Error', )

        if event == consts.key_btn_add_doc:
            doc_input_win = popup_document_input_receiver()
            doc_input_win[consts.key_doc_input_doc].set_focus()

        if event == consts.key_btn_add_doc_save:
            add_doc_helper.save_document_no(values, document_list, main_window, db_connection)
            doc_input_win[consts.key_doc_input_doc].set_focus()
            print(database_class.get_doc_from_primary(db_connection))

        #  this method calls when a user click on one of the document listed in the first col
        #  when user click the document , the event is itself and chek for the document list
        #  if the selected documents is_capture_completed property is true it means that the images are captured and
        #  user selected it for editing. so the image editing window will appear  other wise it is for capturing image so this document
        # is selected as the current document and ready to capture the image for the selected document

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
                                                 add_img_list_to_col3(key=img, image=cv2.imread(img),
                                                                      doc_num=current_doc_no, page_no=count))
                    else:
                        for frame_count in range(image_caputr_count):
                            main_window[consts.key_raw_img_thump_holder_frame_offset
                                        + current_doc.get_raw_image_by_index(frame_count)].unhide_row()
                    window[consts.key_col3_raw_img_thump_col].contents_changed()
                    window.refresh()
                elif not current_doc.get_is_capture_started():
                    image_caputr_count = 0
                    main_window[consts.key_disply_selected_doc].update(current_doc_no)
                    main_window.ding()

                elif current_doc.get_is_capture_completed():
                    img_edit_window = image_editing_window()
                    current_image_index = 0
                    img_for_editing = graph_img_helper.prepare_graph_for_editing(img_edit_window, current_doc)
                    sg.popup_animated(None)

            else:
                if event != current_doc_no:
                    # if not current_doc.get_is_process_statred() and (document_list[document_list.index(event)].get_is_capture_started() and not document_list[document_list.index(event)].get_is_capture_completed()):
                    if not current_doc.get_is_capture_started() or current_doc.get_is_capture_completed():
                        current_doc = document_list[document_list.index(event)]
                        current_doc_no = current_doc.get_doc_number()
                        # main_window[consts.key_disply_selected_doc].update(current_doc_no)
                        # main_window.ding()
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
                                                         add_img_list_to_col3(key=img, image=cv2.imread(img),
                                                                              doc_num=current_doc_no, page_no=count))
                            else:
                                for frame_count in range(image_caputr_count):
                                    main_window[consts.key_raw_img_thump_holder_frame_offset +
                                                current_doc.get_raw_image_by_index(frame_count)].unhide_row()

                        if current_doc.get_is_capture_completed():
                            my_popups.waiting_window(gifs.saving_gif2)
                            img_edit_window = image_editing_window()
                            current_image_index = 0
                            img_for_editing = graph_img_helper.prepare_graph_for_editing(img_edit_window, current_doc)
                            sg.popup_animated(None)

                    if current_doc.get_is_capture_started() and not current_doc.get_is_capture_completed():
                        image_caputr_count = current_doc.get_page_count()
                        for frame_count in range(image_caputr_count):
                            main_window[consts.key_raw_img_thump_holder_frame_offset +
                                        current_doc.get_raw_image_by_index(frame_count)].hide_row()

                        if current_doc_no not in hided_doc_list:
                            hided_doc_list.append(current_doc_no)

                        current_doc = document_list[document_list.index(event)]
                        current_doc_no = current_doc.get_doc_number()
                        main_window[consts.key_disply_selected_doc].update(value=current_doc_no)

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
                                                         add_img_list_to_col3(key=img, image=cv2.imread(img),
                                                                              doc_num=current_doc_no, page_no=count))
                            else:
                                for frame_count in range(image_caputr_count):
                                    main_window[consts.key_raw_img_thump_holder_frame_offset +
                                                current_doc.get_raw_image_by_index(frame_count)].unhide_row()
                            window[consts.key_col3_raw_img_thump_col].contents_changed()
                            window.refresh()

                        if current_doc.get_is_capture_completed():
                            my_popups.waiting_window(gifs.saving_gif2)
                            current_image_index = 0
                            img_edit_window = image_editing_window()
                            img_for_editing = graph_img_helper.prepare_graph_for_editing(img_edit_window, current_doc)
                            window[consts.key_col3_raw_img_thump_col].contents_changed()
                            window.refresh()
                            sg.popup_animated(None)

                elif event == current_doc_no:
                    if current_doc.get_is_capture_completed():
                        my_popups.waiting_window(gifs.saving_gif2)
                        current_image_index = 0
                        img_edit_window = image_editing_window()
                        img_for_editing = graph_img_helper.prepare_graph_for_editing(img_edit_window, current_doc)
                        sg.popup_animated(None)

        if event == consts.key_preview:
            im_captured , img_path = video_capture.capture_img(current_doc_no,image_caputr_count)
            cv2.imshow('Preview', im_captured )
            

        if event == consts.key_capture_image:
            im_captured, img_path = video_capture.capture_img(current_doc_no, image_caputr_count)
            # cv2.imshow('Preview', im_captured)

            # frame = cv2.cvtColor(frame,cv2.C)
            frame = imutils.resize(im_captured, width=750)
            main_window[consts.key_video_view_disply].update(data=cv2.imencode('.png', frame)[1].tobytes())
            # if current_doc_no is not None:
            #     if recording:
            #         img_name = '{}-{}.png'.format(current_doc_no, image_caputr_count)
            #         current_document_path = os.path.join(consts.raw_image_directory, current_doc_no)
            #         if not os.path.exists(current_document_path):
            #             os.mkdir(current_document_path)
            #         cv2.imwrite(filename=os.path.join(current_document_path, img_name), img=frame)
            #         window.extend_layout(window[consts.key_col3_raw_img_thump_col],
            #                              add_img_list_to_col3(key=os.path.join(current_document_path, img_name),
            #                                                   image=frame, doc_num=current_doc_no,
            #                                                   page_no=image_caputr_count))
            #         window[os.path.join(current_document_path, img_name)].set_cursor(cursor='hand2', cursor_color='red')
            #
            #         current_doc.add_raw_image(
            #             CapturedImages(os.path.join(current_document_path, img_name)))
            #         image_caputr_count += 1
            #         main_window[consts.key_col3_raw_img_thump_col].contents_changed()
            #         window.refresh()
            #
            #         if not current_doc.get_is_capture_started():
            #             database_class.set_capture_start(db_connection, current_doc_no)
            #             current_doc.set_capture_started()
            #
            #         if not is_raw_img_save_all_btn_enabled:
            #             main_window[consts.key_save_all_raw_img_btn].update(disabled=False)
            #
            #     else:
            #         my_popups.ok_error_popup('Please check the camera..... ', title='Stop', )
            # else:
            #     my_popups.ok_error_popup('Select a document first ', title='Stop')

        if event == consts.key_save_all_raw_img_btn:  # when the user click on the save all button in col3
            #     what will happen here is
            #  first confirm the user to save the details by  a popup
            # 1.clear the colum3 - delete the list of all raw image
            # 2.clear the selected image for capturing (camera heading)
            # 3. delete the document number from the document list column(column 1)
            # 4. set the capture_complete to True in the current document
            # 6. set this button to disabled
            # 7. add the document to the 7th column- thats capture completed Documents
            result = sg.popup_yes_no('Do you take all the image of  this document', title='Image', keep_on_top=True,
                                     modal=True, background_color=consts.popup_back_color)
            print(result)

            if result == 'Yes':
                for frame_count in range(current_doc.get_page_count()):
                    main_window[consts.key_raw_img_thump_holder_frame_offset +
                                current_doc.get_raw_image_by_index(frame_count)].hide_row()

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

        if event == consts.key_img_edit_win_close:
            result = sg.PopupYesNo('Do You really want to exit....', title='Exiting..', keep_on_top=True, modal=True,
                                   background_color=consts.popup_back_color
                                   )
            print(result)
            if result == 'Yes':
                current_doc = set_curent_document
                current_doc_no = None
                current_doc_index = None
                is_doc_genration_list = False
                list_of_doc_for_generation = []
                main_window[consts.key_disply_selected_doc].update(value='')
                img_edit_window.close()

        if event in current_doc.get_raw_image_list():
            # this method called when a user click on any of the img in the col3
            #  what will happen when a user clik on the image
            # 1. release the camera
            # 2. make recording false
            # 3. set the image editor view not none
            # 4. set the current document to the selected document
            # 4. set the image of the graph to the selected image - this may be
            # 5. set the current index to the index position of selected image
            # 6. see the header of this document view with document number and page number
            if cap is not None:
                cap.release()
            recording = False
            page_no = current_doc.get_page_number_of_image(event)
            current_image_index = current_doc.get_index_of_raw_img(event)
            img_view_window = create_img_view_window()
            img_for_view = graph_img_helper.draw_graph_img(img_view_window, consts.key_img_view_graph, event)
            graph_img_helper.graph_header_update(img_view_window,
                                                 current_doc_no,
                                                 page_no, current_doc.get_page_count())

            img_view_window[consts.key_page_no].update(value=str(page_no))

        if event == consts.key_img_view_next:  # when user click on the next button on the imgae_view_window
            page_count = current_doc.get_page_count() - 1
            if current_image_index < page_count:
                current_image_index = current_image_index + 1
                if window == img_view_window:
                    page_no = current_doc.get_page_number_from_img_at_index(current_image_index)
                    img_view_window[consts.key_img_view_graph].erase()
                    graph_img_helper.draw_graph_img(window=img_view_window, key=consts.key_img_view_graph,
                                                    image_path=current_doc.get_raw_image_by_index(
                                                        current_image_index))

                    graph_img_helper.graph_header_update(img_view_window, current_doc_no, page_no,
                                                         current_doc.get_page_count())
                    img_view_window[consts.key_page_no].update(value=str(page_no))

                if window == img_edit_window:
                    img_edit_window[consts.key_graph].erase()
                    img_for_editing = graph_img_helper.draw_graph_img(img_edit_window, consts.key_graph,
                                                                      current_doc.get_raw_image_by_index(
                                                                          current_image_index))
                    graph_img_helper.graph_header_update(img_edit_window, current_doc_no,
                                                         current_doc.get_page_number_from_img_at_index(
                                                             current_image_index), current_doc.get_page_count())

                    img_edit_window[consts.key_crop_selct_point].update(disabled=False)
                    cropped = False
                    crop_point_list = []

        if event == consts.key_img_view_prev:
            page_count = current_doc.get_page_count() - 1
            if current_image_index <= page_count and current_image_index != 0:
                current_image_index = current_image_index - 1
                if window == img_view_window:
                    img_view_window[consts.key_img_view_graph].erase()
                    page_no = current_doc.get_page_number_from_img_at_index(current_image_index)
                    graph_img_helper.draw_graph_img(window=img_view_window, key=consts.key_img_view_graph,
                                                    image_path=current_doc.get_raw_image_by_index(
                                                        current_image_index))
                    graph_img_helper.graph_header_update(img_view_window, current_doc_no,
                                                         current_doc.get_page_number_from_img_at_index(
                                                             current_image_index), current_doc.get_page_count())
                    img_view_window[consts.key_page_no].update(value=str(page_no))
                if window == img_edit_window:
                    img_edit_window[consts.key_graph].erase()
                    img_for_editing = graph_img_helper.draw_graph_img(img_edit_window, consts.key_graph,
                                                                      current_doc.get_raw_image_by_index(
                                                                          current_image_index))
                    graph_img_helper.graph_header_update(img_edit_window, current_doc_no,
                                                         current_doc.get_page_number_from_img_at_index(
                                                             current_image_index), current_doc.get_page_count())
                    img_edit_window[consts.key_crop_selct_point].update(disabled=False)
                    cropped = False
                    crop_point_list = []

        if event == consts.key_img_view_del:
            result = sg.PopupYesNo('Do You really want to Delete  This image', title='Deleting', keep_on_top=True,
                                   modal=True, background_color=consts.popup_back_color)
            if result == 'Yes':
                page_count = current_doc.get_page_count()
                if current_image_index == 0 and page_count == 1:  # if only one image in the list
                    # 1. clear the image list column- column3
                    # 3. clear the current document in process to none
                    # 4.delete the folder form the raw_image
                    # 5. clear the document list
                    # 6. make the image_list to empty
                    # 7. make the saveAll button n the col3 to disable
                    # TODO  when trying to delete the image which is capture afresh after
                    #  deleting an image , all but No 1 is not working need to clear this BUG

                    # the key of the entire frame that hold a single image is se as
                    #  key=consts.key_raw_img_thump_holder_frame_offset + str(page_no)
                    #  note that the page number starts with 1
                    #  here we add 1 to the key offset becoze the is only one image in this case
                    if window == img_view_window:
                        main_window[consts.key_raw_img_thump_holder_frame_offset + current_doc.get_raw_image_by_index(
                            0)].hide_row()
                        # os.remove(current_doc.get_raw_image_list()[0])
                        try:
                            shutil.rmtree(os.path.join(consts.raw_image_directory, current_doc_no))
                        except OSError as e:
                            sg.PopupOK(title='cant remove this ', keep_on_top=True)
                        document_list.remove(current_doc)
                        current_doc.clear_img_list()
                        current_doc_no = None
                        current_doc = set_curent_document
                        main_window[consts.key_disply_selected_doc].update(value=None)
                        main_window[consts.key_save_all_raw_img_btn].update(disabled=True)
                        database_class.del_doc_from_primaryTb(db_connection, current_doc_no)
                        img_view_window.close()
                    if window == img_edit_window:
                        print('cannot delete the image')
                else:  # if more than one imgae
                    # 1.clear it from the 3rd row
                    # 2. delete  the image from the folder
                    # 3. delete it from the document list
                    # 4.TODO - need to implement when image_view index == 0
                    # todo now it have some bugs
                    if window == img_view_window:
                        main_window[
                            consts.key_raw_img_thump_holder_frame_offset +
                            current_doc.get_raw_image_by_index(current_image_index)
                            ].hide_row()
                        current_doc.remove_raw_img_by_index(current_image_index)  # 2 and

                        if current_image_index == 0:
                            current_image_index = current_image_index + 1
                        current_image_index = current_image_index - 1
                        print('current index ', current_image_index)
                        graph_img_helper.draw_graph_img(img_view_window, consts.key_img_view_graph,
                                                        current_doc.get_raw_image_by_index(current_image_index))
                        graph_img_helper.graph_header_update(img_view_window, current_doc_no,
                                                             current_doc.get_page_number_from_img_at_index(
                                                                 current_image_index), current_doc.get_page_count())
                    if window == img_edit_window:
                        print('cannot delete image')

        if event == consts.key_img_view_win_close:
            result = sg.PopupYesNo('Do You really want to close the window....', title='Exiting', keep_on_top=True,
                                   modal=True, background_color=consts.popup_back_color)
            if result == 'Yes':
                current_image_index = 0
                page_no = 0
                img_view_window.close()

        if event == consts.key_menu_all_doc_win_close:
            result = sg.PopupYesNo('Do You really want to close the window....', title='Exiting', keep_on_top=True,
                                   modal=True, background_color=consts.popup_back_color)
            if result == 'Yes':
                menu_alldoc_view_win.close()

        if event.startswith(consts.key_del_doc_frm_col_1):  # when a user click on the delete button in the doc
            # 1.inform the user they realy want to delete the document
            # 2 if yes delete the document from list
            # 3. set the selected document for capture to '' if it selected for
            # 4 remove the document from the document list
            # 5. remove the frame that hold this document
            # TODO if a user first delete a document from col 1 after taking some image - the program will crash
            print(event)
            try:
                doc_no = event.split('_')[1]
                if doc_no:

                    confirm = my_popups.ok_cancel_popup(F'Do you wish to delete  Document.....-{doc_no}', 'Deleting')

                    if confirm == 'OK':
                        main_window[event].hide_row()
                        document_list.remove(doc_no)
                        try:
                            database_class.del_doc_from_primaryTb(db_connection, doc_no)
                            main_window[
                                consts.key_doc_number_holder_frame_offset + doc_no].hide_row()
                        except:
                            my_popups.ok_error_popup('\n Cannot access database now.  Please Try again\n'
                                                     'or restart the application to effect the same .Thanks',
                                                     'deleting')
                        if os.path.exists(os.path.join(consts.raw_image_directory, doc_no)):
                            shutil.rmtree(os.path.join(consts.raw_image_directory, doc_no))
                        if current_doc_no == doc_no:
                            current_doc_no = None
                            main_window[consts.key_disply_selected_doc].update(value='')


            except:
                my_popups.ok_error_popup('Cannot delete now. Please Try again', title='deleting')

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
                    crop_point_list.append([x, 750 - y])
                    crop_point_id_list.append(circle_id)
                    if len(crop_point_list) > 1:
                        line_id = window[consts.key_graph].draw_line(
                            point_from=(crop_point_list[-1][0], 750 - crop_point_list[-1][1]),
                            point_to=(crop_point_list[-2][0], 750 - crop_point_list[-2][1]),
                            color='red', width=2)
                        crop_point_line_id_list.append(line_id)
                if len(crop_point_list) == 4:
                    line_id = window[consts.key_graph].draw_line(
                        point_from=(crop_point_list[0][0], 750 - crop_point_list[0][1]),
                        point_to=(crop_point_list[3][0], 750 - crop_point_list[3][1]),
                        color='red', width=2)
                    crop_point_line_id_list.append(line_id)
                    print(crop_point_list)
                    img_edit_window[consts.key_graph].set_cursor(cursor='arrow', )
                    img_edit_window[consts.key_crop_btn].update(disabled=False)
                    img_edit_window[consts.key_crop_selct_point].update(disabled=True)
                    draw_points = False

        if event == consts.key_crop_btn:  # when the user click on the crop button
            if not cropped:
                if len(crop_point_list) == 4:
                    img_for_editing = image_processor.crop_img(img_for_editing, crop_point_list)
                    img_edit_window[consts.key_graph].erase()
                    img_edit_window[consts.key_graph].draw_image(
                        data=cv2.imencode('.png', img_for_editing)[1].tobytes(), location=(0, 750))
                    crop_point_list = []
                    img_edit_window[consts.key_crop_btn].update(disabled=True)
                    img_edit_window[consts.key_crop_undo].update(disabled=False)
                    cropped = True

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
                img_for_editing = cv2.imread(current_doc.get_raw_image_by_index(current_image_index),
                                             cv2.IMREAD_GRAYSCALE)
                img_edit_window[consts.key_graph].erase()
                img_edit_window[consts.key_graph].draw_image(location=(0, 750),
                                                             data=cv2.imencode('.png', img_for_editing)[1].tobytes())
                img_edit_window[consts.key_crop_btn].update(disabled=True)
                img_edit_window[consts.key_crop_selct_point].update(disabled=False)
                crop_point_list = []
                crop_point_id_list = []
                crop_point_line_id_list = []
                cropped = False

        if event == consts.key_contrast_control:
            contrast = 1 + (values[consts.key_contrast_control] / 50)
            print('contrast-', contrast)
            img_edit_window[consts.key_graph].draw_image(
                location=(0, 750),
                data=cv2.imencode('.png', cv2.convertScaleAbs(img_for_editing, alpha=contrast, beta=brightness))
                [1].tobytes())
            threshold = ()

        if event == consts.key_bright_control:
            brightness = 1 + (values[consts.key_bright_control])
            print('brightness-', brightness)
            img_edit_window[consts.key_graph].draw_image(
                location=(0, 750),
                data=cv2.imencode('.png', cv2.convertScaleAbs(img_for_editing, alpha=contrast, beta=brightness))[
                    1].tobytes())
            threshold = ()

        if event == consts.key_rot_right_90:
            print('rotate to right90')
            img_for_editing = cv2.rotate(img_for_editing, cv2.ROTATE_90_CLOCKWISE)
            print('rotate-90 right shape of img = ', img_for_editing.shape)
            img_edit_window[consts.key_graph].erase()
            img_edit_window[consts.key_graph].draw_image(data=cv2.imencode('.png', img_for_editing)[1].tobytes(),
                                                         location=(0, 750))
        if event == consts.key_rot_left_90:
            img_for_editing = cv2.rotate(img_for_editing, cv2.ROTATE_90_COUNTERCLOCKWISE)
            img_edit_window[consts.key_graph].erase()
            img_edit_window[consts.key_graph].draw_image(data=cv2.imencode('.png', img_for_editing)[1].tobytes(),
                                                         location=(0, 750))

        # --------------------THRESHOLDING--------------------

        if event == consts.key_thresh_meanc:
            block = values[consts.key_thresh_block]
            const = values[consts.key_thresh_const]
            t_win = values[consts.key_thresh_Templ_wind]
            s_win = values[consts.key_thresh_search_wind]
            img_edit_window[consts.key_graph].erase()
            img_edit_window[consts.key_graph].draw_image(
                data=cv2.imencode('.png', image_processor.adaptive_threshold_meanc(img_for_editing, block, const, t_win,
                                                                                   s_win))[
                    1].tobytes(),
                location=(0, 750))
            threshold = (consts.key_thresh_meanc, block, const, t_win, s_win)
            brightness = contrast = 1

        if event == consts.key_thresh_meanc_inv:
            block = values[consts.key_thresh_block]
            const = values[consts.key_thresh_const]
            t_win = values[consts.key_thresh_Templ_wind]
            s_win = values[consts.key_thresh_search_wind]
            img_edit_window[consts.key_graph].erase()
            img_edit_window[consts.key_graph].draw_image(
                data=cv2.imencode('.png', image_processor.adaptive_threshold_meanc_inverse
                (img_for_editing, block, const, t_win, s_win))[1].tobytes(),
                location=(0, 750))
            threshold = (consts.key_thresh_meanc_inv, block, const, t_win, s_win)
            brightness = contrast = 1

        if event == consts.key_thresh_gauss:
            block = values[consts.key_thresh_block]
            const = values[consts.key_thresh_const]
            t_win = values[consts.key_thresh_Templ_wind]
            s_win = values[consts.key_thresh_search_wind]
            img_edit_window[consts.key_graph].erase()
            img_edit_window[consts.key_graph].draw_image(
                data=cv2.imencode('.png',
                                  image_processor.adaptive_threshold_guassian_c(img_for_editing, block, const, t_win,
                                                                                s_win))[
                    1].tobytes(),
                location=(0, 750))
            threshold = (consts.key_thresh_gauss, block, const, t_win, s_win)
            brightness = contrast = 1

        if event == consts.key_thresh_gauss_inv:
            block = values[consts.key_thresh_block]
            const = values[consts.key_thresh_const]
            t_win = values[consts.key_thresh_Templ_wind]
            s_win = values[consts.key_thresh_search_wind]
            img_edit_window[consts.key_graph].erase()
            img_edit_window[consts.key_graph].draw_image(
                data=cv2.imencode('.png', image_processor.adaptive_threshold_guassian_c_inverse(img_for_editing, block,
                                                                                                const, t_win, s_win))[
                    1].tobytes(),
                location=(0, 750))
            threshold = (consts.key_thresh_gauss_inv, block, const, t_win, s_win)
            brightness = contrast = 1

        if event == consts.key_capture_again:  # when user click to take photo of a page of the selected doc
            result = sg.PopupYesNo('Do You want to take picture again', keep_on_top=True,
                                   non_blocking=False, modal=True, background_color=consts.popup_text_color)
            print(result)
            if result == 'Yes':
                img_edit_window.close()
                current_doc_no = current_doc.get_doc_number()
                if current_doc_no not in hided_doc_list:
                    for count, img in enumerate(current_doc.get_raw_image_list()):
                        main_window.extend_layout(main_window[consts.key_col3_raw_img_thump_col],
                                                  add_img_list_to_col3(key=img, image=cv2.imread(img),
                                                                       doc_num=current_doc_no, page_no=count))
                else:
                    for frame_count in range(current_doc.get_page_count()):
                        main_window[consts.key_raw_img_thump_holder_frame_offset
                                    + current_doc.get_raw_image_by_index(frame_count)].unhide_row()
                image_caputr_count = current_doc.get_page_count()
                main_window[consts.key_col3_raw_img_thump_col].contents_changed()
                main_window[consts.key_save_all_raw_img_btn].update(disabled=False)

        if event == consts.key_save_processed_img:
            my_popups.waiting_window(gifs.saving)
            r_code = image_processor.save_changes_single_img(img_for_editing, current_doc, current_image_index,
                                                             brightness, contrast, threshold)
            database_class.set_process_start(db_connection, current_doc_no)
            sg.PopupAnimated(None)
        if event == consts.key_save_all_processed_img:
            my_popups.waiting_window(gifs.saving)
            image_processor.save_all_img(current_doc, brightness, contrast, threshold)
            current_doc.set_process_completed(True)
            database_class.set_process_cmplete(db_connection, current_doc_no)
            sg.popup_animated(None)
            sg.popup_auto_close('saved settings ', auto_close_duration=.6)

        if event == consts.key_create_doc:
            my_popups.waiting_window(gifs.saving_gif2)
            image_processor.create_pdf_from_img(current_doc.get_raw_image_list(), current_doc_no)
            database_class.set_pdf(db_connection, current_doc_no)
            current_doc.set_document_created(True)
            sg.popup_animated(None)
            sg.popup_auto_close("Pdf created Successfully  ", auto_close_duration=.6)

        if event == consts.key_view_pdf:
            image_processor.view_pdf(current_doc_no)

        if event == consts.key_del_entire_doc:
            database_class.del_doc_from_primaryTb(db_connection, current_doc_no)

        if event == consts.key_menu_view_docs:
            my_popups.waiting_window(gifs.saving)
            menu_alldoc_view_win = create_menu_doc_view_win()
            for doc in database_class.get_doc_from_primary(db_connection):
                pagecount = menu_helper.get_page_count_for_menu(document_list, doc[0])
                menu_alldoc_view_win.extend_layout(menu_alldoc_view_win[consts.key_menu_column],
                                                   add_doc_to_menu(doc, pagecount))
            sg.popup_animated(None)

        if event == consts.key_edit_page_no:
            img_view_window = create_img_view_window()
        if event == consts.key_save_page_no:
            edited_pageNo = values[consts.key_page_no]
            if edited_pageNo.isnumeric():
                current_doc.set_page_number_of_img(page_no, int(edited_pageNo))
                my_popups.ok_success_popup('New Page Number saved', 'Pages')
            else:
                my_popups.ok_error_popup(F'Incorrect page number ({edited_pageNo})', 'Page No.')
            # helper.page_editor.edit_page_number(current_doc,values)

            print(values)

        if event == consts.key_generate_CC:
            if current_doc.get_is_proess_completed() and current_doc.get_is_document_created():
                result = sg.PopupYesNo(F'Do You want to generate CC for : {current_doc_no} ..?',
                                       title='Generating Doc',
                                       text_color=consts.popup_text_color,
                                       keep_on_top=True,
                                       background_color=consts.popup_back_color)
                if result == 'Yes':
                    my_popups.waiting_window(gif=gifs.saving, message='Document Generated')
                    current_doc.set_document_created(True)
                    database_class.del_doc_from_primaryTb(db_connection, current_doc_no)
                    database_class.add_doc_to_final_tb(db_connection, current_doc_no)
                    main_window[consts.key_doc_number_holder_frame_offset + current_doc_no].hide_row()
                    if not is_doc_genration_list:
                        list_of_doc_for_generation = [doc for doc in document_list if doc.get_is_capture_completed()]
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
                    else:
                        if current_doc_index == len(list_of_doc_for_generation):
                            current_doc_index -= 1

                        current_doc = list_of_doc_for_generation[current_doc_index]
                        current_doc_no = current_doc.get_doc_number()
                        current_image_index = 0
                        img_edit_window[consts.key_graph].erase()
                        img_for_editing = graph_img_helper.draw_graph_img(img_edit_window, consts.key_graph,
                                                                                  current_doc.get_raw_image_by_index(
                                                                                      0))
                        graph_img_helper.graph_header_update(img_edit_window, current_doc_no,
                                                                     current_doc.get_page_number_from_img_at_index(
                                                                         0), current_doc.get_page_count())
                        img_edit_window[consts.key_crop_selct_point].update(disabled=False)
                        cropped = False
                        crop_point_list = []
                        img_edit_window[consts.key_bright_control].update(value=1)
                        img_edit_window[consts.key_contrast_control].update(value=1)
                        threshold = ()


                    sg.popup_animated(None)
            else:
                my_popups.ok_error_popup('The process of this document not completed', 'Document created')

        if event == consts.key_next_doc:
            current_doc_index = document_list.index(current_doc_no)
            if current_doc_index == len(document_list) - 1:
                my_popups.ok_success_popup('No process completed document left for editing', 'Next Doc.')
            else:
                current_doc_index +=1
                for i in range(current_doc_index, len(document_list)):
                    current_doc = document_list[i]
                    if current_doc.get_is_capture_completed():
                        current_doc_no = current_doc.get_doc_number()
                        current_image_index = 0
                        current_doc_index =i
                        img_edit_window[consts.key_graph].erase()
                        img_for_editing = graph_img_helper.draw_graph_img(img_edit_window, consts.key_graph,
                                                                          current_doc.get_raw_image_by_index(0))
                        graph_img_helper.graph_header_update(img_edit_window, current_doc_no,
                                                             current_doc.get_page_number_from_img_at_index(
                                                                 0), current_doc.get_page_count())
                        img_edit_window[consts.key_crop_selct_point].update(disabled=False)
                        cropped = False
                        crop_point_list = []
                        img_edit_window[consts.key_bright_control].update(value=1)
                        img_edit_window[consts.key_contrast_control].update(value=1)
                        threshold = ()
                        break
                    else:
                        i+=1

        if event == consts.key_pre_doc:
            current_doc_index = document_list.index(current_doc_no)
            print(current_doc_index)
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
                        print(f'current xdocument{current_doc_no} at index { current_doc_index}')
                        current_image_index = 0
                        current_doc_index = pre_index
                        img_edit_window[consts.key_graph].erase()
                        img_for_editing = graph_img_helper.draw_graph_img(img_edit_window, consts.key_graph,
                                                                          current_doc.get_raw_image_by_index(0))
                        graph_img_helper.graph_header_update(img_edit_window, current_doc_no,
                                                             current_doc.get_page_number_from_img_at_index(
                                                                 0), current_doc.get_page_count())
                        img_edit_window[consts.key_crop_selct_point].update(disabled=False)
                        cropped = False
                        crop_point_list = []
                        img_edit_window[consts.key_bright_control].update(value=1)
                        img_edit_window[consts.key_contrast_control].update(value=1)
                        threshold = ()
                        break
                    else:
                        pre_index -= 1

            # else:
            #     if current_doc_index <= len(document_list) - 1:
            #         current_doc_index -= 1
            #         current_doc = document_list[current_doc_index]
            #         current_doc_no = current_doc.get_doc_number()
            #         current_image_index = 0
            #         if not current_doc.get_is_capture_completed():
            #             doc_index = current_doc_index - 1
            #             for i in range(current_doc_index):
            #                 if doc_index == 0:
            #                     break
            #                 else:
            #                     current_doc = document_list[doc_index]
            #                     if current_doc.get_is_capture_completed():
            #                         current_doc_no = current_doc.get_doc_number()
            #                         current_doc_index = doc_index
            #                         break
            #                     else:
            #                         doc_index -= 1
            #
            #         elif current_doc.get_is_capture_completed():
            #             current_doc = document_list[current_doc_index]
            #             current_doc_no = current_doc.get_doc_number()
            #             current_image_index = 0
            #         img_edit_window[consts.key_graph].erase()
            #         img_for_editing = graph_img_helper.draw_graph_img(img_edit_window, consts.key_graph,
            #                                                           current_doc.get_raw_image_by_index(0))
            #         graph_img_helper.graph_header_update(img_edit_window, current_doc_no,
            #                                              current_doc.get_page_number_from_img_at_index(
            #                                                  0), current_doc.get_page_count())
            #         img_edit_window[consts.key_crop_selct_point].update(disabled=False)
            #         cropped = False
            #         crop_point_list = []
            #         img_edit_window[consts.key_bright_control].update(value=1)
            #         img_edit_window[consts.key_contrast_control].update(value=1)
            #         threshold = ()


main()
#
