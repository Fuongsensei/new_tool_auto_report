from __future__ import annotations
from utils.data_utils import DataIngestor
from utils.excel_manager import WorkBookManager ,_WorkSheetsManager
from polars import DataFrame
from core.data_processor import DataProcessBase,DataProcessDailyReport
from utils.config_loader import Profile , create_profile,DailyConfig
import sys
from utils.helper import Helper
sys.excepthook = Helper.show_traceback_exception
        
if __name__ == "__main__":
    pro5 : Profile = create_profile()
    daily_config :DailyConfig = DailyConfig(**pro5.daily_report_config)
    data_ingest :DataIngestor = DataIngestor(daily_config.path_local_mapping)
    data_pc : DataProcessBase[DailyConfig] = DataProcessDailyReport(daily_config)
    df :DataFrame = data_pc.Process(data_ingest.ingest_data())
    wb :WorkBookManager = WorkBookManager(daily_config.report_daily_path)
    ws = wb.get_sheet("Verify data")
    print(ws.get_data_range("A:N",True))
    
    