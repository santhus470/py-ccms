# --------------------------------------------------------------------------------------------------------------
#                                    TODO View original image for Editing
# ----------------------------------------------------------------------------------------------------------
if event == consts.key_org_img_for_threshing:
    result = sg.PopupYesNo('Do you want to edit original Image ', title='Original Image')
    print(result)
    if result == 'Yes':
        source = os.path.join(consts.raw_dir, current_doc_no)
        dest = os.path.join(consts.thresh_dir, current_doc_no)
        shutil.rmtree(dest)
        shutil.copytree(source, dest)

    img_edit_window[consts.key_h_value].update(disabled=False)
    img_edit_window[consts.key_thresh_const].update(disabled=False)
    img_edit_window[consts.key_thresh_block].update(disabled=False)
    img_edit_window[consts.key_thresh_Templ_wind].update(disabled=False)
    img_edit_window[consts.key_thresh_search_wind].update(disabled=False)
    img_edit_window[consts.key_thresh_meanc_inv].update(disabled=False)
    img_edit_window[consts.key_thresh_meanc].update(disabled=False)
    img_edit_window[consts.key_thresh_gauss_inv].update(disabled=False)
    img_edit_window[consts.key_thresh_gauss].update(disabled=False)
    img_edit_window[consts.key_bright_control].update(disabled=False)
    img_edit_window[consts.key_contrast_control].update(disabled=False)
    img_edit_window[consts.key_save_all_processed_img].update(disabled=False)
    img_edit_window[consts.key_save_processed_img].update(disabled=False)
    img_edit_window[consts.key_graph].erase()
    graph_img_helper.draw_graph_img(img_edit_window,
                                    consts.key_graph,
                                    current_doc.get_raw_image_by_index(0))
    graph_img_helper.graph_header_update(img_edit_window,
                                         current_doc_no,
                                         current_doc.get_page_number_from_img_at_index(0),
                                         current_doc.get_page_count())
