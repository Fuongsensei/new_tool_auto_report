import mmap
import win32event
import struct

class CommunicationToCSharp:
    def __init__(self):         
        
        self.SRM_NAME : str   = r"Local\python_connect_to_CSharp"        
        
        self.REQ_NAME : str   = r"Local\request_to_python"        
        
        self.RES_NAME : str   = r"Local\respone_to_Csharp"        
        
        self.MUTEX_NAME : str = r"Local\Mutex_connect"        
        
        self.BUF_SIZE  : int = 4096        
        
        self.shared_memo : mmap.mmap = mmap.mmap(-1,self.BUF_SIZE,tagname=self.SRM_NAME)        
        
        self.req_event :int = win32event.CreateEvent(None,0,0,self.REQ_NAME)        
        
        self.res_event :int = win32event.CreateEvent(None,0,0,self.RES_NAME)        
        
        self.muxtext_locker : int = win32event.CreateMutex(None,0,self.MUTEX_NAME)      
        
    def read_memo(self) -> str:
            
            win32event.WaitForSingleObject(self.muxtext_locker,win32event.INFINITE)
            
            self.shared_memo.seek(0)
            
            length : int =  struct.unpack("<I",self.shared_memo.read(4))[0]
            
            self.shared_memo.seek(4)
            
            data : bytes  =  self.shared_memo.read(length)
            
            win32event.ReleaseMutex(self.muxtext_locker)
            
            return data.decode()      
        
    def waiting_request_event(self) -> None:
        win32event.WaitForSingleObject(self.req_event,win32event.INFINITE)
