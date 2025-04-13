from pydantic import BaseModel, Field
from typing import Dict


class SavedSearchCreate(BaseModel):
    search_id: str = Field(..., example="7001")
    user_id: str = Field(..., example="1001")
    #search_time: str = Field(..., example="2025-01-04T14:30:00Z")
    search_parameters: dict
    results_count: int
    Analysis_id: str =  Field(..., example="7001")
class SavedSearchResponse(BaseModel):
    search_id: str
    user_id: str
    search_parameters: dict
    results_count: int
    created_at: str

