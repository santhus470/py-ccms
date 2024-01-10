import os
from dataclasses import dataclass
from helper import consts


class CapturedImages:
    def __init__(self, img_path, page=0):
        self._img_path = img_path
        self._brightness = 1
        self._contrast = 1
        self._thresholds = None
        self._page_no = page
        self._crop_point = []
        self._process_completed = False
        self._cropped = False

    def get_image(self):
        return self._img_path

    def get_page_number(self):
        return self._page_no

    def get_process_completed_value(self):
        return self._process_completed

    def set_brightness(self, brightness):
        self._brightness = brightness

    def set_contrast(self, contrast):
        self._contrast = contrast

    def set_thresholds(self, threshold):
        self._thresholds = threshold

    def set_page_no(self, page):
        self._page_no = page

    def set_crop_point(self, crop_point):
        self._crop_point = crop_point

    def set_process_completed(self, value):
        self._process_completed = value

    def set_cropped(self, value):
        self._cropped = value

    def is_cropped(self):
        return self._cropped

    def __str__(self):
        return self._img_path

    def __iter__(self):
        return self._img_path


class Document:
    def __init__(self, doc_no, volume=''):
        self._doc_num: str = doc_no
        self._volume_no: str = volume
        self._raw_img_list: list = []
        self._processed_img_list = []
        self._page_no = 1
        self._is_capture_started: bool = False
        self._is_process_started: bool = False
        self._is_capture_completed: bool = False
        self._is_process_completed: bool = False
        self._is_document_created: bool = False

    def _remove_file(self, img_obj):
        current_path = img_obj.get_image()
        path_list = current_path.split('\\')
        img_name = path_list[-1]
        doc_no = path_list[-2]
        raw_img_path = os.path.join(consts.raw_dir, doc_no, img_name)
        if os.path.exists(img_obj.get_image()):
            os.remove(current_path)
            os.remove(raw_img_path)

    def set_img_as_processed_in_list(self, img_obj, index):
        self._raw_img_list.pop(index)
        self._raw_img_list.insert(index, img_obj)

    def add_raw_image(self, image):
        image.set_page_no(self._page_no)
        self._raw_img_list.append(image)
        self._page_no = self._page_no + 1

    def remove_raw_image(self, img):
        self._reset_page_no(img)
        try:
            self._raw_img_list.remove(img)
            self._remove_file(img)
        except:
            pass
    def _reset_page_no(self, image_obj):
        curent_page_no = image_obj.get_page_number()
        total_page = self.get_page_count()
        if total_page == curent_page_no: #last page
            self._page_no = self._page_no-1
        else: #currentpage < totalpage
            for i  in range(curent_page_no,total_page):
                self._raw_img_list[i].set_page_no(i)



    def remove_raw_img_by_index(self, index):
        img = self._raw_img_list[index]
        self._reset_page_no(img)
        self._raw_img_list.pop(index)
        self._remove_file(img)

    def clear_img_list(self):
        self._raw_img_list.clear()
        self._page_no = 1

    def add_processed_img(self, img):
        self._processed_img_list.append(img)

    def remove_procesd_img(self, img):
        self._processed_img_list.remove(img)

    def sort_raw_image_list(self):
        # self._raw_img_list = sorted(self._raw_img_list, key=lambda x: int((x.split('.')[0])[-1]))
        self._raw_img_list.sort(key=lambda x: x._page_no)



    def get_doc_number(self):
        return self._doc_num

    def get_volume(self):
        return self._volume_no

    def get_page_number_from_img_at_index(self, index):
        # return (self._raw_img_list[index].split('.')[0]).split('-')[-1]

        return self._raw_img_list[index].get_page_number()

    def get_page_number_of_image(self, image):
        page_no = 0
        for img in self._raw_img_list:
            if img.get_image() == image:
                page_no = img.get_page_number()
        return page_no

    def get_page_count(self):
        return len(self._raw_img_list)

    def get_raw_image_list(self):
        self.sort_raw_image_list()
        # return  self._raw_img_list
        return [img.get_image() for img in self._raw_img_list]


    def get_raw_img_obj_list(self):
        self.sort_raw_image_list()
        return self._raw_img_list

    def get_raw_img_obj_by_ndex(self, index):
        return  self._raw_img_list[index]

    def get_raw_image_by_index(self, index):
        self.sort_raw_image_list()
        return self._raw_img_list[index].get_image()

    def get_index_of_raw_img(self, image):
        index = 0
        for pos, img in enumerate(self._raw_img_list):
            if img.get_image() == image:
                index = pos
                break
        return index

    def get_img_obj_from_path(self, image):
        imj_ob = None
        for img in self._raw_img_list:
            if img.get_image() == image:
                imj_ob = img
                break
        return imj_ob

    def get_is_capture_started(self):
        return self._is_capture_started

    def get_is_process_statred(self):
        return self._is_process_started

    def set_capture_completed(self, value):
        self._is_capture_completed = value

    def set_capture_started(self, ):
        self._is_capture_started = True

    def get_is_capture_completed(self):
        return self._is_capture_completed

    def get_is_proess_completed(self):
        return self._is_process_completed

    def get_is_document_created(self):
        return self._is_document_created

    def set_page_number_of_img(self, index, new_page_no):
        old = self._raw_img_list[index]
        old.set_page_no(new_page_no)
        # self.sort_raw_image_list()

    def set_volume(self, volume):
        self._volume_no = volume

    def set_process_started(self, ):
        self._is_process_started = True

    def set_process_completed(self, value):
        self._is_process_completed = value

    def set_document_created(self, value):
        self._is_document_created = value

    def __eq__(self, other):
        return True if self._doc_num == other else False

    def __iter__(self):
        return self._doc_num

    def __str__(self):
        return self._doc_num
