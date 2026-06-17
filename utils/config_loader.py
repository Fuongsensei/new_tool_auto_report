
import getpass
import datetime as dt 
from pydantic import BaseModel,model_validator,PrivateAttr
from utils.static_variables import yaml_path,yaml_path_home
import yaml
import os
from utils.helper import Helper
import sys 
from polars import DataFrame

class VerifyConfig(BaseModel): 
    sheet_name:str
    from_date : dt.date
    to_date : dt.date
    from_time:dt.time
    to_time:dt.time
    local_path:str = fr"C:\Users\{getpass.getuser()}\Documents\Report"
    report_daily_path : str
    base_report_file: str =  r"\\AWASE1HCMICAP01\AppsData\GR Ver Report"
    sap_rcv : dict[int, dict[str, str | int]]
    path_local_mapping :dict[str,str] ={}
    verify_list :list[int] =[]
    _keyin_list  : DataFrame | None = PrivateAttr(default=None)
    _interpolate_months:list[str] = []
    run_sap : bool
    
    @model_validator(mode='after')
    
    def _initialize_filed(self):
        self._interpolate_months = self._get_short_months_and_year()
        self.verify_list = self._create_verify_list()
        self.path_local_mapping = self._create_path_mapping()
        self._keyin_list = DataFrame(self._create_keyin_list()).drop("FLAG")
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
                
    
    def _create_verify_list(self)-> list[int]|None :
        t:list[int] = []
        
        for k,v in self.sap_rcv.items():
            if v['FLAG'] == 1 or v['FLAG'] == 3:
                t.append(k) 
        if  not len(t):
            print(len(t))
            Helper.show_error(None,"Phải chọn ít nhất 1 SAP")
            sys.exit(1)
        return t   
    
     
    def _create_keyin_list(self) -> list[dict]:
        t:list[dict] = []
        
        for k,v in self.sap_rcv.items():
            if v['FLAG'] == 2 or v["FLAG"] == 3:
                new_dict : dict = {"WD":k,**v,"SLOC":"06RI"} if v['LOC'] == "TBS" else {"WD":k,**v,"SLOC":"03RI"}
                t.append(new_dict)
        if not len(t):
                Helper.show_error(None,"Không thể khởi tạo bảng user keyin !")
                sys.exit(1)
        return t
    
    def _create_path_mapping(self)->dict[str,str]:
        
        mapping : dict[str,str] = {}
        if getpass.getuser() == "fuongsensei":
            self.base_report_file = r"E:\AWASE1HCMICAP01\AppsData\GR Ver Report"
        base_network : str = self.base_report_file
        base_local   : str = self.local_path
        for s in self.verify_list:
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
           tcode:str = "zlgrns1"
           
           @model_validator(mode='after')
           def _initialize_field(self):
                self.entered_date_start = (self.from_date - dt.timedelta(3)).strftime("%m/%d/%Y")
                self.entered_date_end = self.to_date.strftime("%m/%d/%Y")
                self.file_name =  f"EXPORT_GRN16_{self.from_date}"
                self.file_path = rf"C:\Temp\{self.file_name}.xlsx"
                return self



class DailyConfig(BaseModel):
      verify_config :VerifyConfig
      grn_10_numbers_config:GRN10Config
      grn_16_numbers_config:GRN16Config
      
      
class  Profile(BaseModel):
    daily_report_config:DailyConfig



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

      