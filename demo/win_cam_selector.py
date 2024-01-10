import wmi
# import pywin32.client
import  os
c = wmi.WMI()


import subprocess, json

out = subprocess.getoutput("PowerShell -Command \"& {Get-PnpDevice | Select-Object Status,Class,FriendlyName,InstanceId | ConvertTo-Json}\"")
j = json.loads(out)
for dev in j:
    print(dev['Status'], dev['Class'], dev['FriendlyName'], dev['InstanceId'] )

my_system =  c.Win32_PhysicalMedia()
# print(my_system[2])

# print(c.Win32_ComputerSystem())
# c.
# for item in c.Win32_PhysicalMedia():
#     print(item)

# for drive in c.Win32_DiskDrive():
#     print(drive)
#
# for disk in c.Win32_LogicalDisk():
#     print(disk)
#
# for disk in c.Win32_PhysicalMedia

# os.system('pause')