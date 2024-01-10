import platform

import cv2
from helper import consts, image_processor
import subprocess
import os
from layouts import my_popups
import imutils



# camera property
# quality
#
# L 5184x3456 -18
# M 3456x2340 8 M
# s1 2592x1728 4.5M
# s2 1920x1280 2.5 M
# s3 720x480 .3 M
# 1.5 %  raio


def capture_img(current_doc_no, img_count=0):
    if current_doc_no is None:
        my_popups.ok_error_popup('Please select a document first', 'Preview')
    else:
        camera_command = 'C:\Program Files (x86)\digiCamControl\CameraControlCmd.exe'
        img_name = '{}-{}.JPEG'.format(current_doc_no, img_count)
        current_document_path = os.path.join(consts.raw_image_directory, current_doc_no)
        if not os.path.exists(current_document_path):
            os.mkdir(current_document_path)
        current_img_path = os.path.join(current_document_path, img_name)
        capture_cmd = camera_command + ' ' + '/filename' + ' ' + current_img_path + ' /capture'
        print(capture_cmd)
        try:
            p = subprocess.Popen(capture_cmd, stdout=subprocess.PIPE, universal_newlines=True, shell=False)
            r_code = p.wait()
            if r_code == 0:
                # img = imutils.resize(cv2.imread(current_img_path, 0), width=720, height=480, inter=cv2.INTER_AREA)
                img=cv2.imread(current_img_path, 0)
                width = img.shape[1]

                if width > 1920:
                    cv2.imwrite(filename=current_img_path, img=imutils.resize(cv2.imread(current_img_path, 0), width=1920, height=1280, inter=cv2.INTER_AREA))
                return imutils.resize(cv2.imread(current_img_path, 0), width=720, height=480, inter=cv2.INTER_AREA), current_img_path
            else:
                my_popups.ok_error_popup('Please switch on the camera', 'Camera Error')
                return None, None
        except:
            my_popups.ok_error_popup(
                'Cant communicate with camera. If ths error comes repeatedly \n Use the camera with Manual focus  ',
                'Commucation error ')
            return None, None

# capture_img('01-01-2021')

def add_img_to_processed(img_name, curr_doc, img):
    doc_path = os.path.join(consts.processed_image_directory, curr_doc)
    img_path = os.path.join(doc_path,img_name)
    if not os.path.exists(doc_path):
        os.mkdir(doc_path)
    cv2.imwrite(filename=img_path, img=image_processor.adaptive_threshold_meanc(
        img,block=11,conts=2,t_win=7,s_win=21
    ))
