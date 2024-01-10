# C:\Program Files (x86)\digiCamControl>cameracontrolcmd.exe /liveview

import subprocess


# path = 'C:\Program Files (x86)\digiCamControl>CameraControlRemoteCmd.exe /c capture c:\pictures\capture1.jpg'
# out = subprocess.Popen(path, stdout=subprocess.PIPE, shell=True)

camera_command = 'C:\Program Files (x86)\digiCamControl\CameraControlCmd.exe'
# camera_command_details = '/filename ./' + 'santhosh' + ' /capture /iso 500 /shutter 1/30 /aperture 1.8'
camera_command_details = '/liveview'
print('camera details = ',camera_command_details)
full_command=camera_command + ' '
p = subprocess.Popen(full_command, stdout=subprocess.PIPE, universal_newlines=True, shell=False)
(output, err) = p.communicate()
print(output)
print(err)

