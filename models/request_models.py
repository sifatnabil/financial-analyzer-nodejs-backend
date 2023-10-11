from pydantic import BaseModel
from typing import List

class Transactions(BaseModel):
    transactions: List[dict] | dict