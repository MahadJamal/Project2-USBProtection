'''
Usage: python3 usb_eject.py
OS: Window7 and later
Eject the usb storage when the usb device plugin your PC!
'''
from time import sleep
#import http.client
import subprocess
import Password_GUI
import EjectorThread
import threading


def callMakeGUI():
    Password_GUI.makeGUI()

def monitorUSBStorage():
    label = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S',
    'T','U','V','W','X','Y','Z']
    monitorDisk = []
    makeGUI = 0
    for i in label:
        try:
            file = open(i+':/')
        except Exception as e:
            '''
            error = 2  =>not found
            error = 13 =>permission denied (exist!)
            '''
            if(e.errno == 13):
                print("Disk : "+i+" Exist!")
            else:
                monitorDisk.append(i)

    print("Start monitoring.....")
    while(True):
        print("Check...")
        isININ = False;
        disk = '';
        for i in monitorDisk:
            try:
                file = open(i+':/')
            except Exception as e:
                if(e.errno == 13):

                    makeGUI = 1
                    # EjectorThread(name='GUI thread', target=callMakeGUI).start()
                    #threading.Thread(target=Password_GUI.sum).start()
                    #EjectorThread(name='Ejector thread', target=ejector).start()
                    if(Password_GUI.AuthSuccess):
                        isININ = False
                        makeGUI = 0
                        break
                    else:
                        print("Disk : "+i+" Added!")
                        isININ = True
                        disk = i
                        break
        threading.Thread(target=ejector,args=[disk,isININ]).start()
        #EjectorThread(name='Ejector thread', target=ejector).start()
        if(makeGUI):
            callMakeGUI()
        # if(isININ):
        #     tmpFile = open('tmp.ps1','w')
        #     tmpFile.write('$driveEject = New-Object -comObject Shell.Application\n')
        #     tmpFile.write('$driveEject.Namespace(17).ParseName("'+disk+':").InvokeVerb("Eject")')
        #     tmpFile.close()
        #     process = subprocess.Popen(['powershell.exe', '-ExecutionPolicy','Unrestricted','./tmp.ps1'])
        #     callMakeGUI()
        #     process.communicate()

        #sleep for 2 seconds
        sleep(1)

def ejector(disk, isININ):
    print('Ejector Started')
    if (isININ):
        tmpFile = open('tmp.ps1', 'w')
        tmpFile.write('$driveEject = New-Object -comObject Shell.Application\n')
        tmpFile.write('$driveEject.Namespace(17).ParseName("' + disk + ':").InvokeVerb("Eject")')
        tmpFile.close()
        process = subprocess.Popen(['powershell.exe', '-ExecutionPolicy', 'Unrestricted', './tmp.ps1'])
        process.communicate()



if __name__ == '__main__':
    monitorUSBStorage()