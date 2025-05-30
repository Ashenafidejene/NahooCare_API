from fastapi import APIRouter, HTTPException, Depends
from middleware.admin_auth import get_current_admin
from schemas.healthcare_schema import HealthcareCenterCreate, HealthcareCenterUpdate, HealthcareSearch, HealthcareSearchEngin
from services.healthcare_service import admin_search_healthCare, admin_total_healthCare, create_healthcare_center, delete_healthcare_center, get_healthcareCenter, search_engin_health_care_center, search_healthcare_centers, update_healthcare_center, user_get_all_healthcare_centers
from middleware.auth import get_current_user

router = APIRouter()
@router.get("/user/total_healthcare/")
async def total_healthCare(current_user: dict = Depends(get_current_user) ):
    """
    Endpoint to get total healthcare information for a user.
    """
    result = await user_get_all_healthcare_centers()
    return result
@router.get("/totalInfo")
async def healthCareInfo():
    return await admin_total_healthCare()
@router.get("/get_healthcareCenter/{speciality}")
async def get_healthcare_Center(specialists:str,current_admin: dict = Depends(get_current_admin)):
    result = await admin_search_healthCare(specialists)
    return result
@router.get("/get_healthcare/user/{center_id}")
async def get_healthcare(center_id: str ,current_user: dict = Depends(get_current_user)):
    result = await get_healthcareCenter(center_id)
    return result 
@router.post("/create")
async def create(center: HealthcareCenterCreate,current_admin: dict = Depends(get_current_admin)):#current_user: dict = Depends(get_current_user)):
    result = await create_healthcare_center(center)
    if result : 
        return {"message": "Healthcare center created successfully"}
@router.post("/search")
async def search(search_data: HealthcareSearch,current_user: dict = Depends(get_current_user)):
    return await search_healthcare_centers(current_user["user_id"],search_data)
@router.put("/healthcare/{center_id}")
async def update_center(center_id: str, update_data: HealthcareCenterUpdate,current_admin: dict = Depends(get_current_admin)):#) current_user: dict = Depends(get_current_user)):
    return await update_healthcare_center(center_id, update_data)

@router.delete("/healthcare/{center_id}")
async def delete_center(center_id: str,current_admin: dict = Depends(get_current_admin)):#current_user: dict = Depends(get_current_user)):
    return await delete_healthcare_center(center_id)
@router.post("search/specification/")
async def searchEngin(search_data:HealthcareSearchEngin,current_user: dict = Depends(get_current_user)):
    return await search_engin_health_care_center(current_user["user_id"],search_data)
