import xlwings as xw
from utils.helper import Helper
from typing import Any
from polars import DataFrame
import re
class WorkSheetsManager:
      def __init__(self,sheet_name :str,wb:xw.Book):
         self.wb : xw.Book = wb
         self.sheet : xw.Sheet = self.wb.sheets[sheet_name]
         
      def write(self,place:tuple[DataFrame | Any ,str]) -> None:
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
               self.sheet.range(f"{s_p}:{e_p}").clear_contents()
            else:
                Helper.show_error(None,"Sai kiểu dữ liệu truyền vào !")
         except Exception as e :
            Helper.show_error(None,e)
            return False
               
               
      def get_data_range(self,rng:str,get_only_endpoint:bool = False)-> tuple[str,str] | str:
         
         """ Vui lòng truyền str dưới dạng 'start : end' không cần thêm bất kì số hàng nào\n
         Đúng : 'A:N'\n
         Sai  :    'A1:N1'\n
         Nếu chỉ muốn trả về điểm cuối cùng chứa dữ liệu hãy truyền get_only_endpoint = True\n"""
         try:
               point : list[str] = rng.split(":")
               if len(point) > 2:
                  Helper.show_error(None,"Vui lòng truyền đúng định dạng 'start:end' ")
               else:
                     start_p  , end_p = point
                     last_row: int = (self.sheet.range(f"A{self.sheet.cells.last_cell.row}").end("up").row)
                     end_p+=str(last_row)
                     if get_only_endpoint:
                        return end_p
                     return (start_p,end_p)
         except Exception as e:
            Helper.show_error(None,e)
            
            
            
      def delete_row(self, rng_row: tuple[int, int]|tuple[str,str]) -> None:
            try:
               from_row, to_row = rng_row
               t= to_row-from_row
               self.sheet.range(f"{from_row}:{to_row}").delete()
               return 
            except Exception as e:
                  try:
                     result = ":".join(rng_row)
                     point_row : list[int] = re.findall(r"\d+",result)
                     if len(point_row) > 2:
                        Helper.show_error(None,"Vui lòng truyền theo dạng ' start : end ' ")
                        return
                     from_row,to_row = point_row
                     self.sheet.range(f"{from_row}:{to_row}").delete()
                  except Exception as e:
                        Helper.show_error(None,e)

      def range_copy(self,rng:str):
         try:
            self.sheet.range(rng).copy()
         except Exception as e :
               Helper.show_error(None,e)
               
      def close_workbook(self):
         self.wb.close()

class WorkBookManager:
   def __init__(self,path:str,on_screen:bool = True):
      self.wb : xw.Book = xw.Book(path,update_links=False,visible=on_screen)
      

   def get_sheet(self,sheet_name:str) -> WorkSheetsManager:
      
      try:
          return  WorkSheetsManager(sheet_name,self.wb) 
      except Exception as e:
          Helper.show_error(None,"Excel đang bận hoặc tên sheet không đúng !")
          
   def refresh(self) -> None:
      try:
          self.wb.api.RefreshAll()
      except Exception as e:
          Helper.show_error(None,e)
   def close(self)->None:
       self.wb.close()




