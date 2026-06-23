import sys

import os 

import time 

from step.stage import CombaineStepMachine,CombaineComponent

from communication.ipc import CommunicationToCSharp

class DailyReportExportMachine:
     def __init__(self,combaine_step_machine_cls:type[CombaineStepMachine]=CombaineStepMachine,combaine_component_cls:type[CombaineComponent]=CombaineComponent):
        
        self.combaine_step_machine : CombaineStepMachine  = combaine_step_machine_cls(combaine_component_cls)
        self.combaine_step_machine.combaine()
        
        
     def run(self)->None:
        
         if  self.combaine_step_machine.run_sap:
            
             self.combaine_step_machine.run_sap.run()
         
         self.combaine_step_machine.writer_excel.run()
         
         
if __name__ == "__main__":
         
         app : DailyReportExportMachine = DailyReportExportMachine(CombaineStepMachine,CombaineComponent)
         app.run()
         
 