
from typing import Dict
from pydantic import BaseModel, Field


class SearchMaterial(BaseModel):
    symptom: str = Field(..., example="Fever,Cough,Fatigue")
    latitude: float = Field(..., example=9.021)
    longitude: float = Field(..., example=38.7485)
    #user_id: str = Field(..., example="User_id_09786864r2345243")
    max_distance_km: int = Field(default=10, example=10)
class Respons(BaseModel):
    first_aid :Dict[str, str] = Field(...,examples=[["drink cold water" , "rub your chest"]]) 
    potential_conditions: list[str] = Field(..., examples=[["COVID-19", "Influenza"]])
    