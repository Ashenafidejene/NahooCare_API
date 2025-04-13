from fastapi import APIRouter, HTTPException, Depends
from schemas.end_point_schemas import SearchMaterial
from services.end_point import User_search

router = APIRouter()
@router.post("/search")
async def end_point(search: SearchMaterial):
    return await User_search(search)