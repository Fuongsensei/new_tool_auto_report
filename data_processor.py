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
    local_path:str = fr"C:\Users\{getpass.getuser()}\Documents"
    base_report_file:str
    sap_verify : dict[int,int|None]
    path_local_mapping :dict[str,str] ={}
    sap_list :list[int] =[]
    _interpolate_months:list[str] = []
    @model_validator(mode='after')
    def _initialize_filed(self):
        self._interpolate_months = self._get_short_months()
        self.sap_list = self._create_sap_list()
        self.path_local_mapping = self._create_path_mapping()
        return self
        
    def _get_short_months(self)->list[str] :
        return [dt.date(1,i,1).strftime("%b") for i in  range(self.from_date.month,self.to_date.month+1)]
    
    
    def _create_sap_list(self)-> list[int] :
        t:list[int] = []
        for k,v in self.sap_verify.items():
            if v:
                t.append(k)
        return t            
        return self
    
    def _create_path_mapping(self)->dict[str,str]:
        mapping : dict[str,str] = {}
        for s in self.sap_list:
                temp : str = f"GR Verification {s}.xlsx"
                for i in self._interpolate_months:
                    
                    month_folder_path_network = os.path.join(self.base_report_file,f"{i} {self.from_date.year}")
                    month_folder_path_local   = os.path.join(self.local_path,f"{i} {self.from_date.year}")
                    
                    mapping[os.path.join(month_folder_path_network,f"{temp}")] = os.path.join(month_folder_path_local,f"{temp}")
            
        return mapping
        


        
def create_profile()->Profile:
    with open(r"C:\Users\3601183\Documents\Python\new_tool_auto_report\y.yml",mode='r',encoding='utf-8') as f :
        data = yml.safe_load(f)
    
    
        pro5 :Profile = Profile(**data['profile'])
        return pro5    



# pro5 = create_profile()
# data = DataProcessBase(DailyConfig(**pro5.daily_report_config))

# print(data.config.path_local_mapping)
# with open(r"C:\Users\3601183\Documents\Python\new_tool_auto_report\test.txt",mode='w') as f :
#     f.write(str(data.config.path_local_mapping))

