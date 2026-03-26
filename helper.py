import ctypes



class Helper:
    def __init__(self) -> None:
        pass
    def show_error(title,message):
        ctypes.windll.user32.MessageBoxW(0,message,title,0x10)
