from components.components import CoreComponent,ConfigComponent,UtilsComponent,SapProcessComponent,CombaineComponent
from utils.excel_manager import WorkBookManager ,WorkSheetsManager
import time


class RunSapStep:
        def __init__(self, config:ConfigComponent,sap:SapProcessComponent,writer_cls:type[WorkBookManager] = WorkBookManager):
            
                if not sap : return None
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
            
            self.writer_daily_report.close()
            

            
class ProcessDataStep:
        def __init__(self,core:CoreComponent,uls:UtilsComponent,config:ConfigComponent) -> None:
            
            self.flag_run_sap = config.daily_report_config.run_sap
            
            self.core = core
            
            self.uls  = uls
            
            self.config = config
            
            self.verify_data_process = None 
            
            self.grn10_data_process  = None
            
            self.grn16_data_process  = None
            
            self.out_grn16 = None
            
            
        def run(self)->None:
            
            self.verify_data_process = self.core.data_process_verify.Process(self.uls.verify_data_ingestor.ingest_data())
            
            if self.flag_run_sap:
                    
                    self.grn10_data_process  = self.core.data_process_grn10.Process(self.uls.grn10_data_ingestor.load_data_raw_file(self.config.daily_report_config.grn_10_numbers_config.file_path),self.out_grn16,self.config.daily_report_config.delete_old_day)
                    
                    self.out_grn16 = self.grn10_data_process[1]
                    
                    self.grn16_data_process  = self.core.data_process_grn16.Process(self.uls.grn16_data_ingestor.load_data_raw_file(self.config.daily_report_config.grn_16_numbers_config.file_path),self.out_grn16,self.config.daily_report_config.delete_old_day)
            
            
class WriteExcelStep:
    def __init__(self,process_step:ProcessDataStep,writer_cls:type[WorkBookManager] = WorkBookManager,config:ConfigComponent=ConfigComponent):
        
        
            self.flag_run_sap = config.daily_report_config.run_sap
            
            self.process_step = process_step
            
            self.writer_cls = writer_cls 
            
            self.veriy_data_processed = None
            
            self.config_verify = config.daily_report_config.verify_config
            
            self.config_grn10  = None
            
            self.config_grn16  = None
            
            self.writer_sheet_grn_10  = None
            
            self.writer_sheet_grn_16  = None
            
            
            
            
            
            if self.flag_run_sap:  
        
                    self.config_grn10  = config.daily_report_config.grn_10_numbers_config
                    
                    self.config_grn16  = config.daily_report_config.grn_16_numbers_config
                    
                    self.grn10_data_processed = None
                    
                    self.grn16_data_processed = None
                    
        
        
                    
    def write(self)->None:
            
            self.writer_sheet_verify.delete_to_last_row(2)

            self.writer_sheet_verify.write((self.veriy_data_processed,"A2"))
            
            if self.flag_run_sap:
                
                    self.writer_sheet_grn_10.delete_to_last_row(2)
    
                    self.writer_sheet_grn_16.delete_to_last_row(2)
                
    
                    self.writer_sheet_grn_10.write((self.grn10_data_processed,"A2"))
    
                    self.writer_sheet_grn_16.write((self.grn16_data_processed,"A2"))
            
            
            self.writer_daily_report.close()
            
            
    def reopen_excel(self)-> None:
        
        _ = self.writer_cls(self.config_verify.report_daily_path,True)
        _.refresh()
        _.save_workbook()
        
    
    def run(self)-> None:
        
        self.process_step.run()
        
        self.veriy_data_processed = self.process_step.verify_data_process 

        self.writer_daily_report =  self.writer_cls(self.config_verify.report_daily_path,False)

        self.writer_sheet_verify  = self.writer_daily_report.get_sheet(self.config_verify.sheet_name)  


        if self.flag_run_sap:
        
            self.writer_sheet_grn_10  = self.writer_daily_report.get_sheet(self.config_grn10.sheet_name)   
                        
            self.writer_sheet_grn_16  = self.writer_daily_report.get_sheet(self.config_grn16.sheet_name)
    
            self.grn10_data_processed = self.process_step.grn10_data_process[0]
            
            self.grn16_data_processed = self.process_step.grn16_data_process
            
            
        self.write()
        
        self.reopen_excel()

            

class CombaineStepMachine:
    def  __init__(self,combaine_component_machine:type[CombaineComponent]=CombaineComponent):
        
        self.component : CombaineComponent = combaine_component_machine()
        
        self.component.combaine()
        
        self.run_sap = None
        
        self.process_data = None
        
        self.writer_excel = None

    def combaine(self)-> None:
        if self.component.config.daily_report_config.run_sap:
                self.run_sap = RunSapStep(self.component.config,self.component.sap,WorkBookManager)
        
        self.process_data = ProcessDataStep(self.component.core,self.component.uls,self.component.config)
        
        self.writer_excel = WriteExcelStep(self.process_data,WorkBookManager,self.component.config)          
        

        
    