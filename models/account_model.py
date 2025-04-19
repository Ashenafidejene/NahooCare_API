from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime

class PyObjectId(str):
    """Custom validator for MongoDB ObjectId"""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)  # Store as string for compatibility

class Account(BaseModel):
    id: PyObjectId = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    user_id: str 
    full_name: str
    phone_number: str
    hashed_password: str  # Store hashed passwords
    #gender: str
    secret_question: str
    secret_answer: str  # Store hashed secret answer
    #age: int
    created_at: str

    class Config:
        json_encoders = {ObjectId: str}  # Ensure ObjectId is serialized as a string
        arbitrary_types_allowed = True  # Allows ObjectId if needed