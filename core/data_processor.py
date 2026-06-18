import polars as pl
from typing  import Generic,TypeVar 
from abc import ABC,abstractmethod
from pydantic import BaseModel,model_validator,field_validator,PrivateAttr
from utils.helper import Helper
import time

from datetime import date,datetime
from utils.config_loader import VerifyConfig,GRN10Config,GRN16Config
T = TypeVar("T",bound=BaseModel)

class DataProcessBase(Generic[T],ABC):
    def __init__(self,config:T,data_frame_raw:pl.DataFrame):
        self.config :T = config
        self.data : pl.DataFrame = data_frame_raw


    @abstractmethod
    def Process(self,data_raw:pl.DataFrame):
        pass

class DataProcessVerify(DataProcessBase[VerifyConfig]):
        def Process(self):
            """Nhận một raw dataFrame và trả về dataFrame sau khi đã xử lý"""
            try:
                data_raw : pl.DataFrame = self.data
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


class DataProcessGrn10Number(DataProcessBase[GRN10Config]):
        def Process(self):
            drop_col : list[str]  = [self.data.columns[i] for i in self.config.drop_columns]
            self.data = self.data.drop(drop_col)
            self.data = self.data.with_columns(pl.lit("=VLOOKUP(@CN:CN,'Vendor Subcontrac'!A:B,2,0)").alias("Network"))
            self.data = self.data.filter(pl.col(2) == pl.col(2).max().item())
            return self.data

class DataProessGrn16Number(DataProcessBase[GRN16Config]):
        



