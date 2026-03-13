import polars as pl
import static_varibles as sv 
import datetime as dt

import yaml as yml
import os
import io
import msoffcrypto
import fastexcel
import time 
import shutil
import static_varibles as sv 
from pydantic import BaseModel,model_validator

class DataProcess:
    def __init__(self):
        self.dcfig : DataConfig = DataConfig(sv.path_yaml)
        self.cf = self.dcfig.config 
    def Process(self,data:io.BytesIO):
        self.df_raw :pl.DataFrame = pl.read_excel(data,engine="calamine")
        a = dt.datetime.strptime(self.cf.to_date,"%m/%d/%Y").replace(hour=int(self.cf.from_time),minute=int(self.cf.from_minute),second=int(self.cf.from_second))
        
        
        b = dt.datetime.strptime(self.cf.to_date,"%m/%d/%Y").replace(hour=int(self.cf.to_time),minute=int(self.cf.to_minute),second=int(self.cf.to_second))     
        
        print(a)
        print(b)
        self.df_processed = self.df_raw.lazy().filter(    
            ( pl.nth(5).str.split("|").list.get(1).str.strptime(pl.Datetime,"%m/%d/%Y %I:%M:%S %p").is_between(a,b)) &
            (pl.nth(9)==True)&
            (pl.nth(10)==True)&
            (pl.nth(11)==True)&
            (pl.nth(13)==True)).select(
                pl.nth([0,1,2,3,4,5,6,7,8,9,10,11,13])
            ).collect()
        return self.df_processed
        
class TypeConfig(BaseModel):
    from_date : str 
    to_date : str
    from_time: str
    to_time : str
    from_minute:str
    from_second:str
    to_minute:str
    to_second:str
    base_report_file:str
    folder_path:str
    sap_verify : dict
    files_paths_contain : list 
    
    @model_validator(mode='after')
    def create_folder_path(self):
        short_month :str = dt.date.today().strftime('%b')
        year : int =  dt.date.today().year
        self.folder_path  = os.path.join(self.base_report_file,f"{short_month} {year}")
        return self
   
    @model_validator(mode='after')
    def create_files_path(self):
        for k,v in self.sap_verify.items():
            if self.sap_verify[k] == 1:
                print(self.sap_verify[k])
                self.files_paths_contain.append(os.path.join(self.folder_path,f"GR Verification {k}.xlsx"))
        print(self.files_paths_contain[0])    
        return self 

        
        
        
        
class DataConfig:   
    def __init__(self,path_config:str):
         with open(path_config,'r') as cf:
            self.config  :TypeConfig = TypeConfig(**yml.safe_load(cf))
            


def load_data_with_key(path:str, p:str) -> None:
        
                with open(path, 'rb') as file:
                        office_file :msoffcrypto.OfficeFile = msoffcrypto.OfficeFile(file)
                        office_file.load_key(p)
                        decrypted : io.BytesIO = io.BytesIO()
                        office_file.decrypt(decrypted)
                        return decrypted
                        
byte_f  =  load_data_with_key(r"\\AWASE1HCMICAP01\AppsData\GR Ver Report\Mar 2026\GR Verification 3601183.xlsx","J@bil2022")
byte_f.seek(0)


df  = DataProcess().Process(byte_f)

print(df)

