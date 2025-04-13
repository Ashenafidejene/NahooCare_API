from fastapi import FastAPI

from controllers import database_controller, account_controller, end_point_controllers,healthprofile_controller,healthcare_controller,rating_controller, admin_controller, first_aid_guide_controller, saved_search_controller,symptom_analysis_controller

app = FastAPI()



# Include Routers
app.include_router(database_controller.router, prefix="/api", tags=["Database"])

app.include_router(account_controller.router,prefix='/api/account', tags=['Account'])
app.include_router(healthprofile_controller.router,prefix="/api/healthprofile",tags=["HealthProfile"])
app.include_router(healthcare_controller.router, prefix="/api/healthcare", tags=["Healthcare Centers"])
app.include_router(rating_controller.router, prefix="/api/rating", tags=["Ratings"])
app.include_router(admin_controller.router, prefix="/api/admin", tags=["Admin"])

app.include_router(first_aid_guide_controller.router, prefix="/api/first-aid-guide", tags=["First Aid Guide"])
app.include_router(saved_search_controller.router, prefix="/api/saved-searches", tags=["Saved Searches"])
app.include_router(symptom_analysis_controller.router,prefix='/api/SymptomAnalysis',tags=["Ai-Analysis"])
app.include_router(end_point_controllers.router,prefix='/api/endpoint',tags=["end-point"])

