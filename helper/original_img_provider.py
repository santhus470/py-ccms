

# delete the old image from threshef dir
# copy the same image from raw_folder
# write to thresh dir
#  retrun the image
import os.path
from helper import consts
import cv2
import imutils
from PySimpleGUI import popup_yes_no

def get_org_img(img_path):
    result = popup_yes_no("Do u really want to view the orginal image \n",
                          background_color='red',
                          no_titlebar=True,
                          keep_on_top=True,
                          # font=consts.heading_fonts

                          )
    if result == 'Yes':
        path_list = img_path.split('\\')
        img_name = path_list[-1]
        doc_no = path_list[-2]
        raw_img_path = os.path.join(consts.raw_dir,doc_no,img_name)
        new_img = cv2.imread(raw_img_path,cv2.IMREAD_GRAYSCALE)
        cv2.imwrite(img_path, new_img)
        return imutils.resize(new_img,width=720, height=480)

