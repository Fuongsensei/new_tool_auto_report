from core.data_processor import DataProcessForReportDashboardBase
from abc import abstractmethod,ABC



class ConverterDataForReportDashboard
    def __init__(self):
        pass
    
    def convert(self,dct:dict[Any,Any])-> str:
        """Convert dict {K:V,K:V...} to 'K:V'-'K:V'.."""
        
        
        chain :str = ""
        connect:str= ""
        if not dct and not isinstance(dct,dict): return
        for k,v in dct.items():
            form:str = f"{k}:{v}"
            if not chain:
                chain+=form
            else:
                chain+="-"+form 
                
        return chain
        
        
        
        
        