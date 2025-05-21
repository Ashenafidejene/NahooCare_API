from typing import List
from pydantic import BaseModel, Field
from bson import ObjectId

class PyObjectId(str):
    """
    Custom validator for MongoDB ObjectId.
    Ensures the value is a valid ObjectId string.
    """
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        """Validates if the value is a valid ObjectId."""
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)

class FirstAidGuide(BaseModel):
    """
    Pydantic model for a first aid guide.
    Includes emergency type, instructions, and category.
    """
    id: PyObjectId = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    guide_id: str
    emergency_title: str
    instructions: List[str]
    image_url: str
    category: str

    class Config:
        """Config for serializing ObjectId as string."""
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True
