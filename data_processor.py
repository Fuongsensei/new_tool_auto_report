import polars as pl
from typing  import Generic,TypeVar 
from abc import ABC,abstractmethod
from pydantic import BaseModel,model_validator,field_validator,PrivateAttr
from helper import Helper
import time
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
            lf.filter(pl.col(cols[5]).str.split("|").list.get(1).is_between(self.config.from))
            
        
        





