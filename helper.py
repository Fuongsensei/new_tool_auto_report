import ctypes
import traceback
import sys
try:
        ctypes.windll.user32.SetProcessDpiAwarenessContext(ctypes.c_void_p(-4))
except:
        pass

class Helper:
        @staticmethod
        def show_error(errno:int ,message:str):
                if errno!=None:
                        ctypes.windll.user32.MessageBoxW(0,message,f"Mã lỗi : {errno}",0x10)
                else:
                        ctypes.windll.user32.MessageBoxW(0,message,f"Mã lỗi : Không xác định !",0x10)
                        
        def show_traceback_exception(except_type:any,value:str,tb:any):
                ctypes.windll.user32.MessageBoxW(0,"".join(traceback.format_exception(except_type,value,tb)),"Exception",0x10)
                sys.exit(1)

