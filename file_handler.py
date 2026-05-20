import os 
import shutil
from helper import Helper 
class FileHelper():
    def __init__(self):
        pass
    @staticmethod
    def file_transfer(src:str,dest:str):
        shutil.copy(src,dest)
        
        
    @staticmethod
    def create_folder(folder_path:str|list[str]):
        os.makedirs()
        
        
    @staticmethod    
    def remove_folder(path:str):
        try:
            shutil.rmtree(path)
        except FileNotFoundError as e : 
            Helper.show_error(e.errno,"Không tìm thấy đường dẫn file cần xóa!")
FileHelper.remove_folder(r"C:\Users\3601183\Documents\d")