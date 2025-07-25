from fastapi import FastAPI
from database import close_mongo_connection, connect_to_mongo
from fastapi.middleware.cors import CORSMiddleware

# Import all EHR routers
from routers.ehr import (
    demographics_router,
    menstrual_router,
    obstetric_router,
    marital_router,
    history_present_illness_router,
    past_medical_history_router,
    family_history_router,
    medication_history_router,
    allergy_history_router,
    social_history_router,
    vital_signs_router
)

# Import diagnosis routers
from routers.diagnosis import case_router, test_router, medicine_router, treatment_router, diagnosis_router, transcription_router

# Import medical imaging router
from medical_imaging import router as medical_imaging_router

app = FastAPI(
    title="EHR System API",
    description="A comprehensive Electronic Health Records system with CRUD operations",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

# Include all EHR routers
app.include_router(demographics_router.router, prefix="/api/ehr/demographics", tags=["Demographics"])
app.include_router(menstrual_router.router, prefix="/api/ehr/menstrual", tags=["Menstrual History"])
app.include_router(obstetric_router.router, prefix="/api/ehr/obstetric", tags=["Obstetric History"])
app.include_router(marital_router.router, prefix="/api/ehr/marital", tags=["Marital Status"])
app.include_router(history_present_illness_router.router, prefix="/api/ehr/history-present-illness", tags=["History of Present Illness"])
app.include_router(past_medical_history_router.router, prefix="/api/ehr/past-medical-history", tags=["Past Medical History"])
app.include_router(family_history_router.router, prefix="/api/ehr/family-history", tags=["Family History"])
app.include_router(medication_history_router.router, prefix="/api/ehr/medication-history", tags=["Medication History"])
app.include_router(allergy_history_router.router, prefix="/api/ehr/allergy-history", tags=["Allergy History"])
app.include_router(social_history_router.router, prefix="/api/ehr/social-history", tags=["Social History"])
app.include_router(vital_signs_router.router, prefix="/api/ehr/vital-signs", tags=["Vital Signs"])

# Include diagnosis routers
app.include_router(case_router.router, prefix="/api/diagnosis", tags=["Cases"])
app.include_router(test_router.router, prefix="/api/diagnosis", tags=["Tests"])
app.include_router(medicine_router.router, prefix="/api/diagnosis", tags=["Medicines"])
app.include_router(treatment_router.router, prefix="/api/diagnosis", tags=["Treatments"])
app.include_router(diagnosis_router.router, prefix="/api/diagnosis", tags=["Diagnosis"])
app.include_router(transcription_router.router, prefix="/api/transcription", tags=["Transcription"])

# Include medical imaging router
app.include_router(medical_imaging_router, prefix="/api/medical-imaging", tags=["Medical Imaging"])

@app.get("/")
async def root():
    return {"message": "EHR System API is running", "docs": "/docs"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "EHR API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
