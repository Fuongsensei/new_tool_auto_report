import xlwings as xw
from helper import Helper
from polars import DataFrame
import re
class _WorkSheetsManager:
      def __init__(self,sheet_name :str,wb:xw.Book):
         self.wb : xw.Book = wb
         self.sheet : xw.Sheet = self.wb.sheets[sheet_name]
         
      def write(self,place:tuple[any,str]) -> None:
         """Tham số  dùng để truyền data và vị trí vào bằng 1 tuple dưới dạng (data , vùng cần ghi)"""
         data,rng = place
         try:   
            if isinstance(data,DataFrame):
               
               self.sheet.range(rng).value = data.to_numpy()
            else :
                  self.sheet.range(rng).value = data
         except Exception as e:
               Helper.show_error(None,e)
               
               
      def delete_data(self,rng:str|tuple[str,str]) -> bool:
         """Vui lòng truyền str dưới dạng 'start:end' """
         try:
            if isinstance(rng,str):
               self.sheet.range(rng).clear_contents()
               return True
            if isinstance(rng,tuple):
               s_p,e_p = rng
               Helper.show_error(None,f"[{s_p}]  [{e_p}]")
               self.sheet.range(f"{s_p}:{e_p}").clear_contents()
               
         except Exception as e :
            Helper.show_error(None,e)
            return False
               
               
      def get_data_range(self,rng:str,header:bool = True)-> tuple[str,str] :
         try:
               point : list[str] = re.findall("[a-zA-z]",rng)
               if len(point) > 2:
                  Helper.show_error(None,"Vui lòng truyền đúng định dạng 'start:end' ")
               else:
                     start_p  , end_p = point
                     if header:
                        start_p+="2"
                     last_row: int = (self.sheet.range(f"A{self.sheet.cells.last_cell.row}").end("up").row)

                     return (start_p,f"{end_p}{last_row}")
         except Exception as e:
            Helper.show_error(None,e)
            
            
            
      def delete_row(self, rng_row: tuple[int, int]) -> None:
            try:
               from_row, to_row = rng_row
               t= to_row-from_row
               self.sheet.range(f"{from_row}:{to_row}").delete()
            
            except Exception as e:
                  Helper.show_error(e)

      
class WorkBookManager:
   def __init__(self,path:str,on_screen:bool):
      self.wb : xw.Book = xw.Book(path,update_links=False,visible=on_screen)


   def get_sheet(self,sheet_name:str) -> _WorkSheetsManager:
      return  _WorkSheetsManager(sheet_name,self.wb) 
   
   def refresh(self) -> None:
      self.wb.api.RefreshAll()







