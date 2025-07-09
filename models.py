from pydantic import BaseModel , Field
from typing import List  
class query(BaseModel):
  query:str=Field(..., description="query goes here")
class queries(BaseModel):
  queries:List[query]=Field(..., description="queries goes here")


class State_add(BaseModel):
    initial_ad: str = Field(description="The original ad")
    tone: str = Field(description="The tone of the ad")
    platform: str = Field(description="The platform for the ad")
    polished_ad: str = Field(description="The polished ad")
    is_ok: bool = Field(description="Whether the ad is ok")
    feed_back: str = Field(description="The feedback for the ad")