import xlwings as xw
from helper import Helper
from polars import DataFrame
import re
class _WorkSheetsManager:
      def __init__(self,sheet_name :str,wb:xw.Book):
         self.wb : xw.Book = wb
         self.sheet : xw.Sheet = self.wb.sheets[sheet_name]
         
      def write(self,place:tuple[any,str]) -> None:
         """Tham số thứ 2 dùng để truyền data và vị trí vào bằng 1 tuple dưới dạng (data , vùng cần ghi)"""
         data,rng = place
         try:   
            if isinstance(data,DataFrame):
               
               self.sheet.range(rng).value = data.to_numpy()
            else :
                  self.sheet.range(rng).value = data
         except Exception as e:
               Helper.show_error(None,e)
               
               
      def delete_data(self,rng:str) -> bool:
               try:
                  self.sheet.range(rng).delete()
                  return True
               except Exception as e :
                  Helper.show_error(None,e)
                  return False
               
               
      def get_data_range(self,rng:str,header:bool = True)
         try:
               point : list[str] = re.findall("[a-zA-z]")
               if len(point) > 2:
                  Helper.show_error(None,"Vui lòng truyền đúng định dạng 'start:end' ")
               else:
                     start_p  , end_p = point
                     last_row:int = self.sheet. 
         
      def delete_row(self,rng_row:tuple[int,int]) -> None:
         """Tham số nhận vào 1 tuple chứa nơi bắt đầu và nơi kết thúc cần xóa  bắt buộc phải là giá trị int"""
         try:
            from_row ,to_row = rng_row
            t = from_row - to_row
            self.sheet.range(f"{from_row}:{to_row}").delete()
         except Exception as e:
            Helper.show_error(None,e)
      
class WorkBookManager:
   def __init__(self,path:str,on_screen:bool):
      self.wb : xw.Book = xw.Book(path,update_links=False,visible=on_screen)


   def get_sheet(self,sheet_name:str) -> _WorkSheetsManager:
      return  _WorkSheetsManager(sheet_name,self.wb) 
   
   def refresh(self) -> None:
      self.wb.api.RefreshAll()



ws = WorkBookManager(rf"C:\Users\3601183\Downloads\Report Scan Verify Shiftly (RCV) (1) (1).xlsm",True).get_sheet("Sheet4")

ws.delete_row(("1","2"))







