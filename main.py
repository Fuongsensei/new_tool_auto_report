import xlwings 

import time
import yaml
import datetime
import static_varibles as stv
import file_handler as fh
import data_processor as data_p
import excel_manager as excelM
import polars as pl



        
if __name__ == "__main__":
  data = data_p.DataProcess()
  sheet1 = excelM.WorkSheetsManager(R"C:\Users\3601183\Desktop\scan.xlsx","Sheet1")
  
  data_ingestor = fh.DataIngestor(data.cf.path_map_local)
  df_raw = data_ingestor.release_data()
  df = data.Process(df_raw)
  print(df)
  sheet1.Write((df.unique(subset=[df.columns[0]],maintain_order=True,keep='first').to_numpy(),"A1"))

  
  sheet2 = excelM.WorkSheetsManager(R"C:\Users\3601183\Desktop\scan.xlsx","Sheet2")
  rlst = df.select(pl.nth(5).str.split("|").list.get(0)).to_series().value_counts(sort=True,parallel=True)
  sheet2.Write((rlst.to_numpy(),"A1"))