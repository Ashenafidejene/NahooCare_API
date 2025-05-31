from fastapi import APIRouter, HTTPException, Depends, Query
from schemas.admin_schema import AdminCreate, AdminUpdate, AdminLogin
from services.admin_service import create_admin, login_admin, update_admin,user_info_admin
from services.backup_service import backup_database_service, list_backups_service,  restore_database_service
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
async def backup_endpoint():
    # For now, these are synchronous. For long operations, consider BackgroundTasks.
    result = backup_database_service()
    if "error" in result:
        # You might want to return a more specific HTTP status code based on the error
        raise HTTPException(status_code=500, detail=result)
    return result

@router.post("/restore")
async def restore_endpoint(
    backup_file: str = Query(..., description="The filename of the backup to restore (e.g., backup_2025-05-25_16-00-00.gz)"),
    current_admin: dict = Depends(get_current_admin)
):
    # For now, these are synchronous.
    result = restore_database_service(backup_file)
    if "error" in result:
        if "Backup file not found" in result.get("error", ""):
            raise HTTPException(status_code=404, detail=result)
        raise HTTPException(status_code=500, detail=result)
    return result

@router.get("/backups")
async def list_backups_endpoint(current_admin: dict = Depends(get_current_admin)):
    return list_backups_service()
@router.get("/userInfo")
async def userInfo(current_admin: dict = Depends(get_current_admin)):
    return await user_info_admin()
