import google.generativeai as genai
import uuid
from datetime import datetime
from db.mongodb import database
from schemas.symptom_analysis_schemas import SymptomAnalysisRequest, SymptomAnalysisResponse
from fastapi import HTTPException
from core.config import settings
from models.symptom_analysis_model import SyptomAnalysis
from google.generativeai.types import GenerationConfig
collection = database["analysis"]
genai.configure(api_key=settings.OPENAI_API_KEY)



# Initialize the model correctly
model = genai.GenerativeModel('gemini-1.5-pro-latest')

async def analyze_symptoms(request: SymptomAnalysisRequest) -> SymptomAnalysisResponse:
    prompt = f"""
    Analyze these symptoms: "{request.symptoms}"
    
    1. List 3-5 possible conditions (comma-separated)
    2. Recommend departments from:
       [Cardiac, Internal Medicine, Pediatrics, Orthopedics, 
        Surgery, Neurology, ENT, General Hospital]
    3. Provide list  simple first aid recommendation that 
       applies to most of these conditions (title + description)
    
    Respond in EXACT format:
    Possible Conditions: condition1, condition2, condition3
    Recommended Departments: department1, department2
    First Aid Title: 3-5 word action title
    First Aid Description: 1-2 sentence simple advice
    """
    
    try:
        # Correct API call with generation config
        response = model.generate_content(
            prompt,
            generation_config=GenerationConfig(
                temperature=0.3,
                max_output_tokens=400
            )
        )
        
        text = response.text.strip()
        
        # Parse response
        conditions = [
            cond.strip() 
            for cond in text.split("Possible Conditions:")[1]
                          .split("Recommended Departments:")[0]
                          .strip()
                          .split(",")
        ]
        
        departments = [
            dept.strip() 
            for dept in text.split("Recommended Departments:")[1]
                           .split("First Aid Title:")[0]
                           .strip()
                           .split(",")
        ]
        first_aid_title = text.split("First Aid Title:")[1].split("First Aid Description:")[0].strip()
        first_aid_desc = text.split("First Aid Description:")[1].strip()
        
        # Prepare and return response
        analysis_data = {
            "analysis_id": str(uuid.uuid4()),
            "user_id": request.user_id,
            "symptoms": [s.strip() for s in request.symptoms.split(",")],
            "potential_conditions": conditions,
            "healthCare_center_specialty": departments,
            "first_aid": {  # Unified first aid for all conditions
                "title": first_aid_title,
                "description": first_aid_desc
            },
            "analyzed_at": datetime.utcnow().isoformat()
        }
        
        await collection.insert_one(analysis_data)
        return SymptomAnalysisResponse(**analysis_data)
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Analysis failed: {str(e)}"
        )
async def delete_symptom_analysis(user_id:str):
    result = await collection.delete_many({"user_id":user_id})
    return result.deleted_count