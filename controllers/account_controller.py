from fastapi import APIRouter, HTTPException, Depends
from datetime import timedelta
from schemas.account_schemas import AccountCreate, AccountResponse, LoginSchema, PasswordResetSchema
from services.account_service import create_account, authenticate_user, get_account, get_secrete_question, update_account, delete_account, reset_password
from core.security import create_access_token
from core.config import settings
from middleware.auth import get_current_user

router = APIRouter()

# Register User
@router.post("/register")
async def register(account: AccountCreate):
    result = await create_account(account)
    if result:
        return {"Account created successfully"}
    raise HTTPException(status_code=400, detail="Phone number already registered")

# Login and Get JWT Token
@router.post("/login")
async def login(data: LoginSchema):
    user = await authenticate_user(data.phone_number, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid phone number or password")

    access_token = create_access_token({"sub": user["user_id"],"user_id":user["user_id"]}, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}

# Get Account (Protected Route)
@router.get("/")
async def get_user_account(current_user: dict = Depends(get_current_user)): 
    account = await get_account(current_user.get("user_id"))
    if account:
        return account
    raise HTTPException(status_code=404, detail="User not found")
@router.get("/getSecretQuestion/{phone_number}")
async def get_secret_question(phone_number:str):
    result = await get_secrete_question(phone_number)
    if result:
        return result
    return HTTPException(status_code=404, detail="User not found")
@router.put("/{user_id}")
async def update_user_account(str, update_data:  AccountResponse,current_user: dict = Depends(get_current_user)):
    modified_count = await update_account(current_user.get("user_id"), update_data)
    if modified_count:
        return {"message": "Account updated successfully"}
    raise HTTPException(status_code=400, detail="Failed to update account")


@router.delete("/",)
async def delete_user_account(current_user: dict = Depends(get_current_user)):
    deleted_count = await delete_account(current_user.get("user_id"))
    if deleted_count:
        return {"message": "Account deleted successfully"}
    raise HTTPException(status_code=400, detail="Failed to delete account")


@router.post("/reset-password")
async def reset_user_password(data: PasswordResetSchema):
    success = await reset_password(data)
    if success:
        return {"message": "Password reset successfully"}
    raise HTTPException(status_code=400, detail="Invalid secret answer or phone number")
