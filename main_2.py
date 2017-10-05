from USBEject import USBEJECT
import Password_GUI
import threading
import os
import pyautogui
import time


def PressEnter():
    time.sleep(1)
    pyautogui.press('enter')
    pyautogui.PAUSE = 3
    pyautogui.press('enter')

def checkAuth():
    while(1):
        if(Password_GUI.AuthSuccess):
            threading.Thread(target=PressEnter).start()
            os.system("USB-Enable.reg")



threading.Thread(target=PressEnter).start()
os.system("USB-Disable.reg")
# usbhandler.USBEJECT_initialdrives(usbhandler.label, usbhandler.monitorDisk)
threading.Thread(target=checkAuth).start()








#do the rest of stuff here
# threading.Thread(target=PressEnter).start()
# os.system("USB-Enable.reg")





