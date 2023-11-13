from typing import List

from pydantic import BaseModel
from base.response import Data

class LanuageData(BaseModel):
    language_id: int
    language_code: str
    name: str

class LanuageResponse(Data):
    data: List[LanuageData]
