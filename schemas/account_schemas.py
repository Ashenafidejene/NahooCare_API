from pydantic import BaseModel, Field

class AccountCreate(BaseModel):
    full_name: str = Field(..., example="KEBEDE ALEMU Dagne")
    photo_url : str = Field(..., example ="www.haascas/abc/photo.jpg")
    phone_number: str = Field(..., example="+251912345678")
    password: str = Field(..., example="secure_password")
    #gender: str = Field(..., example="Male")
    secret_question: str = Field(..., example="What is my favorite food?")
    secret_answer: str = Field(..., example="Shiro")  # Store answer
    age: int = Field(..., example=44)
class LoginSchema(BaseModel):
    phone_number: str
    password: str
class PasswordResetSchema(BaseModel):
    phone_number: str
    secret_answer: str
    new_password: str
class AccountResponse(BaseModel):
    full_name: str
    phone_number: str
    secret_question: str
    secret_answer: str
    #age:int 
    #photo_url : str
    
class UpdateAccount(BaseExceptionGroup):
    full_name: str
    phone_number:str
    secret_question: str
    secret_answer: str
    password : str