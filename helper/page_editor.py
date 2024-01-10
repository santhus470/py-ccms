from helper import consts
def edit_page_number(current_doc, values):
    # 1. collect the input from the layout
    # 2. check the page number and total pages are matching
    # 2.take the current document
    # 3. set page number of each page as the user input (implement with in document class)
    # 4. sort the image with the page number of each page
    # 5. reset the imgae eidt window with the first page
    # 6. re set the image list of edited page as re arranged
    print(current_doc.get_raw_image_list())
    for count ,img in enumerate(current_doc.get_raw_img_obj_list()):
        # img.set_page_no(int(values[consts.key_page_no+str(count+1)]))
        print(values[consts.key_page_no])
    current_doc.sort_raw_image_list()

    print(current_doc.get_raw_image_list())