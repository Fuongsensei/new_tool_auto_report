import polars as pl
from typing  import Generic,TypeVar 
from pydantic import BaseModel,model_validator,field_validator,PrivateAttr
from helper import Helper


T = TypeVar("T",bound=BaseModel)

class DataProcessBase(Generic[T]):
    def __init__(self,config:T):
        self.config :T = config



    def Process(self,data:pl.DataFrame):
        pass
    




