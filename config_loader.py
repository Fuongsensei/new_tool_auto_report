
import getpass
import datetime as dt 
from pydantic import BaseModel,model_validator
from static_varibles import yaml_path,yaml_path_home
import yaml
import os
from helper import Helper
import sys 

class Profile(BaseModel):
    daily_report_config:dict = {}

class DailyConfig(BaseModel):
    from_date : dt.datetime
    from_hour: int
    from_minute:int
    from_second:int
    to_date : dt.datetime
    to_hour : int
    to_minute:int
    to_second:int
    local_path:str = fr"C:\Users\{getpass.getuser()}\Documents\Report"
    base_report_file: str =  r"\\AWASE1HCMICAP01\AppsData\GR Ver Report"
    sap_verify : dict[int,int|None]
    path_local_mapping :dict[str,str] ={}
    sap_list :list[int] =[]
    _interpolate_months:list[str] = []
    
    
    @model_validator(mode='after')
    
    def _initialize_filed(self):
        self._interpolate_months = self._get_short_months_and_year()
        self.sap_list = self._create_sap_list()
        self.path_local_mapping = self._create_path_mapping()
        return self
        
    def _get_short_months_and_year(self)->list[str] :
        from_year,from_month = (self.from_date.year,self.from_date.month)
        to_year,to_month     = (self.to_date.year,self.to_date.month)
        
        if from_year != to_year:
            if to_year < from_year:
                Helper.show_error(None,"Năm trước không được lớn hơn năm sau !")
            else:
                to_month+=((to_year-from_year)*12)

                temp : list[str] = []
                for y in range(from_year,to_year+1):
                    for m in range(from_month,to_month+1):
                        if m %12 == 0:
                            temp.append(f"{dt.date(1,12,1).strftime("%b")} {y}") 
                            from_month=m+1
                            break
                        temp.append(f"{dt.date(1,m%12,1).strftime("%b")} {y}")
            return temp
        else:
            return [f"{dt.date(1,i,1).strftime("%b")} {from_year}" for i in range(from_month,to_month+1)]
                
    
    def _create_sap_list(self)-> list[int]|None :
        t:list[int] = []
        
        for k,v in self.sap_verify.items():
            if v:
                t.append(k)
        if  not len(t):
            print(len(t))
            Helper.show_error(None,"Phải chọn ít nhất 1 SAP")
            sys.exit(1)
            
            
        return t            
    
    def _create_path_mapping(self)->dict[str,str]:
        
        mapping : dict[str,str] = {}
        if getpass.getuser() == "fuongsensei":
            self.base_report_file = r"E:\AWASE1HCMICAP01\AppsData\GR Ver Report"
        base_network : str = self.base_report_file
        base_local   : str = self.local_path
        for s in self.sap_list:
            temp: str = f"GR Verification {s}.xlsx"
            for month_and_year_folder in self._interpolate_months:
                mapping[os.path.join(os.path.join(base_network,month_and_year_folder),temp)] = os.path.join(os.path.join(base_local,month_and_year_folder),temp)
            
        return mapping
        


        
def create_profile()->Profile:
    path = yaml_path if not getpass.getuser() == "fuongsensei" else yaml_path_home
    try:
        with open(path,mode='r',encoding='utf-8') as f :
            data = yaml.safe_load(f)
        
            
            pro5 :Profile = Profile(**data['profile'])
            return pro5   
    
    except KeyError as erkey:
        Helper.show_error(None,type(erkey).__name__)
    except Exception as e:
        Helper.show_error(type(e).__name__)
