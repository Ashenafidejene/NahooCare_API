from fastapi import HTTPException
from datetime import timedelta
from db.mongodb import database
from models.admin_model import Admin
from schemas.admin_schema import AdminCreate, AdminUpdate, AdminLogin
from services.account_service import user_info
from core.security import hash_password, verify_password, create_access_token
import uuid
from core.config import settings
import logging

collection = database["admins"]


async def create_admin(admin: AdminCreate):
    try:
        existing_admin = await collection.find_one({"email": admin.email})
        if existing_admin:
            raise HTTPException(status_code=400, detail="Admin email already registered")

        admin_data = admin.dict()
        admin_data["admin_id"] = str(uuid.uuid4())
        result = await collection.insert_one()
        if not result.inserted_id:
            raise HTTPException(status_code=500, detail="Failed to create admin account")
        return str(result.inserted_id)

    except Exception as e:
        logging.error(f"Error creating admin: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

async def login_admin(admin: AdminLogin):
    admin_record = await collection.find_one({"email": admin.email})
    if not admin_record or not verify_password(admin.password, admin_record["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": admin_record["email"],"admin_id":admin_record["admin_id"]}, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": token, "token_type": "bearer"}


async def update_admin(admin_id: str, update_data: AdminUpdate):
    result = await collection.update_one({"admin_id": admin_id}, {"$set": update_data.dict(exclude_unset=True)})
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="No changes were made")

    return {"message": "Admin updated successfully"}
async def user_info_admin():
    return await user_info()