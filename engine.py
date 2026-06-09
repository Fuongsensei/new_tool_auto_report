from __future__ import annotations
from utils.data_utils import DataIngestor
from utils.excel_manager import WorkBookManager ,_WorkSheetsManager
from polars import DataFrame
from core.data_processor import DataProcessBase,DataProcessDailyReport
from utils.config_loader import Profile , create_profile,DailyConfig
import time
import sys
from core.sap_connector import SapConnector,SessionMB51,SessionZlGrns1
from utils.helper import Helper
sys.excepthook = Helper.show_traceback_exception
        
if __name__ == "__main__":
   sap : SapConnector = SapConnector()
   
   mb51 = SessionMB51(sap.create_session('MB51'))
   time.sleep(3)
   nzl = SessionZlGrns1(sap.create_session("nzl"))
   time.sleep(3)
   nzl.ProcessingSAP()   
   time.sleep(3)
   mb51.ProcessingSAP()
   print(mb51.session.Id)
   print(nzl.session.Id)

   
