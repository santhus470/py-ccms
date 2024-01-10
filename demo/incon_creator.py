import PySimpleGUI as sg
import os
import cv2
import base64

# def crop():
#     image = cv2.imread('/home/santhosh/Downloads/del_red_ico/res/mipmap-hdpi/del_red_ico.png',)
#     print(image.shape)
#     cv2.imwrite('del_reg_cropped.png',cv2.resize(image,dsize=(30,30),interpolation=cv2.INTER_LINEAR))
#
# crop()

layout = [
    [sg.Text('File ',size=(7,1), pad=(20,30)), sg.Input(key='file'),
     sg.FileBrowse(), sg.Button('Create Icon', key='create')
     ],
    [sg.Text('Folder ', pad=(20,30),size=(7,1)), sg.Input(key='folder'),
     sg.FolderBrowse(), sg.Button('Create all', key='create_all')
     ],
]

window = sg.Window('Crop', layout=layout, finalize=True)


def main():
    event, value = window.read()

    while True:
        if event == sg.WINDOW_CLOSED or event == 'Cancel' or event == '-CLOSE-' or event is None:
            window.close()
            break
        if event == 'create':
            path = value['file']
            img = cv2.resize(cv2.imread(path), dsize=(60, 60), interpolation=cv2.INTER_LINEAR)
            # img = cv2.imread(path),
            # cv2.imwrite('deafult_icon.png',img)
            b64_string = base64.b64encode(cv2.imencode('.png', img)[1].tobytes())
            # name = file.split('.')[0]
            print(F'icon={b64_string}')
            break
        if event == 'create_all':
            xpath = value['folder']
            for root, d, f in os.walk(xpath):
                for file in f:
                    path = os.path.join(xpath,file)
                    # print(path)
                    img = cv2.resize(cv2.imread(path), dsize=(20, 20), interpolation=cv2.INTER_LINEAR)
                    b64_string = base64.b64encode(cv2.imencode('.png', img)[1].tobytes())
                    name = file.split('.')[0]
                    print(F'icon_{name}={b64_string}')
            break
            # window.close()

# script


# def base():
#
#     xpath = '/home/santhosh/environments/python/ccms/ccms/assets/icons'
#     for root, d, f in os.walk(xpath):
#         for file in f:
#             path = xpath + '/' + file
#             img = cv2.resize(cv2.imread(path), dsize=(20, 20), interpolation=cv2.INTER_LINEAR)
#             b64_string = base64.b64encode(cv2.imencode('.png', img)[1].tobytes())
#             # name = file.split('.')[0]
#             print(F'icon={b64_string}')
#
# base()
main()
