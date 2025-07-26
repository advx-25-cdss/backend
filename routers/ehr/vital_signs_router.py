from fastapi import APIRouter, HTTPException, Query
from typing import List
from models.ehr_models import VitalSigns
from services.ehr_service import vital_signs_service

router = APIRouter()


@router.post("/", response_model=VitalSigns)
async def create_vital_signs(vs: VitalSigns):
    """Create new vital signs record"""
    try:
        vs_dict = vs.model_dump(by_alias=True, exclude_unset=True)
        created_record = await vital_signs_service.create(vs_dict)
        return VitalSigns(**created_record)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{record_id}", response_model=VitalSigns)
async def get_vital_signs(record_id: str):
    """Get vital signs record by ID"""
    try:
        record = await vital_signs_service.get_by_id(record_id)
        if not record:
            raise HTTPException(status_code=404, detail="Vital signs record not found")
        return VitalSigns(**record)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/patient/{patient_id}", response_model=List[VitalSigns])
async def get_vital_signs_by_patient(patient_id: str):
    """Get all vital signs records for a specific patient"""
    try:
        records = await vital_signs_service.get_by_patient_id(patient_id)
        return [VitalSigns(**record) for record in records]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[VitalSigns])
async def get_all_vital_signs(
    skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000)
):
    """Get all vital signs records with pagination"""
    try:
        records = await vital_signs_service.get_all(skip=skip, limit=limit)
        return [VitalSigns(**record) for record in records]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{record_id}", response_model=VitalSigns)
async def update_vital_signs(record_id: str, vs: VitalSigns):
    """Update vital signs record"""
    try:
        vs_dict = vs.dict(by_alias=True, exclude_unset=True)
        updated_record = await vital_signs_service.update(record_id, vs_dict)
        if not updated_record:
            raise HTTPException(status_code=404, detail="Vital signs record not found")
        return VitalSigns(**updated_record)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{record_id}")
async def delete_vital_signs(record_id: str):
    """Delete vital signs record"""
    try:
        deleted = await vital_signs_service.delete(record_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Vital signs record not found")
        return {"message": "Vital signs record deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
