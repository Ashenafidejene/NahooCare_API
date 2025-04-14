from pydantic import BaseModel, Field
from datetime import datetime


class RatingCreate(BaseModel):
    center_id: str = Field(..., example="3001")
    rating_value: int = Field(..., ge=1, le=5, example=4)
    comment: str = Field(None, example="Good service and staff.")


class RatingResponse(BaseModel):
    rating_id: str
    user_id: str
    center_id: str
    rating_value: int
    comment: str
    rated_at: datetime


class RatingUpdate(BaseModel):
    rating_value: int = Field(..., ge=1, le=5, example=5)
    comment: str = Field(None, example="Updated review after second visit.")