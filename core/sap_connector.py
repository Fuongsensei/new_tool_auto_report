
from __future__ import annotations
import win32com.client
from abc import ABC,abstractmethod
from typing import TypeVar,Generic
from  utils.helper import Helper
from pydantic import BaseModel
from utils.config_loader import DailyConfig
from utils.excel_manager import WorkBookManager,_WorkSheetsManager
import time
from datetime import timedelta
from datetime import date,datetime

class SapConnector():
        _instance = None
        def __new__(cls,*args,**kwargs):
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            
            return cls._instance
        
        def __init__(self):
            self.engine : any = win32com.client.GetObject("SAPGUI").GetScriptingEngine
            self.session = self.engine.Children(0).Children(0)
            

class GRNConFig(ABC):
        def __init__(self):
            pass
      
context_sap =TypeVar("context_sap",bound=GRNConFig)


class GRN10Config(GRNConFig):
        def __init__(self,config :DailyConfig):
            self.config :DailyConfig = config
            self.year :str  = str(config.from_date.year)
            self.posting_date_start:str = self.config.from_date.date().strftime("%m/%d/%Y")
            self.posting_date_end :str  = self.config.to_date.date().strftime("%m/%d/%Y")
            self.entered_date_start :str = (self.config.from_date.date()-timedelta(3)).strftime("%m/%d/%Y")
            self.entered_date_end:str = self.posting_date_end
            self.file_name = f"EXPORT_GRN10_{self.posting_date_start}"
            self.file_path = rf"C:\TEMP\{self.file_name}.xlsx"
            self.tcode = "z_invmvmts"
            
class GRNProcessor(Generic[context_sap],ABC):
        def __init__(self,context:context_sap,write_helper:_WorkSheetsManager,session:any):
           self.context: context_sap = context
           self.writer = write_helper
           self.session = session
        def process(self):
            pass



class GRN10Processor(GRNProcessor[GRN10Config]):
        def process(self):
           self.writer.range_copy(f"A3:{self.writer.get_data_range("A:A",True)}")
           self.session.StartTransaction(self.context.tcode.upper())
           self.session.findById("wnd[0]/usr/ctxtSO_WERKS-LOW").Text = "VN01"
           self.session.findById("wnd[0]/usr/ctxtSO_BUDAT-LOW").Text = f"{self.context.posting_date_start}"
           self.session.findById("wnd[0]/usr/ctxtSO_BUDAT-HIGH").Text = f"{self.context.posting_date_end}"
           self.session.findById("wnd[0]/usr/btn%_SO_MJAHR_%_APP_%-VALU_PUSH").press()
           self.session.findById("wnd[1]/usr/tabsTAB_STRIP/tabpSIVA/ssubSCREEN_HEADER:SAPLALDB:3010/tblSAPLALDBSINGLE/txtRSCSEL_255-SLOW_I[1,0]").Text = self.context.year
           self.session.findById("wnd[1]/usr/tabsTAB_STRIP/tabpSIVA/ssubSCREEN_HEADER:SAPLALDB:3010/tblSAPLALDBSINGLE/txtRSCSEL_255-SLOW_I[1,1]").Text = self.context.year
           self.session.findById("wnd[1]/tbar[0]/btn[8]").press()
           self.session.findById("wnd[0]/usr/ctxtSO_CPUDT-LOW").Text = self.context.entered_date_start
           self.session.findById("wnd[0]/usr/ctxtSO_CPUDT-HIGH").Text = self.context.entered_date_end
           self.session.findById("wnd[0]/usr/ctxtSO_BWART-LOW").Text = "101"
           self.session.findById("wnd[0]/usr/ctxtSO_BWART-HIGH").Text = "102"
           self.session.findById("wnd[0]/usr/btn%_SO_UNAME_%_APP_%-VALU_PUSH").press()
           self.session.findById("wnd[1]/tbar[0]/btn[24]").press()
           self.session.findById("wnd[1]/tbar[0]/btn[8]").press()
           self.session.findById("wnd[0]/usr/ctxtP_LAY01").Text = "/QUANTITY"
           self.session.findById("wnd[0]/tbar[1]/btn[8]").press()
           self.session.findById("wnd[0]/usr/cntlGRID1/shellcont/shell").selectedRows = "0"
           self.session.findById("wnd[0]/usr/cntlGRID1/shellcont/shell").contextMenu()
           self.session.findById("wnd[0]/usr/cntlGRID1/shellcont/shell").selectContextMenuItem("&XXL")
           self.session.findById("wnd[1]/usr/ssubSUB_CONFIGURATION:SAPLSALV_GUI_CUL_EXPORT_AS:0512/txtGS_EXPORT-FILE_NAME").Text = self.context.file_name
           self.session.findById("wnd[1]/tbar[0]/btn[20]").press()
           self.session.findById("wnd[1]/tbar[0]/btn[11]").press()
           





