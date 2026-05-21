import ctypes



class Helper:
    @staticmethod
    def show_error(errno:int ,message:str):
        if errno!=None:
                ctypes.windll.user32.MessageBoxW(0,message,f"Mã lỗi : {errno}",0x10)
        else:
                ctypes.windll.user32.MessageBoxW(0,message,f"Mã lỗi : Không xác định !",0x10)
