from time import sleep
import subprocess
import Password_GUI


class USBEJECT():
    USBDisk = []
    makeGUI = 0
    def __init__(self):
        self.label = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.monitorDisk = []
        self.isININ = False


    def USBEJECT_initialdrives(self, label, monitorDisk):
        for i in label:
            try:
                file = open(i + ':/')
            except Exception as e:
                '''
                error = 2  =>not found
                error = 13 =>permission denied (exist!)
                '''
                if (e.errno == 13):
                    print("Disk : " + i + " Exist!")
                else:
                    monitorDisk.append(i)


    def USBEJECT_monitorUSB(self, monitorDisk, isININ):
        print("Start monitoring.....")
        while (True):
            print("Check...")
            disk = '';
            for i in monitorDisk:
                try:
                    file = open(i + ':/')
                except Exception as e:
                    if (e.errno == 13):
                        USBEJECT.USBDisk.append(i)  #Appended everytime. We only need once. Also it only detects one USB at a time
                        print(USBEJECT.USBDisk)
                        USBEJECT.makeGUI = 1
                        if (Password_GUI.AuthSuccess):
                            self.isININ = False
                            USBEJECT.makeGUI = 0
                            break
                        else:
                            print("Disk : " + i + " Added!")
                            self.isININ = True
                            print(self.isININ)
                            disk = i
                            break
            sleep(1)

    def USBEJECT_ejector(self):
        print('Ejector Started')
        while(True):
            if (self.isININ):
                tmpFile = open('tmp.ps1', 'w')
                tmpFile.write('$driveEject = New-Object -comObject Shell.Application\n')
                tmpFile.write('$driveEject.Namespace(17).ParseName("' + USBEJECT.USBDisk[0] + ':").InvokeVerb("Eject")')
                tmpFile.close()
                process = subprocess.Popen(['powershell.exe', '-ExecutionPolicy', 'Unrestricted', './tmp.ps1'])
                process.communicate()

