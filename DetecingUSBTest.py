# Does not work when you disable usb from registry but good at detecting mainly USBs
#  only without monitoring all the drive

def locate_usb():
    import win32file
    drive_list = []
    while(1):
        drivebits=win32file.GetLogicalDrives()
        for d in range(1,26):
            mask=1 << d
            if drivebits & mask:
                # here if the drive is at least there
                #print('drive detected')
                drname='%c:\\' % chr(ord('A')+d)
                t=win32file.GetDriveType(drname)
                if t == win32file.DRIVE_REMOVABLE:
                    drive_list.append(drname)
                    print('Now actually drive detected')
                    print(drive_list)
    return drive_list

locate_usb()
