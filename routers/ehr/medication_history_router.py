from fastapi import APIRouter, HTTPException, Query
from typing import List
from models.ehr_models import MedicationHistory
from services.ehr_service import medication_history_service

router = APIRouter()

@router.post("/", response_model=MedicationHistory)
async def create_medication_history(mh: MedicationHistory):
    """Create new medication history record"""
    try:
        mh_dict = mh.model_dump(by_alias=True, exclude_unset=True)
        created_record = await medication_history_service.create(mh_dict)
        return MedicationHistory(**created_record)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{record_id}", response_model=MedicationHistory)
async def get_medication_history(record_id: str):
    """Get medication history record by ID"""
    try:
        record = await medication_history_service.get_by_id(record_id)
        if not record:
            raise HTTPException(status_code=404, detail="Medication history record not found")
        return MedicationHistory(**record)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/patient/{patient_id}", response_model=List[MedicationHistory])
async def get_medication_history_by_patient(patient_id: str):
    """Get all medication history records for a specific patient"""
    try:
        records = await medication_history_service.get_by_patient_id(patient_id)
        return [MedicationHistory(**record) for record in records]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[MedicationHistory])
async def get_all_medication_history(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """Get all medication history records with pagination"""
    try:
        records = await medication_history_service.get_all(skip=skip, limit=limit)
        return [MedicationHistory(**record) for record in records]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{record_id}", response_model=MedicationHistory)
async def update_medication_history(record_id: str, mh: MedicationHistory):
    """Update medication history record"""
    try:
        mh_dict = mh.dict(by_alias=True, exclude_unset=True)
        updated_record = await medication_history_service.update(record_id, mh_dict)
        if not updated_record:
            raise HTTPException(status_code=404, detail="Medication history record not found")
        return MedicationHistory(**updated_record)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{record_id}")
async def delete_medication_history(record_id: str):
    """Delete medication history record"""
    try:
        deleted = await medication_history_service.delete(record_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Medication history record not found")
        return {"message": "Medication history record deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
