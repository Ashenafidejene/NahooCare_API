from pydantic import BaseModel, Field
from typing import Dict
from bson import ObjectId

class PyObjectId(str):
    """Custom validator for MongoDB ObjectId."""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)  # Store ObjectId as string for compatibility

class SavedSearch(BaseModel):
    id: PyObjectId 
    search_id: str 
    user_id: str
    search_parameters: str 
    potential_conditions: list[str]
    first_aid: Dict[str, str]
    results_count: int
    search_time: str = Field(..., example="2025-01-04T14:30:00Z")
    class Config:
        json_encoders = {ObjectId: str}  # Ensures ObjectId is serialized as a string
        arbitrary_types_allowed = True  # Allows ObjectId if needed for validation

