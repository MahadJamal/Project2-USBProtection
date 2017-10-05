from USBEject import USBEJECT
import Password_GUI
import threading


usbhandler = USBEJECT()
usbhandler.USBEJECT_initialdrives(usbhandler.label, usbhandler.monitorDisk)
threading.Thread(target=usbhandler.USBEJECT_monitorUSB, args = [usbhandler.monitorDisk,usbhandler.isININ]).start()
threading.Thread(target=usbhandler.USBEJECT_ejector).start()
while(True):
    if(USBEJECT.makeGUI):
        Password_GUI.makeGUI()
        USBEJECT.makeGUI = 0



