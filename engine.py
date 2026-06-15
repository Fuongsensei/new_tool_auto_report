from __future__ import annotations
from utils.data_utils import DataIngestor
from utils.excel_manager import WorkBookManager ,WorkSheetsManager
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
   pro5 : Profile = create_profile()
   verify_config:VerifyConfig = pro5.daily_report_config.verify_config
   wb : WorkBookManager = WorkBookManager(verify_config.report_daily_path)
   ws : WorkSheetsManager = wb.get_sheet("User")
   ws.write((verify_config._key,"A4"))
   

   
