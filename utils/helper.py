import ctypes
import traceback
import sys

try:
    ctypes.windll.user32.SetProcessDpiAwarenessContext(ctypes.c_void_p(-4))
except Exception:
    pass


class Helper:
    @staticmethod
    def show_traceback_exception(except_type: any, value: str, tb: any):
        ctypes.windll.user32.MessageBoxW(
            0,
            "".join(traceback.format_exception(except_type, value, tb)),
            "Exception",
            0x10,
        )
        sys.exit(1)