from __future__ import annotations
import xlwings 
import time
import yaml
import datetime
from data_utils import DataIngestor
from data_processor import DataProcessBase
from excel_manager import WorkBookManager ,_WorkSheetsManager
import polars as pl
from config_loader import DailyConfig,create_profile,Profile
from data_processor import DataProcessDailyReport
import sys
from helper import Helper
sys.excepthook = Helper.show_traceback_exception
        
if __name__ == "__main__":
    pro5 : Profile = create_profile()
    daily_config :DailyConfig = DailyConfig(**pro5.daily_report_config)
    data_process_daily : DataProcessBase[DailyConfig] = DataProcessDailyReport(daily_config)
    data_ingest : DataIngestor = DataIngestor(data_process_daily.config.path_local_mapping)
    
    
    df : pl.DataFram = data_process_daily.Process(data_ingest.ingest_data())
    ex: WorkBookManager = WorkBookManager(r"C:\Users\3601183\Downloads\Report Scan Verify Shiftly (RCV) (1) (1).xlsm",True)
    ws  = ex.get_sheet("Verify data")
    ws.write((df,"A2"))
    
    
    
    