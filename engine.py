from __future__ import annotations
from utils.data_utils import DataIngestor
from utils.excel_manager import WorkBookManager ,_WorkSheetsManager
from polars import DataFrame
from core.data_processor import DataProcessBase,DataProcessDailyReport
from utils.config_loader import Profile , create_profile,DailyConfig
import time
from getpass import getuser
import sys
from core.sap_connector import SapConnector , GRN10Config,GRN10Processor
from utils.helper import Helper
sys.excepthook = Helper.show_traceback_exception
        
if __name__ == "__main__":
   sap : SapConnector = SapConnector()
   
   pro5 : Profile = create_profile()
   daily_config :DailyConfig = DailyConfig(**pro5.daily_report_config) 
   grn10_context : GRN10Config = GRN10Config(daily_config)
   sap : SapConnector = SapConnector()
   tp:str = daily_config.report_daily_path if getuser() == "fuongsensei" else r"C:\Users\3601183\Downloads\Report Scan Verify Shiftly (RCV) (1).xlsm"
   wb :WorkBookManager = WorkBookManager(tp)

   ws_user :_WorkSheetsManager = wb.get_sheet("User")
   grn10_processor:GRN10Processor = GRN10Processor(grn10_context,ws_user,sap.session)
   grn10_processor.process()
   wb_export_10 : WorkBookManager  = WorkBookManager(grn10_context.file_path)
   print(grn10_context.file_path)
   wb_export_10.close()
   

   
