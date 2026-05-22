
import getpass
import datetime as dt 
from pydantic import BaseModel,model_validator
from static_varibles import yaml_path
import yaml
import os

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
    local_path:str = fr"C:\Users\{getpass.getuser()}\Documents\Report"
    base_report_file:str
    sap_verify : dict[int,int|None]
    path_local_mapping :dict[str,str] ={}
    sap_list :list[int] =[]
    _interpolate_months:list[str] = []
    @model_validator(mode='after')
    def _initialize_filed(self):
        self._interpolate_months = self._get_short_months()
        self.sap_list =[899584, 2978308, 3233925, 4188677, 3294343, 3294344, 714632, 2378250, 3212044, 2304147, 3389335, 2423192, 1440924, 3210271, 3210272, 3601183, 3307814, 3322285, 3000750, 3322289, 3222451, 3294389, 3349561, 1282368, 2930496, 2495170, 2569287, 3242956, 2237774, 1485264, 2253393, 3210195, 3225301, 3337942, 3225303, 1088091, 2253539, 1264229, 3302117, 2229993, 3212020, 3294333]
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
                    
                    mapping[os.path.join(month_folder_path_network,f"{temp}")] = os.path.join(month_folder_path_local,temp)
            
        return mapping
        


        
def create_profile()->Profile:
    with open(yaml_path,mode='r',encoding='utf-8') as f :
        data = yaml.safe_load(f)
    
    
        pro5 :Profile = Profile(**data['profile'])
        return pro5    

