import polars as pl
import static_varibles as sv 
import datetime as dt

import yaml as yml
import os
import io
import msoffcrypto
import fastexcel
import time 
import getpass
import shutil
import static_varibles as sv 
from pydantic import BaseModel,model_validator
import helper as hp

class DataProcess:
    def __init__(self):
        self.dcfig : DataConfig = DataConfig(sv.path_yaml)
        self.cf = self.dcfig.config 
        
        
    def Process(self,data:pl.DataFrame):
        
        df_raw : pl.DataFrame = data
        a = dt.datetime.strptime(self.cf.from_date,"%m/%d/%Y").replace(hour=int(self.cf.from_time),minute=int(self.cf.from_minute),second=int(self.cf.from_second))
        
        
        b = dt.datetime.strptime(self.cf.to_date,"%m/%d/%Y").replace(hour=int(self.cf.to_time),minute=int(self.cf.to_minute),second=int(self.cf.to_second))     
        
        self.df_processed = df_raw.lazy().filter(    
            ( pl.nth(5).str.split("|").list.get(1).str.strptime(pl.Datetime,"%m/%d/%Y %I:%M:%S %p",strict=False).is_between(a,b)) &
             ( pl.nth(5).str.split("|").list.get(0).is_in(self.cf.sap_list)) &
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
    short_month :int
    year:int
    sap_verify : dict[int,int|None]
    path_map_local :dict[str,str] ={}
    sap_list :list =[]
    
    @model_validator(mode='after')
    def create_folder_path(self):
        short_month_parse = dt.date(2000,self.short_month,1).strftime("%b")
        self.folder_path  = os.path.join(self.base_report_file,f"{short_month_parse} {self.year}")
        return self
   
    @model_validator(mode='after')
    def create_files_path(self):
            for k,v in self.sap_verify.items():
                if self.sap_verify[k] == 1:
                    print(k)
                    self.sap_list.append(str(k))
                    p :str =os.path.join(self.folder_path,f"GR Verification {k}.xlsx")
                    self.path_map_local[p] = rf"C:\Users\3601183\Documents\SAP_Scan\GR Verification {k}.xlsx"
            return self
                
                
                


        
        
        
        
class DataConfig:   
    def __init__(self,path_config:str):
         with open(path_config,'r',encoding='utf-8') as cf:
            self.config  :TypeConfig = TypeConfig(**yml.safe_load(cf))
            



                        
