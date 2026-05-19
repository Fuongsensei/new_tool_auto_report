import xlwings 

import time
import yaml
import datetime
from data_utils import DataIngestor
from data_processor import create_profile,DataProcessBase,DailyConfig,Profile
#import excel_manager as excelM
import polars as pl



        
if __name__ == "__main__":
    pro5 : Profile = create_profile()
    daily_config : DailyConfig = DailyConfig(**pro5.daily_report_config)
    data : DataProcessBase[DailyConfig] = DataProcessBase(daily_config)
    data_tranfer = DataIngestor(data.config.path_local_mapping)
    df:pl.DataFrame = data_tranfer.release_data()
    print(df)