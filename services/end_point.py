

import uuid
from schemas.end_point_schemas import Respons, SearchMaterial
from schemas.healthcare_schema import HealthcareSearch
from schemas.saved_search_schemas import SavedSearchCreate
from schemas.symptom_analysis_schemas import SymptomAnalysisRequest
from services.healthcare_service import search_healthcare_centers
from services.saved_search_service import create_search_record
from services.symptom_analysis_services import analyze_symptoms


async def User_search(search :SearchMaterial ):
    symptom_obeject = SymptomAnalysisRequest(symptoms=search.symptom,user_id=search.user_id)
    
    analysis = await analyze_symptoms(symptom_obeject)
    specialties = analysis.healthCare_center_specialty
    hospitalData = HealthcareSearch(latitude=search.latitude,longitude = search.longitude ,specialties=specialties,max_distance_km=search.max_distance_km)
    health_center_data = await  search_healthcare_centers(search.user_id ,hospitalData)

    search_record = SavedSearchCreate(
        user_id=search.user_id,
        search_id=str(uuid.uuid4()),
        search_parameters=symptom_obeject.model_dump(),
        results_count=len(health_center_data ),
        Analysis_id = analysis.analysis_id
    )
    await create_search_record(search_record)
    
    return [Respons(first_aid=analysis.first_aid,potential_conditions=analysis.potential_conditions),health_center_data]