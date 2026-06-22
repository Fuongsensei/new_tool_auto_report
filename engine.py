import sys
import os 
from utils.config_loader import  create_profile,Profile
from components.components import UtilsComponent,SapProcessComponent,CoreComponent,ConfigComponent
import time 

from step.stage import RunSapStep
from utils.excel_manager import WorkBookManager,WorkSheetsManager
from utils.helper import Helper 
import traceback
from communication.ipc import CommunicationToCSharp

config :ConfigComponent = ConfigComponent()
sap : SapProcessComponent = SapProcessComponent(config)

run_sap_step : RunSapStep = RunSapStep(config,sap,WorkBookManager) 

run_sap_step.run()