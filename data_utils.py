import shutil
from concurrent.futures import ThreadPoolExecutor,as_completed
import os 
import getpass
import io
import msoffcrypto
import polars as pl
from helper import Helper as hp
from file_handler import FileHelper
class DataIngestor:
    def __init__(self,paths_map:dict[str,str]):
        self.paths_map = paths_map
        
    def ingest_data(self):
        try:
            if len(self.paths_map) < 2:
                k,v = list(self.paths_map.items())[0]
                return self.single_file_transfer(k,v)
            return self.concurent_file_transfer()
        
        except IndexError as e :
            hp.show_error(e.errno ,"Vui lòng kiểm tra phần SAP của file config vui lòng chọn ít nhất 1 SAP")

            
        
    def load_single_file(self,p_src:str,p_dest:str):
            FileHelper.file_transfer(p_src,p_dest)
            data:io.BytesIO = self.load_data_with_key(p_dest,"J@bil2022")
            data.seek(0)
            df:pl.DataFrame = pl.read_excel(data,engine="calamine")
            return df
    
    
    def load_multiple_files(self):
        data_list : list[pl.DataFrame]=[]
        
        with ThreadPoolExecutor(max_workers=5) as exe :
                
            futures = [exe.submit(self.single_file_transfer,src,dest) for src,dest in self.paths_map.items()]
            for f in as_completed(futures):
                data_list.append(f.result())
        return pl.concat(data_list,rechunk=True,strict=True,parallel=True)
    

    
    
    def load_data_with_key(self,path:str, p:str) -> io.BytesIO:
        
                with open(path, 'rb') as file:
                        office_file :msoffcrypto.OfficeFile = msoffcrypto.OfficeFile(file)
                        office_file.load_key(p)
                        decrypted : io.BytesIO = io.BytesIO()
                        office_file.decrypt(decrypted)
                        return decrypted
