import xlwings as xw

import polars as pl

class WorkSheetsManager:
      def __init__(self,path:str,sheet_name :str):
         self.path:str = path
         self.wb : xw.Book = xw.Book(path)
         self.sheet : self.wb.sheets = self.wb.sheets[sheet_name]
         
      def Write(self,place:tuple):
          data,rng = place
          if isinstance(data,pl.DataFrame):
             self.sheet.range(rng).value = data.values
          else :
               self.sheet.range(rng).value = data
               
          
wbm = WorkSheetsManager(r"C:\Users\3601183\Desktop\Book1.xlsx","Sheet3")
df = pd.read_excel(wbm.path,"Sheet2")
print(df)
place : tuple = (df,"A2:B2")
wbm.Write(place)
