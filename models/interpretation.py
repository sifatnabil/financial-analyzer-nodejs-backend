from pydantic import BaseModel
from models.summaries import Summary
from models.differences import Difference
from typing import List

class Interpretation(BaseModel):
    summary: Summary
    difference: Difference
    summaryId: str
    ids: List[str]

class InterpretationResponse(BaseModel):
    summaryId: str
    chosen_prompt_id: str