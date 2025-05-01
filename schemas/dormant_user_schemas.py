from pydantic import BaseModel, Field

class CreateDormant(BaseModel):
    phone_number : str 
    full_name : str 