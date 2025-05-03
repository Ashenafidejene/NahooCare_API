from fastapi import APIRouter, HTTPException, Depends
from schemas.admin_schema import AdminCreate, AdminUpdate, AdminLogin
from services.admin_service import create_admin, login_admin, update_admin,user_info_admin
from services.backup_service import backup_database, restore_database
from middleware.admin_auth import get_current_admin

router = APIRouter()


@router.post("/register")
async def register(admin: AdminCreate,current_admin: dict = Depends(get_current_admin)):
    result = await create_admin(admin)
    if result : 
        return {"message": "Admin registered successfully"}


@router.post("/login")
async def login(admin: AdminLogin ):
    return await login_admin(admin)


@router.put("/")
async def update(update_data: AdminUpdate , current_admin: dict = Depends(get_current_admin)):# current_user: dict = Depends(get_current_user)):
    return await update_admin(current_admin["admin_id"], update_data)
@router.post("/backup")
async def backup(current_admin: dict = Depends(get_current_admin)):
    return backup_database()
@router.post("/restore")
async def restore(backup_file: str ,current_admin: dict = Depends(get_current_admin)):
    return restore_database(backup_file)
@router.get("/userInfo")
async def userInfo(current_admin: dict = Depends(get_current_admin)):
    return await user_info_admin()
