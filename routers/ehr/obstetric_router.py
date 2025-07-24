from fastapi import APIRouter, HTTPException, Query
from typing import List
from models.ehr_models import Obstetric
from services.ehr_service import obstetric_service

router = APIRouter()

@router.post("/", response_model=Obstetric)
async def create_obstetric(obstetric: Obstetric):
    """Create new obstetric record"""
    try:
        obstetric_dict = obstetric.model_dump(by_alias=True, exclude_unset=True)
        created_record = await obstetric_service.create(obstetric_dict)
        return Obstetric(**created_record)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{record_id}", response_model=Obstetric)
async def get_obstetric(record_id: str):
    """Get obstetric record by ID"""
    try:
        record = await obstetric_service.get_by_id(record_id)
        if not record:
            raise HTTPException(status_code=404, detail="Obstetric record not found")
        return Obstetric(**record)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/patient/{patient_id}", response_model=List[Obstetric])
async def get_obstetric_by_patient(patient_id: str):
    """Get all obstetric records for a specific patient"""
    try:
        records = await obstetric_service.get_by_patient_id(patient_id)
        return [Obstetric(**record) for record in records]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[Obstetric])
async def get_all_obstetric(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """Get all obstetric records with pagination"""
    try:
        records = await obstetric_service.get_all(skip=skip, limit=limit)
        return [Obstetric(**record) for record in records]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{record_id}", response_model=Obstetric)
async def update_obstetric(record_id: str, obstetric: Obstetric):
    """Update obstetric record"""
    try:
        obstetric_dict = obstetric.dict(by_alias=True, exclude_unset=True)
        updated_record = await obstetric_service.update(record_id, obstetric_dict)
        if not updated_record:
            raise HTTPException(status_code=404, detail="Obstetric record not found")
        return Obstetric(**updated_record)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{record_id}")
async def delete_obstetric(record_id: str):
    """Delete obstetric record"""
    try:
        deleted = await obstetric_service.delete(record_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Obstetric record not found")
        return {"message": "Obstetric record deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
