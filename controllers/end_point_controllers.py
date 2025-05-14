from fastapi import APIRouter, HTTPException, Depends
from middleware.auth import get_current_user
from schemas.end_point_schemas import SearchMaterial
from services.end_point import User_search

router = APIRouter()
@router.post("/search")
async def end_point(search: SearchMaterial,current_user: dict = Depends(get_current_user)):
    return await User_search(search,current_user.get("user_id"))