from fastapi import APIRouter, HTTPException, Query
from typing import List
from models.ehr_models import PastMedicalHistory
from services.ehr_service import past_medical_history_service

router = APIRouter()


@router.post("/", response_model=PastMedicalHistory)
async def create_past_medical_history(pmh: PastMedicalHistory):
    """Create new past medical history record"""
    try:
        pmh_dict = pmh.model_dump(by_alias=True, exclude_unset=True)
        created_record = await past_medical_history_service.create(pmh_dict)
        return PastMedicalHistory(**created_record)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{record_id}", response_model=PastMedicalHistory)
async def get_past_medical_history(record_id: str):
    """Get past medical history record by ID"""
    try:
        record = await past_medical_history_service.get_by_id(record_id)
        if not record:
            raise HTTPException(
                status_code=404, detail="Past medical history record not found"
            )
        return PastMedicalHistory(**record)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/patient/{patient_id}", response_model=List[PastMedicalHistory])
async def get_past_medical_history_by_patient(patient_id: str):
    """Get all past medical history records for a specific patient"""
    try:
        records = await past_medical_history_service.get_by_patient_id(patient_id)
        return [PastMedicalHistory(**record) for record in records]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[PastMedicalHistory])
async def get_all_past_medical_history(
    skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000)
):
    """Get all past medical history records with pagination"""
    try:
        records = await past_medical_history_service.get_all(skip=skip, limit=limit)
        return [PastMedicalHistory(**record) for record in records]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{record_id}", response_model=PastMedicalHistory)
async def update_past_medical_history(record_id: str, pmh: PastMedicalHistory):
    """Update past medical history record"""
    try:
        pmh_dict = pmh.dict(by_alias=True, exclude_unset=True)
        updated_record = await past_medical_history_service.update(record_id, pmh_dict)
        if not updated_record:
            raise HTTPException(
                status_code=404, detail="Past medical history record not found"
            )
        return PastMedicalHistory(**updated_record)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{record_id}")
async def delete_past_medical_history(record_id: str):
    """Delete past medical history record"""
    try:
        deleted = await past_medical_history_service.delete(record_id)
        if not deleted:
            raise HTTPException(
                status_code=404, detail="Past medical history record not found"
            )
        return {"message": "Past medical history record deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
