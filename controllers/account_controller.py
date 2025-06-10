from fastapi import APIRouter, HTTPException, Depends

from datetime import timedelta
from schemas.account_schemas import AccountCreate, AccountResponse, LoginSchema, PasswordResetSchema, UpdateAccount
from services.account_service import create_account, authenticate_user, get_account, get_secrete_question, update_account, delete_account, reset_password
from core.security import create_access_token
from core.config import settings
from middleware.auth import get_current_user

router = APIRouter()
"""
This module defines the account-related API endpoints for the FastAPI application.
It includes routes for user registration, login, account retrieval, account updates, 
account deletion, secret question retrieval, and password reset.
Routes:
    - POST /register: Register a new user account.
    - POST /login: Authenticate a user and return a JWT token.
    - GET /{user_id}: Retrieve account details for a specific user.
    - GET /getSecretQuestion/{phone_number}: Retrieve the secret question for a user by phone number.
    - PUT /{user_id}: Update account details for a specific user.
    - DELETE /{user_id}: Delete a specific user account.
    - POST /reset-password: Reset a user's password.
"""
# Register User
@router.post("/register")
async def register(account: AccountCreate):
    """
    Register a new user account.
    Args:
        account (AccountCreate): The account creation schema containing user details.
    Returns:
        dict: A success message if the account is created successfully.
    Raises:
        HTTPException: If the phone number is already registered.
    """
    result = await create_account(account)
    if result:
        return {"message":"Account created successfully"}
    raise HTTPException(status_code=400, detail="Phone number already registered")

# Login and Get JWT Token
@router.post("/login")
async def login(data: LoginSchema):
    """
    Authenticate a user and return a JWT token.
    Args:
        data (LoginSchema): The login schema containing phone number and password.
    Returns:
        dict: A dictionary containing the access token and token type.
    Raises:
        HTTPException: If the phone number or password is invalid.
    """
    user = await authenticate_user(data.phone_number, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid phone number or password")

    access_token = create_access_token({"sub": user["user_id"],"user_id":user["user_id"]}, expires_delta=timedelta(minutes=720))
    return {"access_token": access_token, "token_type": "bearer","full_name":user['full_name'],"image_url":user['photo_url']}

# Get Account (Protected Route)
@router.get("/")

async def get_user_account(current_user: dict = Depends(get_current_user)): 
    """
    Retrieve account details for a specific user.
    Args:
        user_id (str): The ID of the user whose account details are to be retrieved.
    Returns:
        dict: The account details of the user.
    Raises:
        HTTPException: If the user is not found.
    """
    account = await get_account(current_user["user_id"])
    if account:
        return account
    raise HTTPException(status_code=404, detail="User not found")
@router.get("/getSecretQuestion/{phone_number}")
async def get_secret_question(phone_number:str):
    """
    Retrieve the secret question for a user by phone number.
    Args:
        phone_number (str): The phone number of the user.
    Returns:
        dict: The secret question associated with the user's account.
    Raises:
        HTTPException: If the user is not found.
    """
    result = await get_secrete_question(phone_number)
    if result:
        return result
    return HTTPException(status_code=404, detail="User not found")
@router.put("/")
async def update_user_account( update_data:  UpdateAccount  ,current_user: dict = Depends(get_current_user)):
    """
    Update account details for a specific user.
    Args:
        user_id (str): The ID of the user whose account is to be updated.
        update_data (AccountResponse): The updated account details.
    Returns:
        dict: A success message if the account is updated successfully.
    Raises:
        HTTPException: If the account update fails.
    """
    modified_count = await update_account(current_user["user_id"],update_data=update_data)#current_user.get("user_id"), update_data)
    if modified_count:
        return {"message": "Account updated successfully"}
    raise HTTPException(status_code=400, detail="Failed to update account")


@router.delete("/")
async def delete_user_account(current_user: dict = Depends(get_current_user)):
    """
    Delete a specific user account.
    Args:
        user_id (str): The ID of the user whose account is to be deleted.
    Returns:
        dict: A success message if the account is deleted successfully.
    Raises:
        HTTPException: If the account deletion fails.
    """
    deleted_count = await delete_account(current_user["user_id"])#current_user.get("user_id"))
    if deleted_count:
        return {"message": "Account deleted successfully"}
    raise HTTPException(status_code=400, detail="Failed to delete account")


@router.post("/reset-password")
async def reset_user_password(data: PasswordResetSchema):
    """
    Reset a user's password.
    Args:
        data (PasswordResetSchema): The password reset schema containing phone number, 
                                    secret answer, and new password.
    Returns:
        dict: A success message if the password is reset successfully.
    Raises:
        HTTPException: If the secret answer or phone number is invalid.
    """    
    success = await reset_password(data)
    if success:
        return {"message": "Password reset successfully"}
    raise HTTPException(status_code=400, detail="Invalid secret answer or phone number")
