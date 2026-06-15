import polars as pl
from typing  import Generic,TypeVar 
from abc import ABC,abstractmethod
from pydantic import BaseModel,model_validator,field_validator,PrivateAttr
from utils.helper import Helper
import time

from datetime import date,datetime
from utils.config_loader import VerifyConfig
T = TypeVar("T")

class DataProcessBase(Generic[T],ABC):
    def __init__(self,config:T):
        self.config :T = config


    @abstractmethod
    def Process(self,data_raw:pl.DataFrame):
        pass

class DataProcessDailyReport(DataProcessBase[VerifyConfig]):
        def Process(self, data_raw: pl.DataFrame):
            """Nhận một raw dataFrame và trả về dataFrame sau khi đã xử lý"""
            try:
                
                lf : pl.LazyFrame = data_raw.lazy()
                cols = data_raw.columns
                boolean_cols : list[str] = [cols[i] for i in [9,10,11,13]]
                cf = self.config
                perdicate_filter_date : pl.Expr = pl.col(cols[5]).str.split("|").list.get(1).str.    to_datetime(format="%m/%d/%Y %I:%M:%S %p").is_between(
                       datetime.combine(cf.from_date,cf.from_time) ,datetime.combine(cf.to_date,cf.to_time))
                    
                
                perdicate_filter_boolean_cols : pl.Expr = pl.all_horizontal(pl.col(boolean_cols)    ==True)
                
                return lf.filter(perdicate_filter_date & perdicate_filter_boolean_cols).collect().    unique(subset=cols[0],keep="first").sort(cols[0],descending=False)
            
            except Exception as e :
                Helper.show_error(None,e)
        
        





