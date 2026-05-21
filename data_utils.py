import shutil
from concurrent.futures import ThreadPoolExecutor,as_completed
import os 
import getpass
import io
import msoffcrypto
import polars as pl
from helper import Helper as hp
from file_handler import FileHelper
from xlsx2csv import Xlsx2csv
class DataIngestor:
    def __init__(self,paths_map:dict[str,str]):
        self.paths_map = paths_map
        self.local_paths : list[str] = [local_path[1] for local_path in self.paths_map.items()]
        self.local_csv_paths : list[str] = [s.replace(".xlsx",".csv") for s in self.local_paths]
        
    def convert_to_csv(self,path:str|list[str]) -> list[str]:
        pass
                
    def ingest_data(self):
            
        if not self.paths_map:
            hp.show_error(None, "Vui lòng chọn ít nhất 1 SAP")
            return


            
        
    def load_single_file(path_csv:str):
            
            data:io.BytesIO = self.load_data_with_key(path_csv,"J@bil2022")
            data.seek(0)
            df:pl.DataFrame = pl.read_csv(data)
            return df
    
    
    # def load_multiple_files(self):
    #     data_list : list[pl.DataFrame]=[]

    #     with ThreadPoolExecutor(max_workers=5) as exe :
    #             futures = [exe.submit(self.load_single_file,src,dest) for src,dest in self.paths_map.items()]
    #             for f in as_completed(futures):
    #                     data_list.append(f.result())
    #             return pl.concat(data_list,rechunk=True,strict=True,parallel=True)

    

    
    
    def load_data_with_key(self,path:str, p:str) -> io.BytesIO:
        
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
                        
                        
                        
