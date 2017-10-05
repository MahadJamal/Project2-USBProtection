# Project 2

##Files Included:

1) main.py <br/> 
2) USBEject.py <br/> 
3) Password_GUI.py <br/> 
4) CheckUserPassword.py <br/> 

### 1) main.py
_**main.py**_ is responsible for the structural flow of the program. It calls `USBEJECT_initialdrives()` method of USBEJECT class. Next it makes two threads to monitor if a new drive have been added as well to eject if any new drive is added.

The callback functions for the threads are `USBEJECT\_monitorUSB` and `USBEJECT\_ejector`. These methods are called using the  USBEJECT class object.


    usbhandler = USBEJECT()
    usbhandler.USBEJECT_initialdrives(usbhandler.label, usbhandler.monitorDisk)
    threading.Thread(target=usbhandler.USBEJECT_monitorUSB, args = [usbhandler.monitorDisk,usbhandler.isININ]).start()
    threading.Thread(target=usbhandler.USBEJECT_ejector).start()

When a USB is detected (i.e. a new drive is added to PC) the `USBEJECT_ejector` method ejects the drive using power shell. A GUI is created in the mainthread which prompts the user for username and password to enale USB drive. 

NOTES: <br/> 
i) Tkinter can only run in mainthread therefore all the other processes of the program are put in secondary and tertiary threads. The ejector method runs an infinite while loop to eject USB drives if detected so that the thread keeps on running in the background at all times. <br/>
ii) The username and password are store in sqlite database. This database is maintained separately and the main program does not allow to add or modify database entries. Python has built-in server and support for sqlites.<br/>
iii) Work is in progress for performing authentication using email.


### 2) USBEject.py
***USBEject.py*** defines the class `USBEJECT`. This class has three methods namely:
 
1. USBEJECT_initialdrives. 
2. USBEJECT_monitorUSB. 
3. USBEJECT_ejector.

The function of these methods has already been explained in the first part of this document. Whats important here is that the production of GUI is controlled by `makeGUI` class variable, the eject process is controlled by `isININ` object variable and a list `USBDisk` is maintained as class 'sequence object' to hold the name of new USB devices added to the PC. This list is updated everytime a USB storage device is added or removed.


### 3) Password_GUI.py
***Password_GUI.py*** contains all the graphical user interface code.  

NOTES: I was trying to run tkinter in a separate thread but the code does not working,  the reason is that tkinter can only run in main thread. Therefore if i really want the GUI to run in separate thread than we can use PyQt4. The other solution is to run the tkinter in mainloop and do rest of the work in separate threads.


### 4) CheckUserPassword.py
***CheckUserPassword.py*** connects to the sqlite database and checks whether the username and password that the user entered matches with any of the table entries in the database. The `connect()` function connects to the database and initializes a table if there is none so that the `checkUser(name)` function does not produces any error in case there is no database. 

NOTES: `checkUser(name)` function is being modified to perform authentication using email.

##Work in Progress:


1. A method is being introduced to add,edit and update the user/password database by authorized user of PC.
2. A proper was is needed to close the GUI window without destroying the tkinter object as it throws an exception. The tkinter library is designed to run from start to the end of program so it is hard to bring up the GUI in the middle of program and than close it and then reopen it in case a USB device is detected again. 
3. The program should run from start of the OS until the OS is shutdown. Right now this can be done in windows using windows scheduler utility but this process should be automatic. 
4. Authentication should be also done using email for more security.
5. When USB storage is removed the USBDisk list needs to be updated to remove the disk label.