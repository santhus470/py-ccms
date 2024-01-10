import shutil
import threading
import cv2
import os
import numpy as np
from helper import consts, config_helps
from data_classes import document
import img2pdf
from PySimpleGUI import popup_error
import imutils
from PIL import Image

'''
when I try various processing for an imge 
get best result in process_fast_adaptive 
that means fastNLmeansDenoising +adaptive threasholding 
in adaptive threshold I use the block size 7  and constant c to 5 - increae in 7 to 9 -increase the quality of black color
for fast n denoising the h is to 7 and all other parameters set to 0
'''
# collect data from config.json file for editing
thresh_data = config_helps.get_user_data_from_config_file()
thresh_hvalue = thresh_data['hvalue']
thresh_const = thresh_data['const']
thresh_block = thresh_data['block']
thresh_twind = thresh_data['twind']
thresh_swindow = thresh_data['swind']
thresh_bright = thresh_data['brightness']
thresh_contrst = thresh_data['contrast']


def crop_dst_points(src_point):
    point_sum = src_point.sum(axis=1)
    point_diff = np.diff(src_point, axis=1)
    # print(crop_points)
    print(src_point)
    cropping_point = np.zeros((4, 2), dtype='float32')
    cropping_point[0] = src_point[np.argmin(point_sum)]
    cropping_point[3] = src_point[np.argmax(point_sum)]
    cropping_point[1] = src_point[np.argmin(point_diff)]
    cropping_point[2] = src_point[np.argmax(point_diff)]
    (top_left, top_right, bottom_right, bottom_left) = src_point
    bottom_wdth = np.sqrt(
        ((bottom_right[0] - bottom_left[0]) ** 2) + ((bottom_right[1] - bottom_left[1]) ** 2)
    )
    top_width = np.sqrt(
        ((top_right[0] - top_right[0]) ** 2) + ((top_right[1] - top_right[1]) ** 2)
    )
    right_height = np.sqrt(
        ((top_right[0] - bottom_right[0]) ** 2) + ((top_right[1] - bottom_right[1]) ** 2)
    )
    left_height = np.sqrt(
        ((top_left[0] - bottom_left[0]) ** 2) + ((top_left[1] - bottom_left[1]) ** 2)
    )
    max_width = max(int(bottom_wdth), int(top_width))
    max_height = max(int(right_height), int(left_height))
    dst_points = np.float32([[0, 0], [max_width, 0], [max_width, max_height], [0, max_height]])
    return dst_points, max_width, max_height


def crop_img(img, point_list, is_crop_and_process=True):
    #this give exact image as cropped in the graph and crop the image asyncronozly
    # dst_points, img_width, img_height = crop_dst_points(src_point)
    # crop_region = cv2.getPerspectiveTransform(src_point, dst_points)
    # cropped_img = cv2.warpPerspective(img, crop_region, (img_width, img_height))
    # threading.Thread(target=crop_original_img, args=(src_point,)).start()
    src_point = np.float32(point_list)
    src_point = np.round(np.array(src_point))
    img = crop_original_img(src_point, is_crop_and_process)
    return img


# L 5184x3456 -18
# M 3456x2340 8 M
# s1 2592x1728 4.5M
# s2 1920x1280 2.5 M
# s3 720x480 .3 M
# 1.5 %  raio
def png_compression():
    commpress_rate = 1
    if consts.img_widh > 3456:
        commpress_rate = 3
    if consts.img_widh > 2592:
        commpress_rate = 2
    else:
        commpress_rate = 1
    return commpress_rate


def crop_original_img(crop_points, crop_and_prcocess= True):
    img = cv2.imread(consts.current_graph_image_path, 0)
    ratio = 0
    if img.shape[1] > img.shape[0]:
        ratio = img.shape[1] / 720
    else:
        ratio = img.shape[0] / 720
    src_point = np.float32(crop_points)
    src_point = np.round(np.array(src_point) * ratio)
    dst_point, max_width, max_height = crop_dst_points(src_point)
    dst_points = np.float32([[0, 0], [max_width, 0], [max_width, max_height], [0, max_height]])
    crop_region = cv2.getPerspectiveTransform(src_point, dst_points)
    img = cv2.warpPerspective(img, crop_region, (max_width, max_height))
    img = np.pad(img, ((1, 1), (1, 1),), constant_values=0)
    if max_width > max_height:
        img = imutils.resize(img, width=1920, height=1280)
    else:
        img = imutils.resize(img, width=1280, height=1920)
    # img = cv2.copyMakeBorder(img, 60, 60, 20, 20, cv2.BORDER_CONSTANT, value=(255, 255, 255))

    # cv2.imwrite(consts.current_graph_image_path,img, [cv2.IMWRITE_PNG_COMPRESSION, png_compression()])
    if crop_and_prcocess:
        cv2.imwrite(consts.current_graph_image_path,
                    adaptive_threshold_meanc(img,
                                             block=thresh_block,
                                             conts=thresh_const,
                                             t_win=thresh_twind, s_win=thresh_twind,
                                             h_value=thresh_hvalue
                                             ),
                    [cv2.IMWRITE_PNG_COMPRESSION, png_compression()])
    else:
        cv2.imwrite(consts.current_graph_image_path,img,[cv2.IMWRITE_PNG_COMPRESSION, png_compression()])
    return img


def fast_n_denoising(img):
    #     h-lminus component can be 3,5,7
    return cv2.fastNlMeansDenoising(img, h=3, templateWindowSize=7, searchWindowSize=21)  # recomedef size is 21


def gausian_denoising(img):
    return cv2.GaussianBlur(img, (3, 3), 0)


def bilateral_denoising(img):
    return cv2.bilateralFilter(img, 9, 75, 75)


# src, maxValue, adaptiveMethod, thresholdType, blockSize, C, dst=None
# @param blockSize Size of a pixel neighborhood that is used to calculate a threshold value for the
#     .   pixel: 3, 5, 7, and so on.
#     .   @param C Constant subtracted from the mean or weighted mean (see the details below). Normally, it
#     .   is positive but may be zero or negative as well.
def adaptive_threshold_meanc(file, block, conts, t_win, s_win, h_value):  # atm-C
    return cv2.adaptiveThreshold(
        cv2.fastNlMeansDenoising(file, h=h_value, templateWindowSize=t_win, searchWindowSize=s_win),
        255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, block, conts)


def adaptive_threshold_guassian_c(file, block, conts, t_win, s_win, h_value):  # atg-C
    # return cv2.threshold(cv2.GaussianBlur(file, (3, 3), 0), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return cv2.adaptiveThreshold(
        cv2.fastNlMeansDenoising(file, h=h_value, templateWindowSize=t_win, searchWindowSize=s_win),
        255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block, conts)
    # return cv2.adaptiveThreshold(cv2.bilateralFilter(file, 9, 75, 75),255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    # return cv2.adaptiveThreshold(cv2.filter2D(src=file,ddepth=-1,kernel=kernel3),255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    # return cv2.adaptiveThreshold(cv2.medianBlur(src=file,ksize=5),255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)


def adaptive_threshold_meanc_inverse(file, block, h_value, conts, t_win, s_win):  # atm-C-Inverse
    return cv2.adaptiveThreshold(
        cv2.fastNlMeansDenoising(file, h=h_value, templateWindowSize=t_win, searchWindowSize=s_win),
        255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, block, conts)
    # return cv2.adaptiveThreshold(file, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV,block, conts)


def adaptive_threshold_guassian_c_inverse(file, h_value, block, conts, t_win, s_win):  # atg-C-Inverse
    return cv2.adaptiveThreshold(
        cv2.fastNlMeansDenoising(file, h=h_value, templateWindowSize=t_win, searchWindowSize=s_win),
        255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, block, conts)

    # return cv2.adaptiveThreshold(file, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, block, conts)


def otsu_guassian_thresholding(file):  # ogt
    return cv2.threshold(cv2.GaussianBlur(file, (3, 3), 0), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


def otsu_fast_n_thresholding(file):  # ofat
    otsu = cv2.threshold(file, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return cv2.adaptiveThreshold(
        cv2.fastNlMeansDenoising(file, h=2, templateWindowSize=7, searchWindowSize=11),
        255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, 2)


def rotate_right():
    cv2.imwrite(filename=consts.current_graph_image_path,
                img=cv2.rotate(cv2.imread(consts.current_graph_image_path), cv2.ROTATE_90_CLOCKWISE))


def rotate_left():
    cv2.imwrite(filename=consts.current_graph_image_path,
                img=cv2.rotate(cv2.imread(consts.current_graph_image_path), cv2.ROTATE_90_COUNTERCLOCKWISE))


def save_changes_single_img(img, current_doc, current_index, brightness, contrast, threshold):
    doc_num = current_doc.get_doc_number()
    img_path = os.path.join(consts.thresh_dir, doc_num)
    r_code = None
    # img_name = '{}-{}.JPEG'.format(doc_num, current_index)
    # file_path = os.path.join(img_path, img_name)
    file_path = consts.current_graph_image_path
    processed_img = document.CapturedImages(file_path)
    # processed_img.set_page_no(current_index)
    processed_img.set_process_completed(True)
    new_img = cv2.imread(file_path, 0)
    if brightness != 1 or contrast != 1:
        new_img = cv2.convertScaleAbs(new_img, alpha=contrast, beta=brightness)
    else:
        if threshold:
            if threshold[0] == consts.key_thresh_meanc:
                new_img = adaptive_threshold_meanc(new_img, threshold[1], threshold[2], threshold[3], threshold[4],
                                                   threshold[5])
            elif threshold[0] == consts.key_thresh_gauss:
                new_img = adaptive_threshold_guassian_c(new_img, threshold[1], threshold[2], threshold[3], threshold[4],
                                                        threshold[5])
            elif threshold[0] == consts.key_thresh_meanc_inv:
                new_img = adaptive_threshold_meanc_inverse(new_img, threshold[1], threshold[2], threshold[3],
                                                           threshold[4], threshold[5])
            elif threshold[0] == consts.key_thresh_gauss_inv:
                new_img = adaptive_threshold_guassian_c_inverse(new_img, threshold[1], threshold[2], threshold[3],
                                                                threshold[4], threshold[5])

    # current_doc.set_img_as_processed_in_list(processed_img, current_index)

    if not os.path.exists(img_path):
        os.mkdir(img_path)
    try:
        cv2.imwrite(filename=file_path, img=new_img)
        r_code = 1
    except:
        r_code = 0
    return r_code


def save_all_img(current_doc, brightness, contrast, threshold):
    for img in current_doc.get_raw_img_obj_list():
        if not img.get_process_completed_value():
            save_changes_single_img(cv2.imread(img.get_image(), cv2.IMREAD_GRAYSCALE), current_doc, 0, brightness,
                                    contrast, threshold)


def document_generation(img_list, curent_doc_no):
    rcode = None
    pdf_file = curent_doc_no + '.pdf'
    deskop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    pdf_path = os.path.join(deskop, 'ccms_certified_copy')
    thresh_path = os.path.join(consts.thresh_dir, curent_doc_no)
    raw_path = os.path.join(consts.raw_dir, curent_doc_no)
    pdf_rm_path = os.path.join(consts.pdf_dir, pdf_file)
    if not os.path.exists(pdf_path):
        os.mkdir(pdf_path)

    try:
        pdf_createor(pdf_path, img_list, curent_doc_no)
        os.remove(pdf_rm_path)
        shutil.rmtree(thresh_path)
        shutil.rmtree(raw_path)  # remove the riginal image
        img1 = Image.fromarray(
            cv2.copyMakeBorder(cv2.imread(img_list[0]), 80, 80, 40, 40, cv2.BORDER_CONSTANT, value=(255, 255, 255)))
        # img1 = Image.open(img_list[0], mode='r')
        # img1 = np.pad(cv2.imread(path), ((30, 30), (80, 80), (0, 0)), constant_values=255)
        # path_name = os.path.join(pdf_dir, curent_doc_no)
        img1.save(f'{pdf_path}.pdf', save_all=True, append_images=[Image.fromarray(
            cv2.copyMakeBorder(cv2.imread(img), 80, 80, 40, 40, cv2.BORDER_CONSTANT, value=(255, 255, 255))) for img in
            img_list[1:]])
        rcode = 1
    # for image in img_list:
    #     print(image.get_page_number(), image.get_image())
    # path_name = os.path.join(consts.pdf_directory, curent_doc_no)
    # img1 = Image.fromarray(cv2.imread(img_list[0].get_image()))
    # img1.save(f'{path_name}.pdf', save_all=True,
    #           append_images=[Image.fromarray(cv2.imread(img.get_image())) for img in img_list[1:]])

    except:
        pass
    return rcode, pdf_path


def create_pdf_from_img(img_list, curent_doc_no):
    pdf_dir = consts.pdf_dir
    r_code = pdf_createor(pdf_dir, img_list, curent_doc_no)
    if r_code:
        view_pdf(curent_doc_no)

    return r_code


def pdf_createor(path, img_list, curent_doc_no):
    r_code = None
    a4inpt = (img2pdf.mm_to_pt(210), img2pdf.mm_to_pt(297))
    layout_fun = img2pdf.get_layout_fun(a4inpt)
    if img_list:
        path_name = os.path.join(path, curent_doc_no)
        try:
            with open(f'{path_name}.pdf', 'wb') as f:
                f.write(img2pdf.convert(img_list, layout_fun=layout_fun))
                f.close()
                r_code = 1
        except:
            r_code = None
            popup_error('Please close the existing pdf of this document and try again', 'error',
                        background_color='red', no_titlebar=True)

    return r_code


def view_pdf(doc_number):
    pdf_file = doc_number + '.pdf'
    file_path = os.path.join(consts.pdf_dir, pdf_file)
    try:
        os.startfile(file_path)

    except:
        popup_error(f'Cant open the document {doc_number}. Tyr again', f'{doc_number}')


def resize_image_reduce_for_sg(img, shape):
    # print('sahpe', shape)
    return cv2.imencode('.png', cv2.resize(img, dsize=shape, interpolation=cv2.INTER_LINEAR))[1].tobytes()


def make_border(img):
    return cv2.copyMakeBorder(img, 80, 80, 60, 60, cv2.BORDER_CONSTANT, value=(255, 255, 255))
