
import getpass
import datetime as dt 
from pydantic import BaseModel,model_validator
from utils.static_variables import yaml_path,yaml_path_home
import yaml
import os
from utils.helper import Helper
import sys 
from typing import Dict, Union

class  Profile(BaseModel):
    daily_report_config:dict 


class DailyConfig(BaseModel):
      verify_config :dict
      grn_10_numbers_config:dict 
      grn_16_numbers_config:dict

class VerifyConfig(BaseModel):
    from_date : dt.datetime
    from_hour: int
    from_minute:int
    from_second:int
    to_date : dt.datetime
    to_hour : int
    to_minute:int
    to_second:int
    local_path:str = fr"C:\Users\{getpass.getuser()}\Documents\Report"
    report_daily_path : str
    base_report_file: str =  r"\\AWASE1HCMICAP01\AppsData\GR Ver Report"
    sap_rcv : dict[int, dict[str, str | int]]
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
        
        for k,v in self.sap_rcv.items():
            if v['FLAG']:
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
        

class GRN10Config(BaseModel):
      sheet_name:str
      posting_date_start:str | None = None
      posting_date_end:str | None = None
      entered_date_start:str | None = None
      entered_date_end  :str | None = None

      from_date:dt.date
      to_date : dt.date
      file_name:str
      file_path:str
      number_format_string:str
      number_format_date  :str
      columns_string_format:list[str]
      columns_date_format  :list[str]
      drop_columns : list[int]
      year:int | None = None
      tcode :str = "z_invmvmts"
      @model_validator(mode="after")

      def _initialize_field(self):
           self.year = self.from_date.year
           self.posting_date_start = self.from_date.strftime("%m/%d/%Y")
           self.posting_date_end  = self.to_date.strftime("%m/%d/%Y")
           self.entered_date_start = (self.from_date - dt.timedelta(3)).strftime("%m/%d/%Y")
           self.entered_date_end  = self.posting_date_end
           self.file_name = f"EXPORT_GRN10_{self.from_date}"
           self.file_path = rf"C:\Temp\{self.file_name}.xlsx"
           return self



class GRN16Config(BaseModel):
           sheet_name : str
           from_date : dt.date
           to_date : dt.date
           entered_date_start:str | None = None
           entered_date_end  :str | None = None
           file_name :str
           file_path:str
           number_format_string:str
           number_format_date:str
           columns_string_format:list[str]
           columns_date_format : list[str]
           drop_columns : list[int]
           
           @model_validator(mode='after')
           def _initialize_field(self):
                self.entered_date_start = (self.from_date - dt.timedelta(3)).strftime("%m/%d/%Y")
                self.entered_date_end = self.to_date.strftime("%m/%d/%Y")
                self.file_name =  f"EXPORT_GRN16_{self.from_date}"
                self.file_path = rf"C:\Temp\{self.file_name}.xlsx"
                return self

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


      