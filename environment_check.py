import ctypes
from ctypes.wintypes import RECT
from PySide2 import QtWidgets
import sys

def get_monitors_size_and_position():
    monitors = []
    offsets = []
    def size_callback(monitor, dc, rect, data):
        monitors.append((rect[0], rect[1], rect[2], rect[3]))
        return True
    def offset_callback(hMonitor, hdcMonitor, lprcMonitor, dwData):
        rect = lprcMonitor.contents
        offsets.append((rect.top, rect.bottom))
        return True
    EnumDisplayMonitors = ctypes.windll.user32.EnumDisplayMonitors
    size_callback_type = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_ulong, ctypes.c_ulong, ctypes.POINTER(ctypes.c_int), ctypes.c_int)
    offset_callback_type = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_ulong, ctypes.c_ulong, ctypes.POINTER(RECT), ctypes.c_ulong)
    EnumDisplayMonitors(None, None, size_callback_type(size_callback), None)
    EnumDisplayMonitors(None, None, offset_callback_type(offset_callback), None)
    if len(monitors) >= 2:
        main_left, main_top, main_right, main_bottom = monitors[0]
        main_width = main_right - main_left
        main_height = main_bottom - main_top
        second_left, second_top, second_right, second_bottom = monitors[1]
        second_width = second_right - second_left
        second_height = second_bottom - second_top
        if second_left > main_left:
            position = "right"
        else:
            position = "left"
        return (main_width, main_height), (second_width, second_height), position, offsets[1][0]
    elif len(monitors) == 1:
        main_left, main_top, main_right, main_bottom = monitors[0]
        main_width = main_right - main_left
        main_height = main_bottom - main_top
        return (main_width, main_height), None, None, None
    else:
        return None, None, None, None

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main, second, position, offset = get_monitors_size_and_position()
    if main:
        print("Main monitor size:", main[0], "x", main[1])
    else:
        print("Main monitor is not connected")
    if second:
        print("Second monitor size:", second[0], "x", second[1])
        print("Second monitor is on the", position, "side of the main monitor")
    else:
        print("Second monitor is not connected")
    print(offset)
