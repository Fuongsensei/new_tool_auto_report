import xlwings as xw

import polars as pl


class WorkBookManager:
    def __init__(self,path:str,on_screen:bool):
       self.wb : xw.Book = xw.Book(path,update_links=False,visible=on_screen)
       
       
    def get_sheet(self,sheet_name:str) -> _WorkSheetsManager:
        return  _WorkSheetsManager(sheet_name,self.wb) 
        
    def refresh(self) -> None:
        self.wb.api.RefreshAll()
        
        

class _WorkSheetsManager:
      def __init__(self,sheet_name :str,wb:xw.Book):
         self.wb : xw.Book = wb
         self.sheet : xw.Sheet = self.wb.sheets[sheet_name]
         
      def write(self,place:tuple) -> None:
          data,rng = place
          self.sheet.range("1:100000").delete()
          if isinstance(data,pl.DataFrame):
             self.sheet.range(rng).value = data.values
          else :
               self.sheet.range(rng).value = data
               
      def delete_data(self,rng:str) -> bool:
         try: 
            self.sheet.range(rng).delete() 
         except 
         
      def delete_row(self,rng_row:tuple[int,int]) -> None:
         from_row ,to_row = rng_row
         self.sheet.range(f"{from_row}:{to_row}").delete()
          

path:str = r"C:\Users\3601183\Desktop\HCM Goods Receipt Verification PRD V3.6.9.2 3.xlsm"
 
sheet_4 : WorkSheetsManager =  WorkBookManager(path,True).get_sheet("Sheet4")

sheet_4.delete_row((9,1))




