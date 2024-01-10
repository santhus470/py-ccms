from helper import  consts


def enable_edit_win_btn(window):
    window[consts.key_h_value].update(disabled=False)
    window[consts.key_thresh_const].update(disabled=False)
    window[consts.key_thresh_block].update(disabled=False)
    window[consts.key_thresh_Templ_wind].update(disabled=False)
    window[consts.key_thresh_search_wind].update(disabled=False)
    window[consts.key_thresh_meanc_inv].update(disabled=False)
    window[consts.key_thresh_meanc].update(disabled=False)
    window[consts.key_thresh_gauss_inv].update(disabled=False)
    window[consts.key_thresh_gauss].update(disabled=False)
    window[consts.key_bright_control].update(disabled=False)
    window[consts.key_contrast_control].update(disabled=False)
    window[consts.key_save_all_processed_img].update(disabled=False)
    window[consts.key_save_processed_img].update(disabled=False)


def disable_edit_win_btn(window):
    window[consts.key_h_value].update(disabled=True)
    window[consts.key_thresh_const].update(disabled=True)
    window[consts.key_thresh_block].update(disabled=True)
    window[consts.key_thresh_Templ_wind].update(disabled=True)
    window[consts.key_thresh_search_wind].update(disabled=True)
    window[consts.key_thresh_meanc_inv].update(disabled=True)
    window[consts.key_thresh_meanc].update(disabled=True)
    window[consts.key_thresh_gauss_inv].update(disabled=True)
    window[consts.key_thresh_gauss].update(disabled=True)
    window[consts.key_bright_control].update(disabled=True)
    window[consts.key_contrast_control].update(disabled=True)
    window[consts.key_save_all_processed_img].update(disabled=True)
    window[consts.key_save_processed_img].update(disabled=True)
