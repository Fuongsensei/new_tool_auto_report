
from __future__ import annotations
import win32com.client
from abc import ABC,abstractmethod
from typing import TypeVar,Generic
from utils.helper import Helper
import time

context_sap =TypeVar("context_sap",bound=GRNConFig)

class SapConnector():
        _instance = None
        def __new__(cls,*args,**kwargs):
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            
            return cls._instance
        
        def __init__(self):
            self.engine : any = win32com.client.GetObject("SAPGUI").GetScriptingEngine
            self.session = self.engine.Children(0).Children(0)
            

class GRNConFig(ABC):
        def __init__(self):
            pass
      

class GRN10Config(GRNConFig):
        def __init__(self):
            pass
        def 
class GRNProcessor(Generic[context_sap]  ,ABC):
        def __init__(self):
           self.context = context_sap
        def process(self):
            pass
      

            
            
        
        
        


                     

class SessionSAPProcessing(ABC):
      def __init__(self,session:any):
            self.session = session
            self.tcode :str|None = None
      @abstractmethod
      def ProcessingSAP()->None:
           pass


