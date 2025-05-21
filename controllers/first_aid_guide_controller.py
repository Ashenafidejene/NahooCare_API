from fastapi import APIRouter, HTTPException, Depends
from schemas.first_aid_guide_schemas import FirstAidGuideCreate, FirstAidGuideUpdate
from services.first_aid_guide_service import (
    create_first_aid_guide,
    get_first_aid_guide,
    update_first_aid_guide,
    delete_first_aid_guide,
    get_all_first_aid_guides
)
from middleware.auth import get_current_user
from middleware.admin_auth import get_current_admin

router = APIRouter()

# Create a New First Aid Guide
@router.post("/create")
async def add_first_aid_guide(guide: FirstAidGuideCreate):
    """
    Creates a new first aid guide in the database.
    
    Args:
        guide (FirstAidGuideCreate): The data for the new first aid guide.
    
    Returns:
        dict: A success message with the guide ID or raises a 400 error if the guide ID already exists.
    """
    result = await create_first_aid_guide(guide)
    if result:
        return {"message": "First aid guide created successfully", "id": result}
    raise HTTPException(status_code=400, detail="Guide ID already exists")

# Get All First Aid Guides
@router.get("/all")
async def get_all_guides():
    """
    Retrieves all first aid guides from the database.
    
    Returns:
        list: A list of all first aid guides, or raises a 404 error if no guides are found.
    """
    guides = await get_all_first_aid_guides()
    if isinstance(guides, dict) and "message" in guides:
        raise HTTPException(status_code=404, detail=guides["message"])
    return guides

# Get a First Aid Guide by ID
@router.get("/{guide_id}")
async def get_guide(guide_id: str):
    """
    Retrieves a specific first aid guide by its ID.
    Args:
        guide_id (str): The ID of the guide to retrieve.
    Returns:
        dict: The first aid guide if found, or raises a 404 error if not found.
    """
    guide = await get_first_aid_guide(guide_id)
    if guide:
        return guide
    raise HTTPException(status_code=404, detail="First aid guide not found")

# Update an Existing First Aid Guide
@router.put("/{guide_id}")
async def update_guide(guide_id: str, update_data: FirstAidGuideUpdate,current_admin: dict = Depends(get_current_admin)):
    """
    Updates an existing first aid guide with new data.
    
    Args:
        guide_id (str): The ID of the guide to update.
        update_data (FirstAidGuideUpdate): The updated data for the guide.
    
    Returns:
        dict: A success message or raises a 400 error if the update fails.
    """
    modified_count = await update_first_aid_guide(guide_id, update_data)
    if modified_count:
        return {"message": "First aid guide updated successfully"}
    raise HTTPException(status_code=400, detail="Failed to update the first aid guide")

# Delete a First Aid Guide by ID
@router.delete("/{guide_id}")
async def delete_guide(guide_id: str,current_admin: dict = Depends(get_current_admin)):
    """
    Deletes a specific first aid guide by its ID.
    
    Args:
        guide_id (str): The ID of the guide to delete.
    
    Returns:
        dict: A success message or raises a 400 error if the deletion fails.
    """
    deleted_count = await delete_first_aid_guide(guide_id)
    if deleted_count:
        return {"message": "First aid guide deleted successfully"}
    raise HTTPException(status_code=400, detail="Failed to delete the first aid guide")
