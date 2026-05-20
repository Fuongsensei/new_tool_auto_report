import ctypes



class Helper:
    @staticmethod
    def show_error(errno:int ,message:str):
        ctypes.windll.user32.MessageBoxW(0,message,f"Mã lỗi : {errno}",0x10)
