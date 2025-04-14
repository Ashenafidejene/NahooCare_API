from fastapi import APIRouter, HTTPException, Depends
from schemas.healthprofile_schema import HealthProfileCreate, HealthProfileUpdate
from services.healthprofile_service import create_health_profile, get_health_profile, update_health_profile, delete_health_profile
from middleware.auth import get_current_user

router = APIRouter()


@router.post("/create")
async def create(profile: HealthProfileCreate,current_user: dict = Depends(get_current_user)):
    result = await create_health_profile(current_user.get("user_id"),profile)
    if result:
        return "Account create success Fully"
    raise HTTPException(status_code=400, detail="Failed to create health profile")


@router.get("/{profile_id}")
async def get_profile(profile_id: str,current_user: dict = Depends(get_current_user)):
    profile = await get_health_profile(profile_id)
    if profile:
        return profile
    raise HTTPException(status_code=404, detail="Health profile not found")


@router.put("/{profile_id}")
async def update_profile(profile_id: str, update_data: HealthProfileUpdate,current_user: dict = Depends(get_current_user)):
    updated = await update_health_profile(profile_id, update_data)
    return updated


@router.delete("/{profile_id}")
async def delete_profile(profile_id: str,current_user: dict = Depends(get_current_user)):
    deleted = await delete_health_profile(profile_id)
    return deleted
