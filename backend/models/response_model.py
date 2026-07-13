from pydantic import BaseModel
from typing import List

class DiffItem(BaseModel):
    type: str
    old: str
    new: str

class CompareResponse(BaseModel):
    file1: str
    file2: str
    diff: List[DiffItem]