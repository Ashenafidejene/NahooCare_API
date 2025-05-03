from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional, Union


class HealthcareCenterCreate(BaseModel):
    name: str = Field(..., example="Yekatit 12 General Hospital")
    address: str = Field(..., example="Sdsst Kilo, Addis Ababa")
    latitude: float = Field(..., example=9.0456)
    longitude: float = Field(..., example=38.7612)
    specialists: List[str] = Field(..., example=["Cardiology", "Neurology"])
    contact_info: Optional[Dict[str, str]] = Field(..., example= {
    "Reception": "+251-11-123-4567",
    "Emergency": "+251-91-234-5678"})
    available_time : List[str] = Field(..., example=["it works every day 8:00 am - 10:pm "])

class HealthcareSearch(BaseModel):
    specialties: List[str] = Field(..., example=["Cardiology", "Neurology"])
    latitude: float = Field(..., example=9.0456)
    longitude: float = Field(..., example=38.7612)
    max_distance_km: int = Field(default=10, example=10)
class HealthcareCenterUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Updated Hospital Name")
    address: Optional[str] = Field(None, example="New Address, Addis Ababa")
    latitude: Optional[float] = Field(None, example=9.0556)
    longitude: Optional[float] = Field(None, example=38.7623)
    specialists: Optional[List[str]] = Field(None, example=["Pediatrics", "Cardiology"])
    contact_info: Optional[Dict[str, str]] = Field(None, example= {
    "Reception": "+251-11-123-4567",
    "Emergency": "+251-91-234-5678"})
    available_time : Optional[List[str]] = Field(..., example=["it works every day 8:00 am - 10:pm "])
class SearchOutput(BaseModel):
    center_id:str =  Field(..., example="center_id_Yekatit")
    name: str = Field(..., example="Yekatit 12 General Hospital")
    latitude: float = Field(..., example=9.0456)
    longitude: float = Field(..., example=38.7612)
class HelathcareCenterRespons(BaseModel):
    center_id:str =  Field(..., example="center_id_Yekatit")
    name: str = Field(..., example="Yekatit 12 General Hospital")
    address: str = Field(..., example="Sdsst Kilo, Addis Ababa")
    latitude: float = Field(..., example=9.0456)
    longitude: float = Field(..., example=38.7612)
    specialists: List[str] = Field(..., example=["Cardiology", "Neurology"])
    contact_info: Dict[str, str]= Field(None, example= {
    "Reception": "+251-11-123-4567",
    "Emergency": "+251-91-234-5678"})
    available_time : List[str] = Field(..., example=["it works every day 8:00 am - 10:pm "]) 
class HealthcareSearchEngin(BaseModel):
    """Search schema for healthcare centers with location-based filtering"""
    name: Optional[str] = Field(
        None,
        example="City General",
        description="Case-insensitive partial name match"
    )
    
    specialty: Optional[Union[str, List[str]]] = Field(
        None,
        example=["Cardiology", "Neurology"],
        description="Single specialty or list of specialties to match"
    )
    
    latitude: Optional[float] = Field(
        None,
        ge=-90,
        le=90,
        example=9.0456,
        description="Latitude for location search (-90 to 90)"
    )
    
    longitude: Optional[float] = Field(
        None,
        ge=-180,
        le=180,
        example=38.7612,
        description="Longitude for location search (-180 to 180)"
    )
    
    max_distance_km: int = Field(
        default=10,
        ge=1,
        le=100,
        example=15,
        description="Maximum search distance in kilometers (1-100 km)"
    )

    @validator('specialty', pre=True)
    def convert_str_to_list(cls, v):
        """Convert string specialty to single-item list for consistency"""
        if isinstance(v, str):
            return [v]
        return v

    class Config:
        schema_extra = {
            "example": {
                "name": "City General",
                "specialty": ["Cardiology"],
                "latitude": 9.0456,
                "longitude": 38.7612,
                "max_distance_km": 10
            }
        }