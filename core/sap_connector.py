
from __future__ import annotations
import win32com.client
from abc import ABC,abstractmethod
from utils.helper import Helper

class SapConnector():
        _instance = None
        def __new__(cls,*args,**kwargs):
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            
            return cls._instance
        
        def __init__(self):
            self.engine : any = win32com.client.GetObject("SAPGUI").GetScriptingEngine
            self.main_connection = self.engine.Children(0)
            self.main_session = self.main_connection.Children(0)
            self.count_session = self.main_connection.Children.Count
            self.dict_session :dict[str,any] = {"main" : self.main_session}
            
            
        def check_dictionnary_session(self)->None:
                for name,session in self.dict_session.items():
                    Helper.show_error(None,f"[{name}]")

        def create_session(self,name_session:str)->any:
            if not name_session:
               return False
            self.main_session.CreateSession()
            after  = self.main_connection.Children.Count
            session = self.main_connection.Children(after-1)
            self.dict_session[name_session] = session
            return session
        
        def close_session(self,name_session:str)->bool:
            if not name_session:return False
            try:
                session = self.dict_session[name_session]
                session.CloseSession()
                return True
            except Exception as e:
                 print(e)
                 return False

        def clean_all_session(self)->None:
            for _,s in self.dict_session.items():
                s.CloseSession()
            return
        
    

                     

class SessionSAPProcessing(ABC):
      def __init__(self,session:any):
            self.session = session
            self.tcode :str|None = None
      @abstractmethod
      def ProcessingSAP()->None:
           pass

class SessionMB51(SessionSAPProcessing):
      def ProcessingSAP(self):
           self.tcode = "MB51"
           self.session.StartTransaction(self.tcode)
           print(f"Truy cap thanh cong  {self.tcode}")

class SessionZlGrns1(SessionSAPProcessing):
      def ProcessingSAP(self):
           self.tcode ="zlgrns1"
           self.session.StartTransaction(self.tcode)
           print(f"truy cap thanh cong {self.tcode}")

