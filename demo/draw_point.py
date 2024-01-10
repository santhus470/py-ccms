import PySimpleGUI as sg
import cv2
import numpy as np

graph = 'graph'
draw = 'draw'

image_view = [
    [
        sg.Frame(
            pad=(5, 5),
            title='Image',
            expand_y=True,
            expand_x=True,
            layout=[
                [sg.Text('Document No')],
                [
                    sg.Graph(canvas_size=(800, 800),
                             graph_bottom_left=(-0, -0),
                             graph_top_right=(800,800),
                             key='graph', enable_events=True,
                             background_color='white',
                             drag_submits=True, pad=(0, 0))
                ],
            ]
        )
    ],
    [
        sg.Button('Draw Points', key = 'draw'), sg.Button('Crop', key='crop')
    ]

]
window = sg.Window(title='Draw testing',
                   layout=image_view,
                   size=(900, 900),

                   finalize=True
                   )


def converting_points(pointList):
    point_list = []
    for points in pointList:
        points[0], points[1] =points[0],points[1]
        point_list.append(points)
    return  point_list



# All points are in format [cols, rows]
pt_A = [41, 2001]
pt_B = [2438, 2986]
pt_C = [3266, 371]
pt_D = [1772, 136]
# Here, I have used L2 norm. You can use L1 also.
width_AD = np.sqrt(((pt_A[0] - pt_D[0]) ** 2) + ((pt_A[1] - pt_D[1]) ** 2))
width_BC = np.sqrt(((pt_B[0] - pt_C[0]) ** 2) + ((pt_B[1] - pt_C[1]) ** 2))
maxWidth = max(int(width_AD), int(width_BC))

height_AB = np.sqrt(((pt_A[0] - pt_B[0]) ** 2) + ((pt_A[1] - pt_B[1]) ** 2))
height_CD = np.sqrt(((pt_C[0] - pt_D[0]) ** 2) + ((pt_C[1] - pt_D[1]) ** 2))
maxHeight = max(int(height_AB), int(height_CD))


def main():
    image = '/home/santhosh/environments/python/ccms/ccms/raw_documents/33-1-2013/33-1-2013-1.png'
    init_point_list = []
    drawing = False
    window[graph].draw_image(filename=image, location=(0,800))
    while True:
        event, value = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Cancel' or event == '-CLOSE-' or event is None:
            window.close()
            break
        if event == draw:
            drawing = True
        if event == graph:
            if drawing:
                x,y = value[graph]
                print(x,y)
                init_point_list.append((x,y))
                if len(init_point_list) <= 8:
                    window[graph].draw_point( point=(x,y),size=10, color='red')
                    if len(init_point_list) >1:
                        window[graph].draw_lines(points = init_point_list, color='red', width=2)
                        if len(init_point_list) == 8:
                            window[graph].draw_line(point_from=init_point_list[0],point_to=init_point_list[7], color='red', width=2)
            if len(init_point_list) == 8:
                drawing = False

        if event == 'crop':
            if len(init_point_list) == 8:
                point_list = converting_points(init_point_list)
                img = cv2.imread(image)

                print(point_list)
                converting_points(point_list)
                height, width = img.shape[:2]
                # ps1 =  np.array([[10,5],[20,30],[70,20],[50,10]], np.int32)

                ps1 = np.float32([point_list[0],point_list[2],point_list[4],point_list[6]])
                ps1 = ps1.reshape((-1, 1, 2))

                pts2 = np.float32([[0,0],[800,0],[800,600],[0,600]])
                crop_points = cv2.getPerspectiveTransform(ps1,pts2)
                new_img = cv2.warpPerspective(img,crop_points,(800, 600), borderValue=(255,255,255,255))
                # new_img = cv2.rotate(img,cv2.ROTATE_90_CLOCKWISE)
                # # new_img = cv2.flip(new_img,0)
                # cv2.polylines(img, [ps1], isClosed=True, color=(0,255,235))
                cv2.imwrite('../ccms/raw_documents/12-1-2013/12-1-2013-1.png', new_img)
                window[graph].erase()

                window[graph].draw_image(data=cv2.imencode('.png',new_img )[1].tobytes(), location=(0,800))
            # window[graph].draw_polygon(points=[(252, 753),(259, 341),(591, 390),(591, 793),],fill_color='green')
            print('cropped')
            # else:
            #     print(point_list)


main()