import xlwings as xw

import polars as pl

class _WorkSheetsManager:
      def __init__(self,sheet_name :str,wb:xw.Book):
         self.wb : xw.Book = wb
         self.sheet : xw.Sheet = self.wb.sheets[sheet_name]
         
      def write(self,place:tuple[any,str]) -> None:
         data,rng = place
         #self.sheet.range("1:100000").delete()
         if isinstance(data,pl.DataFrame):
            self.sheet.range(rng).value = data.to_numpy()
         else :
               self.sheet.range(rng).value = data
               
      def delete_data(self,rng:str) -> bool:
         try: 
            self.sheet.range(rng).delete() 
         except :
            pass
         
      def delete_row(self,rng_row:tuple[int,int]) -> None:
         from_row ,to_row = rng_row
         self.sheet.range(f"{from_row}:{to_row}").delete()


class WorkBookManager:
   def __init__(self,path:str,on_screen:bool):
      self.wb : xw.Book = xw.Book(path,update_links=False,visible=on_screen)


   def get_sheet(self,sheet_name:str) -> _WorkSheetsManager:
      return  _WorkSheetsManager(sheet_name,self.wb) 
   
   def refresh(self) -> None:
      self.wb.api.RefreshAll()










