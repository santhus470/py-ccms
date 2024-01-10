import threading
import cv2
from helper import consts, config_helps
import subprocess
import os
from layouts import my_popups
import imutils
import winapps

# collect data from config.json file for editing
thresh_data = config_helps.get_user_data_from_config_file()
thresh_hvalue = thresh_data['hvalue']
thresh_const = thresh_data['const']
thresh_block = thresh_data['block']
thresh_twind = thresh_data['twind']
thresh_swindow = thresh_data['swind']
thresh_bright = thresh_data['brightness']
thresh_contrst = thresh_data['contrast']


# camera property
# quality
#
# L 5184x3456 -18
# M 3456x2340 8 M
# s1 2592x1728 4.5M
# s2 1920x1280 2.5 M
# s3 720x480 .3 M
# 1.5 %  raio

def check_for_digicam_presence():
    for app in winapps.search_installed('digiCamControl'):
        return True if app.name == 'digiCamControl' else False


def disable_btn(window):
    print("disabling")
    window[consts.key_capture_image].update(disabled=True)
    window[consts.key_preview].update(disabled=True)
    window[consts.key_preview].set_cursor(cursor='clock')
    window[consts.key_capture_image].set_cursor(cursor='trek')


def enable_btn(window):
    print("enabling button")
    window[consts.key_capture_image].update(disabled=False)
    window[consts.key_preview].update(disabled=False)
    window[consts.key_preview].set_cursor(cursor='hand2')
    window[consts.key_capture_image].set_cursor(cursor='hand2')


def capture_img(current_doc_no, img_count=0, preview=True, window=None):
    r_code = 1  # set return code
    disable_btn(window)
    if current_doc_no is None:
        my_popups.ok_error_popup('Please select a document first', 'Preview')
    else:
        thresh_dir = consts.thresh_dir
        raw_dir = consts.raw_dir
        camera_command = 'C:\Program Files (x86)\digiCamControl\CameraControlCmd.exe'
        img_name = '{}-{}.png'.format(current_doc_no, img_count)
        current_document_path = os.path.join(raw_dir, current_doc_no)
        current_thresh_document_path = os.path.join(thresh_dir, current_doc_no)
        if not os.path.exists(current_document_path):
            os.mkdir(current_document_path)
        if not os.path.exists(current_thresh_document_path):
            os.mkdir(current_thresh_document_path)
        current_img_path = os.path.join(current_document_path, img_name)
        current_Thresh_img_path = os.path.join(current_thresh_document_path, img_name)
        capture_cmd = camera_command + ' ' + '/filename' + ' ' + current_img_path + ' /capture'
        try:
            subprocess.run(capture_cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE,
                           timeout=9, creationflags=subprocess.CREATE_NO_WINDOW)
            # subprocess.Popen(capture_cmd, stdout=subprocess.PIPE, universal_newlines=True, shell=False,
            #                  creationflags=subprocess.CREATE_NO_WINDOW)

            img = cv2.imread(current_img_path, 0)
            consts.img_widh = img.shape[1]

            if not preview:
                threading.Thread(target=add_img_to_thresolded, args=(img_name, current_doc_no, img,)).start()
                enable_btn(window)
                return imutils.resize(img, width=720, height=480, inter=cv2.INTER_AREA), \
                       current_img_path, current_Thresh_img_path

            else:
                enable_btn(window)
                return imutils.resize(img, width=720, height=480, inter=cv2.INTER_AREA), \
                       current_img_path, None
                # return img, current_img_path, None

        except:
            enable_btn(window)
            my_popups.ok_error_popup('Please Switch off/on the camera and try again', 'Camera error ')
        return None, None, None


# capture_img('01-01-2021')


def add_img_to_thresolded(img_name, curr_doc, img):
    try:
        thres_dir = consts.thresh_dir
        doc_path = os.path.join(thres_dir, curr_doc)
        img_path = os.path.join(doc_path, img_name)
        if not os.path.exists(doc_path):
            os.mkdir(doc_path)
        # just write as PNG
        cv2.imwrite(img_path, img)


    except:
        pass
