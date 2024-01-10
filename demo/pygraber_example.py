
import pygrabber

from tkinter import Tk
# graph = FilterGraph()
# graph.add_video_input_device(1)

# from pygrabber.dshow_graph import FilterGraph
import cv2
graph = pygrabber.dshow_graph.FilterGraph()
camera_command = 'C:\Program Files (x86)\digiCamControl\CameraControlCmd.exe'
camera_command_details = '/filename ./' + 'input_filename' + ' /capture /iso 500 /shutter 1/30 /aperture 1.8'
print('camera details = ',camera_command_details)
full_command=camera_command + ' ' + camera_command_details
print(full_command)

print(graph.get_input_devices())
capture = cv2.VideoCapture(1, cv2.CAP_DSHOW)


print("CV_CAP_PROP_FRAME_WIDTH: '{}'".format(capture.get(cv2.CAP_PROP_FRAME_WIDTH)))
print("CV_CAP_PROP_FRAME_HEIGHT : '{}'".format(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
print("CAP_PROP_FPS : '{}'".format(capture.get(cv2.CAP_PROP_FPS)))
print("CAP_PROP_POS_MSEC : '{}'".format(capture.get(cv2.CAP_PROP_POS_MSEC)))
print("CAP_PROP_FRAME_COUNT  : '{}'".format(capture.get(cv2.CAP_PROP_FRAME_COUNT)))
print("CAP_PROP_BRIGHTNESS : '{}'".format(capture.get(cv2.CAP_PROP_BRIGHTNESS)))
print("CAP_PROP_CONTRAST : '{}'".format(capture.get(cv2.CAP_PROP_CONTRAST)))
print("CAP_PROP_SATURATION : '{}'".format(capture.get(cv2.CAP_PROP_SATURATION)))
print("CAP_PROP_HUE : '{}'".format(capture.get(cv2.CAP_PROP_HUE)))
print("CAP_PROP_GAIN  : '{}'".format(capture.get(cv2.CAP_PROP_GAIN)))
print("CAP_PROP_CONVERT_RGB : '{}'".format(capture.get(cv2.CAP_PROP_CONVERT_RGB)))
print(capture.isOpened())
while(True):
    retval, im = capture.read()
    # print(im)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    im = im[0:100,720:1180]
    cv2.imshow("image", im)

    k = cv2.waitKey(33)

    if k==27: # Esc key press
        print('Resolution: {0}x and {1}y'.format(im.shape[1],im.shape[0]))
        print('FPS: {0}'.format(capture.get(cv2.CAP_PROP_FPS)))
        break

capture.release()
cv2.destroyAllWindows()