import xlwings 

import time
import yaml
import datetime
from data_utils import DataIngestor
from data_processor import DataProcessBase
#import excel_manager as excelM
import polars as pl
from config_loader import DailyConfig,create_profile,Profile


        
if __name__ == "__main__":
    pro5 : Profile = create_profile()
    daily_config :DailyConfig = DailyConfig(**pro5.daily_report_config)
    data_ingest : DataIngestor = DataIngestor(daily_config.path_local_mapping)
    print(data_ingest.local_csv_paths)