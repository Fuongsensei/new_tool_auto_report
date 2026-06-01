import shutil
from concurrent.futures import ThreadPoolExecutor,as_completed
import os 
import getpass
import io
import msoffcrypto
import threading 
import polars as pl
from helper import Helper as hp
from file_handler import FileHelper
from xlsx2csv import Xlsx2csv
class DataIngestor:
    def __init__(self,paths_map:dict[str,str]):
        self.paths_map : dict[str,str] = paths_map
        self.paths_folder_locals : set[str] = set([os.path.dirname(v) for k,v in paths_map.items()])
        self.file_error:list[str] =[]

                
    def ingest_data(self):

        if not self.paths_map:
            
            hp.show_error(None, "Vui lòng chọn ít nhất 1 SAP")
            return
        if len(self.paths_map) == 1 :
            s,d = list(self.paths_map.items())[0]
            
            data_single : pl.DataFrame = self.load_single_file(s,d)
            FileHelper.remove_folder(d)
            return data_single
        
        data : pl.DataFrame = self.load_multiple_files()
        for i in self.paths_folder_locals:
            FileHelper.remove_folder(i)
        return data
        
    def load_single_file(self,src_p:str,dest_p:str) -> pl.DataFrame:

            if os.path.exists(src_p):
                FileHelper.create_folder(dest_p)
                FileHelper.file_transfer(src_p,dest_p)
                data:io.BytesIO = self._load_data_with_key(dest_p,"J@bil2022")
                data.seek(0)
                df:pl.DataFrame = pl.read_excel(data,infer_schema_length=0,has_header=False)
                df = df.slice(1)
                df = df.select(df.columns[:14])
                df.columns  = [
                                "GRN", "MPN", "DC", "LOT (1T)", "Qty", 
                                "User/Time", "MPN SAP", "DC SAP", "LOT SAP (1T)", 
                                "MPN Verify", "DC Verify", "LOT Verify", 
                                "Stk Placement", "Qty Ver"]
                
                
            
                if df is not None and not df.is_empty():
                    return df
                else:
                    self.file_error.append(src_p)

    
    def load_multiple_files(self) -> list[pl.DataFrame]:
        data_list : list[pl.DataFrame]=[]

        with ThreadPoolExecutor(max_workers=10) as exe :
                futures = [exe.submit(self.load_single_file,src,dest) for src,dest in self.paths_map.items()]
                for f in as_completed(futures):
                        if f.result() is not None:
                            data_list.append(f.result())

        return pl.concat(data_list,rechunk=True,strict=True,parallel=True)

    

    
    
    def _load_data_with_key(self,path:str, p:str) -> io.BytesIO:
        
                with open(path, 'rb') as file:
                        
                        office_file :msoffcrypto.OfficeFile = msoffcrypto.OfficeFile(file)
                        if office_file.is_encrypted():
                            office_file.load_key(p)
                            decrypted : io.BytesIO = io.BytesIO()
                            office_file.decrypt(decrypted)
                            return decrypted
                        else:
                            file.seek(0)
                            return io.BytesIO(file.read())
                        
                        
                        
