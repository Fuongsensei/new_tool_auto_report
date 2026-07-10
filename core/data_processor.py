import polars as pl
from typing import Generic, TypeVar
from abc import ABC, abstractmethod
from pydantic import BaseModel, model_validator, field_validator, PrivateAttr
import time
from datetime import date, datetime
from utils.config_loader import VerifyConfig, GRN10Config, GRN16Config

T = TypeVar("T")


class DataProcessBase(Generic[T], ABC):
    def __init__(self, config: T|None):
        self.config: T = config


    @abstractmethod
    def Process(self, data_raw: pl.DataFrame) -> pl.DataFrame|None:
        pass
    
    def check_valid(self,data_raw:pl.DataFrame) -> bool:
        if data_raw is None or data_raw.is_empty():return False
        return True

class DataProcessForReportDashboardBase:
    def __init__(self,data_processed:pl.DataFrame):
           self.data = data_processed
      

    def get_record(self) -> tuple|None:
        if self.data is None or self.data.is_empty():return None
        return  self.get_record_after_validate()

    @abstractmethod 
    def get_record_after_validate(self)->tuple:
        pass


class DataProcessVerify(DataProcessBase[VerifyConfig]):
    
    def Process(self, data_raw: pl.DataFrame) -> pl.DataFrame | None:
        if not super().check_valid(data_raw):return None
        """Nhận một raw dataFrame và trả về dataFrame sau khi đã xử lý"""
        try:
            lf: pl.LazyFrame = data_raw.lazy()
            cols = data_raw.columns
            boolean_cols: list[str] = [cols[i] for i in [9, 10, 11, 13]]
            cf = self.config
            if not cf:
                raise Exception("Xử lý data verify cấu hình không được None")

            perdicate_filter_date: pl.Expr = (
                pl.col(cols[5])
                .str.split("|")
                .list.get(1)
                .str.to_datetime(format="%m/%d/%Y %I:%M:%S %p")
                .is_between(
                    datetime.combine(cf.from_date, cf.from_time),
                    datetime.combine(cf.to_date, cf.to_time),
                )
            )

            perdicate_filter_boolean_cols: pl.Expr = pl.all_horizontal(
                pl.col(boolean_cols) == True
            )

            return (
                lf.filter(perdicate_filter_date & perdicate_filter_boolean_cols)
                .collect()
                .unique(subset=cols[0], keep="first")
                .sort(cols[0], descending=False)
            )

        except Exception as e:
            raise RuntimeError("Xử lý Verify data thất bại") from e


class DataProcessGrn10Number(DataProcessBase[GRN10Config]):

    def Process(self, data_raw: pl.DataFrame, out_for_grn_16: pl.DataFrame, delete_old_day: bool) -> tuple[pl.DataFrame, pl.DataFrame|None]:
        if not super().check_valid(data_raw):return None
        if not self.config:
                raise Exception("Xử lý data verify cấu hình không được None")
            
        drop_col: list[str] = [data_raw.columns[i] for i in self.config.drop_columns]
        lz_df: pl.LazyFrame = data_raw.lazy()
        lz_df = (
            lz_df
            .drop(drop_col)
            .with_columns(
                pl.lit("=VLOOKUP(@CN:CN,'Vendor Subcontrac'!A:B,2,0)").alias("Network")
            )
        )
        
        if not delete_old_day:
            return lz_df.collect(),None

        lz_df = lz_df.filter(pl.col(lz_df.columns[2]) == pl.col(lz_df.columns[2]).max())
        out_for_grn_16 = lz_df.select(pl.col(lz_df.columns[0])).collect()
        return lz_df.collect(), out_for_grn_16


class DataProcessGrn16Number(DataProcessBase[GRN16Config]):
    
    def Process(self, data_raw: pl.DataFrame, grn_data: pl.DataFrame, delete_old_day: bool) -> pl.DataFrame|None:
        if not super().check_valid(data_raw):return None
        if not self.config:
                raise Exception("Xử lý data verify cấu hình không được None")
        drop_col: list[str] = [data_raw.columns[i] for i in self.config.drop_columns]
        check_na_col = data_raw.columns[5]

        lz_df: pl.LazyFrame = data_raw.lazy()
        lz_df = lz_df.drop(drop_col)

        if not delete_old_day:
            return lz_df.collect()
        
        grn_data = grn_data.to_series(0)
        
        return lz_df.filter(pl.col(check_na_col).str.slice(0, 10).is_in(grn_data)).collect()
    
    
class DataVerifyProcessForReportDashboard(DataProcessForReportDashboardBase):
        
        def __init__(self,data_processed:pl.DataFrame):
            super().__init__(data_processed)
            self.record : tuple = self.get_record()
            self.total_labels : int 

            self.total_foreach_verify_sap: dict[int,int] 

        
            
        def _get_total_labels(self)-> int:
            return self.data.height
            
                    
        def _get_total_foreach_verify_sap(self) -> dict[int,int]:
            return dict(self.data.with_columns(
                pl.col("User/Time").
                str.split("|").
                list.get(0).
                str.strip_chars().
                cast(pl.Int64,strict=True).
                alias("User")).
                        group_by("User").
                        len("Total").
                        iter_rows())
        


        def get_record_after_validate(self) -> tuple:
            return(self._get_total_labels(),self._get_total_foreach_verify_sap())

class DataGrn10ProcessForReportDashboard(DataProcessForReportDashboardBase):
      def __init__(self, data_processed):
           super().__init__(data_processed)
           self.record = self.get_record()
           
           self.total_receipt :int = self.record[0]
           
           self.total_receipt_foreach_keyin_sap:dict[int,int] = self.record[1]
 
      
            
      def _get_total_receipt(self)-> int:
            return self.data.height
            
                    
      def _get_total_foreach_keyin_sap(self) -> dict[int,int]:
            return dict(self.data.with_columns(
                pl.col("User").
                alias("User")).
                        group_by("User").
                        len("Total").
                        iter_rows())



      def get_record_after_validate(self) ->tuple:
          return(self._get_total_receipt(),self._get_total_foreach_keyin_sap())
           

           