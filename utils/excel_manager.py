import xlwings as xw

from utils.helper import Helper

from typing import Any

from polars import DataFrame

import re

import os 
class WorkSheetsManager:

      def __init__(self,sheet_name :str,wb:'WorkBookManager'):

         self.wb : WorkBookManager = wb

         self.sheet : xw.Sheet = self.wb.sheets[sheet_name]

      def write(self,place:tuple[DataFrame | Any ,str]) -> None:

         """Tham số dùng để truyền data và vị trí vào bằng 1 tuple dưới dạng (data, vùng cần ghi)"""

         data,rng = place

         try:

            self.wb.app.screen_updating = False

            self.wb.app.display_alerts = False

            self.wb.app.calculation = 'manual'

            self.wb.app.enable_events = False

            if isinstance(data,DataFrame):

               self.sheet.range(rng).value = data.to_numpy()

               self.wb.save_workbook()

            else :

                  self.sheet.range(rng).value = data

                  self.wb.save_workbook()

         except Exception as e:

               Helper.show_error(None,e)

         finally :

            self.wb.app.screen_updating = True

            self.wb.app.display_alerts = True

            self.wb.app.calculation = 'automatic'

            self.wb.app.enable_events = True

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

         """ Vui lòng truyền str dưới dạng 'start : end' không cần thêm bất kì số hàng nào\nĐúng : 'A:N'\nSai  :    'A1:N1'\nNếu chỉ muốn trả về điểm cuối cùng chứa dữ liệu hãy truyền get_only_endpoint = True\n"""

         try:

               point : list[str] = rng.split(":")

               if len(point) > 2:

                  Helper.show_error(None,"Vui lòng truyền đúng định dạng 'start:end' ")

               else:

                     start_p  , end_p = point

                     last_row: int = (self.sheet.range(f"A{self.sheet.cells.last_cell.row}").end("up").row)

                     end_p+=str(last_row)

                     if get_only_endpoint:

                        return last_row

                     return (start_p,end_p)

         except Exception as e:

            Helper.show_error(None,e)

      def delete_row(self, rng_row: tuple[int, int]) -> None:

            try:

               from_row, to_row = rng_row

               if(to_row <  from_row):return

               self.sheet.range(f"{from_row}:{to_row}").delete()

               return

            except Exception as e:
                     Helper.show_error(None,e)
                  
      def delete_to_last_row(self,start_index:int)->None:
            try:
               
               last_row : int =  self.sheet.range("A" + str(self.sheet.cells.last_cell.row)).end("up").row
               
               if start_index >= last_row : return
               
               self.sheet.range(f"{start_index}:{last_row}").delete()
               
            except Exception as e:
               
               Helper.show_error(None,e)
               
      def range_copy(self,rng:str):

         try:

            self.sheet.range(rng).copy()

         except Exception as e :

               Helper.show_error(None,e)
               

      def format_col(self,fm:str,col_or_range:str|list[str]) -> None:

         if fm == "@" or fm == "dd/mm/yyyy":

               if isinstance(col_or_range,str):

                  self.sheet.range(col_or_range).number_format = fm

               if isinstance(col_or_range,list):

                  for col in col_or_range:

                     self.sheet.range(f"{col}:{col}").number_format = fm
                     
                     
      def  copy_to_last_row(self,rng_to_range:str,index_start:int)->None:
               from_rng ,to_rng = rng_to_range.split(":")
               
               last_row: int = (self.sheet.range(f"A{self.sheet.cells.last_cell.row}").end("up").row)
               
               if index_start >= last_row: return
               
               self.sheet.range(f"{from_rng}{index_start}:{to_rng}{last_row}").copy()
      
      def  close(self)->None:
         self.wb.close()
         
               
class WorkBookManager:
   def __init__(self,path:str,on_screen:bool = True):
      
         self.path :str = path
          
         if not os.path.exists(path):
            
            raise Exception ("Đường dẫn không tồn tại !")
            
         else:
            self.app : xw.App|None = None
   
            self.wb  : xw.Book|None = None
            self.sheets  = None
   
            for app in xw.apps:
   
               for wb in app.books:
   
                  if wb.fullname == path:
   
                     self.app = app
   
                     self.wb  = wb
                     
                     self.sheets = wb.sheets
   
            if  not self.app or not self.wb:
   
                  self.app = xw.App(visible=on_screen,add_book=False)
   
                  self.wb  = self.app.books.open(path)
                  
                  self.sheets = self.wb.sheets


   def get_sheet(self,sheet_name:str) -> WorkSheetsManager:

      try:

            return  WorkSheetsManager(sheet_name,self)

      except Exception as e:

            Helper.show_error(None,"Excel đang bận hoặc tên sheet không đúng !")

   def refresh(self) -> None:

      try:

            self.wb.api.RefreshAll()

      except Exception as e:

            Helper.show_error(None,e)

   def close(self)->None:

         self.wb.close()
         if self.app.books.count < 1:
            self.app.quit()
         
   def create_empty_book(self) ->tuple[xw.App,xw.Book]:
      
         app : xw.App = xw.App(add_book=False,visible=False)
         
         wb  : xw.Book = app.books.add()
         
         wb.save(self.path)
         
         return app,wb
      
   def save_workbook(self)->None:
       self.wb.save()
      