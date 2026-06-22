from components.components import CoreComponent,ConfigComponent,UtilsComponent,SapProcessComponent
from core.sap_connector import GRN16Processor,GRN10Processor
from utils.excel_manager import WorkBookManager ,WorkSheetsManager
import time


class RunSapStep:
        def __init__(self, config:ConfigComponent,sap:SapProcessComponent,writer_cls:type[WorkBookManager] = WorkBookManager):
            
                self.writer_cls = writer_cls
                
                self.session = sap.session

                self.grn10_processor = sap.sap_grn10

                self.grn16_processor = sap.sap_grn16

                self.config  = config 

                self.path_report : str = self.config.daily_report_config.verify_config.report_daily_path
                
                self.writer_daily_report =  self.writer_cls(self.path_report,False)
                
                self.writer_sheet_user = self.writer_daily_report.get_sheet("User")
                
                self.writer_sheet_verify  = self.writer_daily_report.get_sheet(self.config.daily_report_config.verify_config.sheet_name)
                
                
                self.writer_sheet_grn_10  = self.writer_daily_report.get_sheet(self.config.daily_report_config.grn_10_numbers_config.sheet_name)
                
                
                
                self.writer_sheet_grn_16  = self.writer_daily_report.get_sheet(self.config.daily_report_config.grn_16_numbers_config.sheet_name)
                

            
        
            
        def copy_user_sheet(self)-> None:
            self.writer_sheet_user.copy_to_last_row("A:A",3)
            
                
        def run(self)-> None:
            
            self.writer_sheet_user.delete_to_last_row(5)
            
            self.writer_sheet_user.write((self.config.daily_report_config.verify_config._keyin_list,"A4"))
            
            self.copy_user_sheet()
            
            self.grn10_processor.process()
            
            time.sleep(3)
            
            
            self.writer_grn10_data = self.writer_cls(self.config.daily_report_config.grn_10_numbers_config.file_path).get_sheet("Data")
            
            self.writer_grn10_data.copy_to_last_row("A:A",2)
            
            self.grn16_processor.process()
            
            time.sleep(3)
            
            
            self.writer_grn16_data = self.writer_cls(self.config.daily_report_config.grn_16_numbers_config.file_path).get_sheet("Data")
            
            
            self.writer_grn10_data.close()
            
            
            self.writer_grn16_data.close()
            

class ProcessDataStep:
        def __init__(self,core:CoreComponent,uls:UtilsComponent,config:ConfigComponent) -> None:
            
            self.core = core
            
            self.uls  = uls
            
            self.config = config
            
            self.verify_data_process = None 
            
            self.grn10_data_process  = None
            
            self.grn16_data_process  = None
            
            
            
        def run(self)->None:
            self.verify_data_process = self.core.data_process_verify.Process(self.uls.verify_data_ingestor.ingest_data())
            
            self.grn10_data_process  = self.core.data_process_grn10.Process(self.uls.grn10_data_ingestor.load_data_raw_file(self.config.daily_report_config.grn_10_numbers_config.file_path))
            
            self.grn16_data_process  = self.core.data_process_grn16.Process(self.uls.grn16_data_ingestor.load_data_raw_file(self.config.daily_report_config.grn_16_numbers_config.file_path))