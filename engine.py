from __future__ import annotations
from utils.data_utils import DataIngestor
from utils.excel_manager import WorkBookManager ,_WorkSheetsManager
from polars import DataFrame
from core.data_processor import DataProcessBase,DataProcessDailyReport
from utils.config_loader import Profile , create_profile,DailyConfig,VerifyConfig,GRN10Config,GRN16Config
import time
from getpass import getuser
import sys
from core.sap_connector import SapConnector ,GRN10Processor,GRN16Processor
from utils.helper import Helper
sys.excepthook = Helper.show_traceback_exception
        
if __name__ == "__main__":
   sap : SapConnector = SapConnector()
   
   pro5 : Profile = create_profile()
   daily_config :DailyConfig = DailyConfig(**pro5.daily_report_config) 
   
   verify_config :VerifyConfig = VerifyConfig(**daily_config.verify_config)
   grn10_context : GRN10Config = GRN10Config(**daily_config.grn_10_numbers_config) 
   grn16_context : GRN16Config = GRN16Config(**daily_config.grn_16_numbers_config)
   sap : SapConnector = SapConnector()
   tp:str = verify_config.report_daily_path if getuser() == "fuongsensei" else r"C:\Users\3601183\Downloads\Report Scan Verify Shiftly (RCV) (1).xlsm"
   wb :WorkBookManager = WorkBookManager(tp)
   ws_user = wb.get_sheet("User")
  
   ws_grn_10 : _WorkSheetsManager  = wb.get_sheet(grn10_context.sheet_name)
   ws_grn_16 : _WorkSheetsManager  = wb.get_sheet(grn16_context.sheet_name)
   

   grn10_processor:GRN10Processor = GRN10Processor(grn10_context,ws_user,sap.session)
   grn16_processor : GRN16Processor = GRN16Processor(grn16_context,ws_grn_10,sap.session)
   grn10_processor.process()
   ws_export_10 : _WorkSheetsManager = WorkBookManager(grn10_context.file_path).get_sheet("Data")
   time.sleep(3)
   ws_export_10.range_copy(f"A2:{ws_export_10.get_data_range("A:A",True)}")


   grn16_processor.process()
   

   

   
