from fastapi import APIRouter, HTTPException, Depends
from services.symptom_analysis_services import analyze_symptoms
from middleware.auth import get_current_user
from schemas.symptom_analysis_schemas import SymptomAnalysisResponse, SymptomAnalysisRequest
router = APIRouter()
@router.post("/analysis", response_model=SymptomAnalysisResponse)
async def analyze(request: SymptomAnalysisRequest,current_user: dict = Depends(get_current_user)):
    return await analyze_symptoms(request)