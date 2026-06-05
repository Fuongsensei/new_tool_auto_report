
from __future__ import annotations
import win32com.client
from abc import ABC,abstractmethod
from helper import Helper

class SapConnector():
        _instance = None
        def __new__(cls,*args,**kwargs):
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            
            return cls._instance
        
        def __init__(self):
            self.engine : any = win32com.client.GetObject("SAPGUI").GetScriptingEngine
            self.main_connection = self.engine.Children(0)
            self.dict_session :dict[str,'SessionSAPProcessing'] = {}
            
        def check_dictionnary_session(self)->None:
                for name,session in self.dict_session.items():
                    Helper.show_error(None,f"[{name}]")
class SessionSAPProcessing(ABC):
        def __init__(self,index:int,name_session:str,sap:'SapConnector'):
            if  isinstance(index,int):
                self.session = sap.main_connection.Children(index)
                sap.dict_session[name_session] = self
            else:
                Helper.show_error(None,"Index phải  là số nguyên dương !")
        @abstractmethod
        def get_data_from_transaction(self):
            pass
            


            
class SapConnectToMB51(SessionSAPProcessing):
        def get_data_from_transaction(self):
            self.session.StartTransaction("MB51")

main_sap = SapConnector()
mb51 = SapConnectToMB51(0,"TruyCapMB51",main_sap)
mb51.get_data_from_transaction()
print(main_sap.check_dictionnary_session())