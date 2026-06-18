from __future__ import annotations
from utils.data_utils import DataIngestor
from utils.excel_manager import WorkBookManager ,WorkSheetsManager
from polars import DataFrame
import polars as pl
from core.data_processor import DataProcessBase,DataProcessVerify,DataProcessGrn10Number
from utils.config_loader import Profile , create_profile,DailyConfig,VerifyConfig,GRN10Config,GRN16Config
import time
from getpass import getuser
import sys
from core.sap_connector import SapConnector ,GRN10Processor,GRN16Processor
from utils.helper import Helper
sys.excepthook = Helper.show_traceback_exception
        
if __name__ == "__main__":
   pro5 : Profile = create_profile()
   
   sap  : SapConnector  = SapConnector()
   
   session = sap.session
   
   verify_config:VerifyConfig = pro5.daily_report_config.verify_config
   
   grn10_config :GRN10Config = pro5.daily_report_config.grn_10_numbers_config
   
   grn16_config : GRN16Config =  pro5.daily_report_config.grn_16_numbers_config
   
   wb : WorkBookManager = WorkBookManager(verify_config.report_daily_path)
   
   ws_user : WorkSheetsManager = wb.get_sheet("User")
   
   ws_veify: WorkSheetsManager = wb.get_sheet(verify_config.sheet_name)
   
   ws_grn_10_number : WorkSheetsManager = wb.get_sheet(grn10_config.sheet_name)
   
   ws_grn_16_number : WorkSheetsManager = wb.get_sheet(grn16_config.sheet_name)
   
   grn10_process :GRN10Processor = GRN10Processor(grn10_config,ws_grn_10_number,session)
   
   grn16_process :GRN16Processor = GRN16Processor(grn16_config,ws_grn_16_number,session)
   
   ws_user.delete_row(("A4",ws_user.get_data_range("A:A",True)))
   ws_user.write((verify_config._keyin_list ,"A4"))
   
   ws_user.range_copy(f"A3:{ws_user.get_data_range("A2:A100",True)}")
   
   grn10_process.process()
   time.sleep(3)
   data_grn_10 : WorkSheetsManager = WorkBookManager(grn10_config.file_path).get_sheet("Data")
   
   data_grn_10.range_copy(f"A2:{data_grn_10.get_data_range("A:A",True)}")   
   
   grn16_process.process()
   time.sleep(3)
   data_grn_16 :WorkSheetsManager = WorkBookManager(grn16_config.file_path).get_sheet("Data")
   
   
   df_verify : DataFrame = DataProcessVerify(verify_config,DataIngestor(verify_config.path_local_mapping).ingest_data()).Process()
   
   data_grn_10_ingest :DataFrame = DataProcessGrn10Number(grn10_config,DataIngestor(None,True).load_data_raw_file(grn10_config.file_path)).Process();
   
   ws_grn_10_number.write((data_grn_10_ingest,"A2"))
   ws_veify.write((df_verify,"A2"))
  

   
