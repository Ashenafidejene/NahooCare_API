from typing import List
from pydantic import BaseModel, Field

class FirstAidGuideCreate(BaseModel):
    """
    Model for creating a new first aid guide.
    Includes required fields: guide ID, emergency type, instructions, and category.
    """
    emergency_title: str = Field(..., example="Burns")
    instructions: List[str] = Field(..., example=["Cool burn with water", "Cover with clean cloth"])
    image_url: str = Field(..., example="https://example.com/image.jpg")
    category: str = Field(..., example="Burn")

class FirstAidGuideUpdate(BaseModel):
    """
    Model for updating an existing first aid guide.
    Fields are optional for partial updates.
    """
    emergency_title: str = Field(None, example="Fractures")
    instructions: List[str] = Field(None, example=["Immobilize the fracture site and seek medical help."])
    image_url: str = Field(None, example="https://example.com/image.jpg")
    category: str = Field(None, example="Fracture")

class FirstAidGuideResponse(BaseModel):
    """
    Response model for retrieving a first aid guide.
    Contains guide ID, emergency title, instructions, and category.
    """
    emergency_title: str
    instructions: List[str]
    image_url: str
    category: str

class FirstAidGuideDeleteResponse(BaseModel):
    """
    Response model for the deletion of a first aid guide.
    Contains guide ID and a success message.
    """
    guide_id: str = Field(..., example="6001")
    message: str = Field(..., example="First aid guide successfully deleted.")
