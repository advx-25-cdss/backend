from fastapi import APIRouter, HTTPException, Query
from typing import List
from models.ehr_models import FamilyHistory
from services.ehr_service import family_history_service

router = APIRouter()

@router.post("/", response_model=FamilyHistory)
async def create_family_history(fh: FamilyHistory):
    """Create new family history record"""
    try:
        fh_dict = fh.model_dump(by_alias=True, exclude_unset=True)
        created_record = await family_history_service.create(fh_dict)
        return FamilyHistory(**created_record)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{record_id}", response_model=FamilyHistory)
async def get_family_history(record_id: str):
    """Get family history record by ID"""
    try:
        record = await family_history_service.get_by_id(record_id)
        if not record:
            raise HTTPException(status_code=404, detail="Family history record not found")
        return FamilyHistory(**record)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/patient/{patient_id}", response_model=List[FamilyHistory])
async def get_family_history_by_patient(patient_id: str):
    """Get all family history records for a specific patient"""
    try:
        records = await family_history_service.get_by_patient_id(patient_id)
        return [FamilyHistory(**record) for record in records]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[FamilyHistory])
async def get_all_family_history(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """Get all family history records with pagination"""
    try:
        records = await family_history_service.get_all(skip=skip, limit=limit)
        return [FamilyHistory(**record) for record in records]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{record_id}", response_model=FamilyHistory)
async def update_family_history(record_id: str, fh: FamilyHistory):
    """Update family history record"""
    try:
        fh_dict = fh.dict(by_alias=True, exclude_unset=True)
        updated_record = await family_history_service.update(record_id, fh_dict)
        if not updated_record:
            raise HTTPException(status_code=404, detail="Family history record not found")
        return FamilyHistory(**updated_record)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{record_id}")
async def delete_family_history(record_id: str):
    """Delete family history record"""
    try:
        deleted = await family_history_service.delete(record_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Family history record not found")
        return {"message": "Family history record deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
