import os
import shutil
import subprocess
import winapps

# fonts

theme_dark_color = '#263238'
theme_light1 = '#37474f'
theme_light_2 = '#455a64'
popup_back_color = '#00796B'
popup_text_color = 'white'
img_widh = 720
img_heigh = 480
graph_width = 720  # define the graph width
org_img_width = org_img_height = 0

#
# def get_directory(name):
#     my_dir_path = os.path.join(os.getcwd(), name)
#     if not os.path.exists(my_dir_path):
#         os.mkdir(my_dir_path)
#     return my_dir_path


digicam_msg = 'Digi cam controller is not installed .\n\nYou can Download it from ' \
              '\nhttps://sourceforge.net/projects/digicamcontrol/files/latest/download' \
              '\n\nPlease install it and proceeds\n'

thresh_dir = None
raw_dir = None
db_dir = None
json_dir = None
processed_dir = None
pdf_dir = None

heading_fonts = 'ubuntu 13 bold'
heading_fonts_LARGE = 'CourierNew 16 bold'
normal_font = 'Ubuntu '
frame_border_main_wind_size = 2
frame_relief_main = 'solid'

# current_imge_property
current_graph_image_path = None
current_image_obj = None

# keys main window
key_col_add_doc = '-COL_ADD_DOC-'
key_col_camera = '-COL_CAMERA-'
key_col3_raw_img_thump_col = '-COL_RAW_IMG_THUMP-'
key_raw_img_thump_holder_frame_offset = '-RAW_IMG_HOLDE_FRAME-'
key_doc_number_holder_frame_offset = '-DOC-NO-HOLDER-FRAME-'
key_del_doc_frm_col_1 = '-DEL-DOC-FROM-COL1-_'
key_capture_image = '-TAKEPHOTO-'
key_start_camera = '-STARTCAMERA-'
key_video_view_disply = '-VIDEO-'
key_save_all_raw_img_btn = '-SAVE_ALL-'
key_col4_capture_completed_doc = '-CAPTURE_COMPLETED_DOC-'
key_capture_completed_doc_frame_offset = '-CAPTURED_DOC_HOLDER_FRAME-'
key_volume_no = '-VOL_IN_COL_1-'
key_preview = '-VIEW_PREVIEW-'
key_delete_thump_offset = 'DELETE_RAW_THUMP#'

# DocumentInput keys
key_doc_input_doc = '-DOCNO-'
key_doc_input_book = '-BOOK-'
key_doc_input_year = '-YEAR-'
key_doc_input_vol = '-VOLUME-'

# Document Displykey
key_disply_selected_doc = '-DOCHEADING-'
key_btn_add_doc = '-ADDDOC-'
key_btn_add_doc_save = '-SAVEDOC-'
key_btn_add_doc_close = 'CLOSEDOCINPUTWIN'

# color
color_column_bg_color = 'grey'
# text size
doc_read_input_size = (18, 1)
doc_read_Text_size = (13, 1)
heading_text_size = (20, 2)
top_row_height = 40
bottom_row_height = 50

# Screen Size
web_cam_dimension = (800, 600)  # webcam
# screen_width, screen_height = sg.Window.get_screen_size()
screen_width, screen_height = 1500, 900
side_col_width = int(screen_width / 8)
side_col_size = (150, 1)
center_column_width = graph_width + 50

# web_cam_dimension = (1056,704) #cannon

# // camera running in photog2
camera_script1 = 'echo Igr@123 | sudo -s modprobe v4l2loopback'
camera_script2 = 'gphoto2 --stdout --capture-movie | ffmpeg -i - -vcodec rawvideo -pix_fmt yuv420p -threads 0 -f v4l2 ' \
                 '/dev/video0 '

# // image editor connsts
key_img_edit_win_close = '-CLOSE_IMG_EDIT_WIN-'
key_bright_control = '-BRIGT_CTRL-'
key_contrast_control = '-CONTRST_CTRL-'
key_crop_btn = '-CROP-'
key_crop_only = '-CROP_ONLY-'
key_crop_undo = '-DEL_CROP-'
key_crop_selct_point = '-CROP_POINTS-'
key_graph = "-GRAPH-"
key_bright_input = 'BRIGHT-INPUT'
key_edited_image = '-EDITED-IMAGE-'
key_rot_right_90 = '-ROT_90_RIGHT-'
key_rot_left_90 = '-ROT_90_LEFT-'
key_rot_right = '-ROT_RIGHT-'
key_rot_left = '-ROT_LEFT-'
key_previous_btn = '-PREVIOUS_IMG-'
key_next_img = '-NEXT_IMG-'
key_flip_img = '-FLIP_IMH-'
key_img_edit_list_col = '-MG_LIST_IMG_EDIT-'
key_save_processed_img = '-SAVE_PROCESSED_IMG-'
key_save_all_processed_img = '-SAVE_CHANGES_TO_ALL_IMAGE-'
key_create_doc = '-CREATE_DOC-'
key_view_pdf = '-VIEW_PDF-'
key_thresh_const = '-THRES_CONST-'
key_thresh_block = '-THRESH_BLOCK-'
key_thresh_meanc = '-THRESH_MEAN-'
key_thresh_meanc_inv = '-THRESH_MEAN_INV-'
key_thresh_gauss = '-THRESH_GAUSS-'
key_thresh_gauss_inv = '-THRESH_GAUSS_INV-'
key_capture_again = '-CAPTURE_FROM_EDIT_WIN-'
key_del_entire_doc = '-EDIT_ENTIRE_DOC-'
key_thresh_Templ_wind = '-THRESH_TEMPLATE_WIND-'
key_thresh_search_wind = '-KEY_THRESH_SEARCH_WIND-'
key_h_value = '-H_VALUE-'
key_edit_page_no = '-EDIT_PAGE_NO-'
key_pre_doc = '-PREV_DOC-'
key_next_doc = '-NEXT_DOC-'
key_generate_CC = '-GENERATE_CC-'
key_total_page = '-GRAPH_TOTAL_PAGE-'
key_View_original_img = '-VIEW_ORG_IMG-'

# camera selection layout
key_availabele_camera = '-AVAILABLE_CAMERA-'
key_camera_select_ok = '-SELECT_CAMERA_OK_BTN-'

# recapture
key_recap_video_view_disply = '-RECAP_VID_DISPLY-'
# menu
key_menu_view_docs = 'In process Doc List'
key_menu_view_generated_doc = 'Created Doc List'
key_menu_list_doc_frame_offset = '-MENU_DOC_FRAME_OFFSET-'
key_menu_column = '-MENU_DOC_LIST_COL-'
key_menu_all_doc_win_close = '-CLOSE_MENU_WIN-'
key_menu_gerated_doc_win_close = '-CLOSE_MENU_GENERATED_DOC_WIN-'
key_menu_generated_doc_column = '-MENU_GEN_DOC_LIST_COL-'
key_menu_del_doc = '-DEL_DOC_FROM_MENU-.'
key_menu_add_doc = 'Add Single Document'
key_menu_read_file = 'Add from file'

key_menu_about = 'About'

# Image View
key_img_view_graph = '-IMG_VIEW_GRAPH-'
key_img_view_prev = '-IMG_VIEW_PREV-'
key_img_view_next = '-IMG_VIEW_NEXT-'
key_img_view_del = '-IMG_VIEW_DEL-'
key_img_view_win_close = 'IMG_VIEW_CLOSE-'
key_graph_header = '-IMG_VIEW_HEDER-'
key_page_edit_lrlr = '-EDIT_PAGE_LRLR-'
key_page_edit_lrrl = '-EDIT_PAGE_LRRL-'
key_page_editlist_col = '-PAGE_EDIT_LIST_COL-'
key_page_edit_frame_offset = '-PAGE_EDIT_FRAME-'

# Key_camera_selection
# Page editing window
key_page_edit_col = '-PAGE_EDIT_COL-'
key_save_page_no = '-PAGE_EDIT_SAVE-'
key_page_edit_reset = '-PAGE_EDIT_RESET-'
key_page_no = '-PAGE_NUMBER-'
key_org_page_no = '-ORG_PAGE_NO-'

# File broeser window
key_read_file_browse = '-FILE_BROWSER-'
key_file_path = '-FILE_PATH-'

edit_bright_pad = ((20, 0), (25, 5))

graph_size = 750
init_img_height = 0
frame_size = (650, 450)
column_size = (800, 1000)
image_size = (800, 600)
canvas_size = (900, 900)


# about page url_consts
url_sg = 'https://www.pysimplegui.org'
url_cv = 'https://opencv.org/'
url_mutils = 'https://pypi.org/project/imutils/'
url_winapp = 'https://pypi.org/project/winapps/'
url_pdf = 'https://pypi.org/project/PyPDF2/'
url_pillow = 'https://pypi.org/project/Pillow/'
url_digicam = 'http://digicamcontrol.com/download'
url_pearl = 'https://registration.kerala.gov.in'
key_about_close = '-CLOSE_ABOUT_WIN-'
url_watsaspp = 'https://web.whatsapp.com/send/?phone=918547344357&text=&type=phone_number&app_absent=0'