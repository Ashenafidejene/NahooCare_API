from fastapi import APIRouter, HTTPException, Depends
from schemas.rating_schema import RatingCreate,RatingUpdate
from services.rating_service import recalculate_healthcare_rating, remove_inappropriate_review, submit_rating, get_ratings ,update_rating
from middleware.auth import get_current_user
from middleware.admin_auth import get_current_admin
router = APIRouter()
@router.post("/submit")
async def rate(rating: RatingCreate, current_user: dict = Depends(get_current_user)):
    result = await submit_rating(current_user["user_id"],rating=RatingCreate)
    if result : 
        return {"message": "Rating submitted successfully"}
@router.get("/{center_id}")
async def get_center_ratings(center_id: str):
    return await get_ratings(center_id)
@router.put("/{center_id}")
async def edit_rating(center_id: str, update_data: RatingUpdate,current_user: dict = Depends(get_current_user)):
    return await update_rating(current_user["user_id"], center_id, update_data)
@router.delete("{rating_id}")
async def delete_review(rating_id: str ,current_admin: dict = Depends(get_current_admin)):
    return await remove_inappropriate_review(rating_id)
@router.post("/recalculate-rating/{center_id}")
async def recalculate_rating(center_id: str,current_admin: dict = Depends(get_current_admin)):
    return await recalculate_healthcare_rating(center_id)
