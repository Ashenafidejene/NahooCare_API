from fastapi import APIRouter, HTTPException, Depends
from schemas.healthcare_schema import HealthcareCenterCreate, HealthcareCenterUpdate, HealthcareSearch, HealthcareSearchEngin
from services.healthcare_service import create_healthcare_center, delete_healthcare_center, get_healthcareCenter, search_engin_health_care_center, search_healthcare_centers, update_healthcare_center
from middleware.auth import get_current_user

router = APIRouter()
@router.get("/get_healthcareCenter/{name}")
async def get_healthcare_Center(name:str):
    result = await get_healthcareCenter(name)
    return result

@router.post("/create")
async def create(center: HealthcareCenterCreate):#current_user: dict = Depends(get_current_user)):
    result = await create_healthcare_center(center)
    if result : 
        return {"message": "Healthcare center created successfully"}

@router.post("/search")
async def search(user_id:str,search_data: HealthcareSearch):#current_user: dict = Depends(get_current_user)):
    return await search_healthcare_centers(user_id,search_data)
@router.put("/healthcare/{center_id}")
async def update_center(center_id: str, update_data: HealthcareCenterUpdate):#) current_user: dict = Depends(get_current_user)):
    return await update_healthcare_center(center_id, update_data)

@router.delete("/healthcare/{center_id}")
async def delete_center(center_id: str):#current_user: dict = Depends(get_current_user)):
    return await delete_healthcare_center(center_id)
@router.post("search/specification/")
async def searchEngin(user_id:str,search_data:HealthcareSearchEngin):
    return await search_engin_health_care_center(user_id,search_data)