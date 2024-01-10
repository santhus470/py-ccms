import os
import subprocess
import PySimpleGUI as sg
import cv2

from layouts import my_popups


def capture_img(current_doc_no='01-01-2021', img_count=0, preview=True):
    r_code = 1  # set return code
    if current_doc_no is None:
        my_popups.ok_error_popup('Please select a document first', 'Preview')
    else:
        thresh_dir = os.getcwd()
        raw_dir = os.getcwd()
        camera_command = 'C:\Program Files (x86)\digiCamControl\CameraControlCmd.exe'
        img_name = '{}-{}.JPEG'.format(current_doc_no, img_count)
        current_document_path = os.path.join(raw_dir, current_doc_no)
        current_thresh_document_path = os.path.join(thresh_dir, current_doc_no)
        if not os.path.exists(current_document_path):
            os.mkdir(current_document_path)
        if not os.path.exists(current_thresh_document_path):
            os.mkdir(current_thresh_document_path)
        current_img_path = os.path.join(current_document_path, img_name)
        current_Thresh_img_path = os.path.join(current_thresh_document_path, img_name)
        capture_cmd = camera_command + ' ' + '/filename' + ' ' + current_img_path + ' /capture'
        print(capture_cmd)
        p = subprocess.run(capture_cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE,
                           timeout=7, )
        # p.wait(timeout=7)
        # with subprocess.Popen(capture_cmd, stdout=subprocess.PIPE, universal_newlines=True, shell=True) as p:
        #     p.wait(timeout=7)

        cv2.imshow('Img', cv2.imread(current_img_path))
        cv2.waitKey(0)
        cv2.destroyAllWindows()


        # try:
        #     img = cv2.imread(current_img_path, 0)
        #
        #     # if img.shape[1] != 3456:
        #     #
        #     # popup_ok('Please set the resolution to Medium (3456x2340)',
        #     #            no_titlebar=True, background_color='red', font=consts.normal_font,
        #     #            icon=icons_dark.main_icon)
        #     if not preview:
        #         threading.Thread(target=add_img_to_thresolded, args=(img_name, current_doc_no, img,)).start()
        #         return imutils.resize(img, width=720, height=480, inter=cv2.INTER_AREA), \
        #                current_img_path, current_Thresh_img_path
        #     else:
        #         return imutils.resize(img, width=720, height=480, inter=cv2.INTER_AREA), \
        #                current_img_path, None
        #         # return img, current_img_path, None
        #
        # except:
        #
        #     sg.PopupOK(
        #         'Please Switch off/on the camera and try again', 'Camera error ')

        return None, None, None


if __name__ == "__main__" :
    capture_img()
