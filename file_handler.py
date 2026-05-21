import os 
import shutil
from helper import Helper 
class FileHelper():
    def __init__(self):
        pass
        
    @staticmethod
    def create_folder(folder_path:str|list[str],parrent_folder:bool=False):

            
        if folder_path:
            if parrent_folder:
            
                folder_path = folder_path.rsplit("\\",1)[0]
                os.makedirs(folder_path,exist_ok=True)
        else:
            print("Đường dẫn không hợp lệ")
        
    @staticmethod
    def file_transfer(src:str,dest:str):
        try:
            if os.path.exists(src):
                    shutil.copy(src,dest)
            else:
                Helper.show_error(None,f"Đường dẫn gốc không hợp lệ !{src}")
       
        except Exception as e:
            Helper.show_error(e.errno,"File đích chưa được tạo ! hãy kiểm tra lại")
            os._exit(0)
        
    @staticmethod    
    def remove_folder(path:str):
        try:
            shutil.rmtree(path)
        except FileNotFoundError as e : 
            Helper.show_error(e.errno,"Không tìm thấy đường dẫn file cần xóa!")
