import os 
import shutil
from utils.helper import Helper 
class FileHelper:
    def __init__(self):
        pass
        
    @staticmethod
    def create_folder(folder_path:str|list[str]):

            
        if folder_path:
            
            os.makedirs(os.path.dirname(folder_path),exist_ok=True) if not  os.path.isdir(folder_path) else os.makedirs(folder_path,exist_ok=True)
            
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
            
            Helper.show_error(e.errno,"File đích chưa được tạo hãy kiểm tra lại !")
            
            os._exit(0)
        
    @staticmethod    
    def remove_folder(path:str):
        try:
            
            if path:
                
                shutil.rmtree(os.path.dirname(path)) if not os.path.isdir(path) else shutil.rmtree(path)
            
        except FileNotFoundError as e : 
            
            Helper.show_error(e.errno,"Không tìm thấy đường dẫn file cần xóa!")
