import polars as pl
from typing  import Generic,TypeVar 
from abc import ABC,abstractmethod
from pydantic import BaseModel,model_validator,field_validator,PrivateAttr
from helper import Helper
import time

from datetime import date,datetime
from config_loader import DailyConfig
T = TypeVar("T",bound=BaseModel)

class DataProcessBase(Generic[T],ABC):
    def __init__(self,config:T):
        self.config :T = config


    @abstractmethod
    def Process(self,data:pl.DataFrame):
        pass

class DataProcessDailyReport(DataProcessBase[DailyConfig]):
        def Process(self, data: pl.DataFrame):
            lf : pl.LazyFrame = data.lazy()
            cols = data.columns
            cf = self.config
            perdicate_filter_date : pl.Expr = pl.col(cols[5]).str.split("|").list.get(1).str.to_datetime(format="%m/%d/%Y %I:%M:%S %p").is_between(
                    cf.from_date.replace(hour=cf.from_hour,minute=cf.from_minute,second=cf.from_second),cf.to_date.replace(hour=cf.to_hour,minute=cf.to_minute,second=cf.to_second)
                )
            perdicate_boolean_col:pl.Expr = pl.all_horizontal(pl.col([cols[i] for i in [9,10,11,13]]) == True)
            return data.filter(perdicate_boolean_col&perdicate_filter_date)
            
            #return lf.filter(perdicate_filter_date).collect()
            
        
        





