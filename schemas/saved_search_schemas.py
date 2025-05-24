from pydantic import BaseModel, Field
from typing import Dict


class SavedSearchCreate(BaseModel):
    search_id: str = Field(..., example="7001")
    user_id: str = Field(..., example="1001")
    #search_time: str = Field(..., example="2025-01-04T14:30:00Z")
    search_parameters: str = Field(..., example="Fever,Cough,Fatigue")
    potential_conditions: list[str] = Field(..., example=["COVID-19", "Influenza"])
    first_aid: Dict[str, str] = Field(..., example={"drink cold water": "rub your chest"})
    results_count: int = Field(..., example=5)
class getSavedSearch(BaseModel):
    search_id:str 
    search_parameters : str
    results_count: int = Field(..., example=5)
    first_aid: Dict[str, str] = Field(..., example={"drink cold water": "rub your chest"})
    potential_conditions: list[str] = Field(..., example=["COVID-19", "Influenza"])
    created_at: str = Field(..., example="2025-01-04T14:30:00Z")
