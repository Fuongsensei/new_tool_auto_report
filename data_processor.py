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
from typing  import Generic,TypeVar 
from pydantic import BaseModel,model_validator,field_validator,PrivateAttr
import helper as hp
import genericpath  

T = TypeVar("T",bound=BaseModel)
pYaml : str =  sv.path_yaml
class DataProcessBase(Generic[T]):
    def __init__(self,config:T):
        self.config :T = config



    def Process(self,data:pl.DataFrame):
        pass
    


class Profile(BaseModel):
    daily_report_config:dict = {}

class DailyConfig(BaseModel):
    from_date : dt.date
    from_time: int
    from_minute:int
    from_second:int
    to_date : dt.date
    to_time : int
    to_minute:int
    to_second:int
    base_report_file:str
    sap_verify : dict[int,int|None]
    path_map_local :dict[str,str] ={}
    sap_list :list[int] =[]
    sap_path_list :list[str]= []
    _interpolate_months:list[str] = []
    @model_validator(mode='after')
    def initialize_filed(self):
        self._interpolate_months  : list[str] = [dt.date(1,i,1).strftime("%b") for i in  range(self.from_date.month,self.to_date.month+1)]
        return self


        
def create_profile()->Profile:
    with open(r"C:\Users\3601183\Documents\Python\new_tool_auto_report\y.yml",mode='r',encoding='utf-8') as f :
        data = yml.safe_load(f)
    
    
        pro5 :Profile = Profile(**data['profile'])
        return pro5    



pro5 = create_profile()
data = DataProcessBase(DailyConfig(**pro5.daily_report_config))
print(data.config._interpolate_months)

