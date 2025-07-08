from pydantic import BaseModel , Field
from typing import List  
class query(BaseModel):
  query:str=Field(..., description="query goes here")
class queries(BaseModel):
  queries:List[query]=Field(..., description="queries goes here")