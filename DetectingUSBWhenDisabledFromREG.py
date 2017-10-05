import win32serviceutil
import win32service
import win32event
import servicemanager

import win32gui
import win32gui_struct
struct = win32gui_struct.struct
pywintypes = win32gui_struct.pywintypes
import win32con

GUID_DEVINTERFACE_USB_DEVICE = "{A5DCBF10-6530-11D2-901F-00C04FB951ED}"
DBT_DEVICEARRIVAL = 0x8000
DBT_DEVICEREMOVECOMPLETE = 0x8004

import ctypes

#
# Cut-down clone of UnpackDEV_BROADCAST from win32gui_struct, to be
# used for monkey-patching said module with correct handling
# of the "name" param of DBT_DEVTYPE_DEVICEINTERFACE
#
def _UnpackDEV_BROADCAST (lparam):
  if lparam == 0: return None
  hdr_format = "iii"
  hdr_size = struct.calcsize (hdr_format)
  hdr_buf = win32gui.PyGetMemory (lparam, hdr_size)
  size, devtype, reserved = struct.unpack ("iii", hdr_buf)
  # Due to x64 alignment issues, we need to use the full format string over
  # the entire buffer.  ie, on x64:
  # calcsize('iiiP') != calcsize('iii')+calcsize('P')
  buf = win32gui.PyGetMemory (lparam, size)

  extra = {}
  if devtype == win32con.DBT_DEVTYP_DEVICEINTERFACE:
    fmt = hdr_format + "16s"
    _, _, _, guid_bytes = struct.unpack (fmt, buf[:struct.calcsize(fmt)])
    extra['classguid'] = pywintypes.IID (guid_bytes, True)
    extra['name'] = ctypes.wstring_at (lparam + struct.calcsize(fmt))
  else:
    raise NotImplementedError("unknown device type %d" % (devtype,))
  return win32gui_struct.DEV_BROADCAST_INFO(devtype, **extra)
win32gui_struct.UnpackDEV_BROADCAST = _UnpackDEV_BROADCAST

class DeviceEventService (win32serviceutil.ServiceFramework):

  _svc_name_ = "DevEventHandler"
  _svc_display_name_ = "Device Event Handler"
  _svc_description_ = "Handle device notification events"

  def __init__(self, args):
    win32serviceutil.ServiceFramework.__init__ (self, args)
    self.hWaitStop = win32event.CreateEvent (None, 0, 0, None)
    #
    # Specify that we're interested in device interface
    # events for USB devices
    #
    filter = win32gui_struct.PackDEV_BROADCAST_DEVICEINTERFACE (
      GUID_DEVINTERFACE_USB_DEVICE
    )
    self.hDevNotify = win32gui.RegisterDeviceNotification (
      self.ssh, # copy of the service status handle
      filter,
      win32con.DEVICE_NOTIFY_SERVICE_HANDLE
    )

  #
  # Add to the list of controls already handled by the underlying
  # ServiceFramework class. We're only interested in device events
  #
  def GetAcceptedControls(self):
    rc = win32serviceutil.ServiceFramework.GetAcceptedControls (self)
    rc |= win32service.SERVICE_CONTROL_DEVICEEVENT
    return rc

  #
  # Handle non-standard service events (including our device broadcasts)
  # by logging to the Application event log
  #
  def SvcOtherEx(self, control, event_type, data):
    if control == win32service.SERVICE_CONTROL_DEVICEEVENT:
      info = win32gui_struct.UnpackDEV_BROADCAST(data)
      #
      # This is the key bit here where you'll presumably
      # do something other than log the event. Perhaps pulse
      # a named event or write to a secure pipe etc. etc.
      #
      if event_type == DBT_DEVICEARRIVAL:
        print('USB_ADDED')
        servicemanager.LogMsg (
          servicemanager.EVENTLOG_INFORMATION_TYPE,
          0xF000,
          ("Device %s arrived" % info.name, '')
        )
      elif event_type == DBT_DEVICEREMOVECOMPLETE:
        servicemanager.LogMsg (
          servicemanager.EVENTLOG_INFORMATION_TYPE,
          0xF000,
          ("Device %s removed" % info.name, '')
        )

  #
  # Standard stuff for stopping and running service; nothing
  # specific to device notifications
  #
  def SvcStop(self):
    self.ReportServiceStatus (win32service.SERVICE_STOP_PENDING)
    win32event.SetEvent (self.hWaitStop)

  def SvcDoRun(self):
    win32event.WaitForSingleObject (self.hWaitStop, win32event.INFINITE)
    servicemanager.LogMsg (
      servicemanager.EVENTLOG_INFORMATION_TYPE,
      servicemanager.PYS_SERVICE_STOPPED,
      (self._svc_name_, '')
    )

if __name__=='__main__':
  win32serviceutil.HandleCommandLine (DeviceEventService)



#-------------------------------------------------------------------------

#
# import win32api, win32con, win32gui
# from ctypes import *
#
# #
# # Device change events (WM_DEVICECHANGE wParam)
# #
# DBT_DEVICEARRIVAL = 0x8000
# DBT_DEVICEQUERYREMOVE = 0x8001
# DBT_DEVICEQUERYREMOVEFAILED = 0x8002
# DBT_DEVICEMOVEPENDING = 0x8003
# DBT_DEVICEREMOVECOMPLETE = 0x8004
# DBT_DEVICETYPESSPECIFIC = 0x8005
# DBT_CONFIGCHANGED = 0x0018
#
# #
# # type of device in DEV_BROADCAST_HDR
# #
# DBT_DEVTYP_OEM = 0x00000000
# DBT_DEVTYP_DEVNODE = 0x00000001
# DBT_DEVTYP_VOLUME = 0x00000002
# DBT_DEVTYPE_PORT = 0x00000003
# DBT_DEVTYPE_NET = 0x00000004
#
# #
# # media types in DBT_DEVTYP_VOLUME
# #
# DBTF_MEDIA = 0x0001
# DBTF_NET = 0x0002
#
# WORD = c_ushort
# DWORD = c_ulong
#
# class DEV_BROADCAST_HDR (Structure):
#   _fields_ = [
#     ("dbch_size", DWORD),
#     ("dbch_devicetype", DWORD),
#     ("dbch_reserved", DWORD)
#   ]
#
# class DEV_BROADCAST_VOLUME (Structure):
#   _fields_ = [
#     ("dbcv_size", DWORD),
#     ("dbcv_devicetype", DWORD),
#     ("dbcv_reserved", DWORD),
#     ("dbcv_unitmask", DWORD),
#     ("dbcv_flags", WORD)
#   ]
#
# def drive_from_mask (mask):
#   n_drive = 0
#   while 1:
#     if (mask & (2 ** n_drive)): return n_drive
#     else: n_drive += 1
#
# class Notification:
#
#   def __init__(self):
#     message_map = {
#       win32con.WM_DEVICECHANGE : self.onDeviceChange
#     }
#
#     wc = win32gui.WNDCLASS ()
#     hinst = wc.hInstance = win32api.GetModuleHandle (None)
#     wc.lpszClassName = "DeviceChangeDemo"
#     wc.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW;
#     wc.hCursor = win32gui.LoadCursor (0, win32con.IDC_ARROW)
#     wc.hbrBackground = win32con.COLOR_WINDOW
#     wc.lpfnWndProc = message_map
#     classAtom = win32gui.RegisterClass (wc)
#     style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
#     self.hwnd = win32gui.CreateWindow (
#       classAtom,
#       "Device Change Demo",
#       style,
#       0, 0,
#       win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
#       0, 0,
#       hinst, None
#     )
#
#   def onDeviceChange (self, hwnd, msg, wparam, lparam):
#     #
#     # WM_DEVICECHANGE:
#     #  wParam - type of change: arrival, removal etc.
#     #  lParam - what's changed?
#     #    if it's a volume then...
#     #  lParam - what's changed more exactly
#     #
#     dev_broadcast_hdr = DEV_BROADCAST_HDR.from_address (lparam)
#
#     if wparam == DBT_DEVICEARRIVAL:
#       print ("Something's arrived")
#
#       if dev_broadcast_hdr.dbch_devicetype == DBT_DEVTYP_VOLUME:
#         print ("It's a volume!")
#
#         dev_broadcast_volume = DEV_BROADCAST_VOLUME.from_address (lparam)
#         if dev_broadcast_volume.dbcv_flags & DBTF_MEDIA:
#           print ("with some media")
#           drive_letter = drive_from_mask (dev_broadcast_volume.dbcv_unitmask)
#           print ("in drive", chr (ord ("A") + drive_letter))
#
#     return 1
#
# if __name__=='__main__':
#   w = Notification ()
#   win32gui.PumpMessages ()