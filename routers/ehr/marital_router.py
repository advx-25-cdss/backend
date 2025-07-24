from fastapi import APIRouter, HTTPException, Query
from typing import List
from models.ehr_models import Marital
from services.ehr_service import marital_service

router = APIRouter()

@router.post("/", response_model=Marital)
async def create_marital(marital: Marital):
    """Create new marital record"""
    try:
        marital_dict = marital.model_dump(by_alias=True, exclude_unset=True)
        created_record = await marital_service.create(marital_dict)
        return Marital(**created_record)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{record_id}", response_model=Marital)
async def get_marital(record_id: str):
    """Get marital record by ID"""
    try:
        record = await marital_service.get_by_id(record_id)
        if not record:
            raise HTTPException(status_code=404, detail="Marital record not found")
        return Marital(**record)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/patient/{patient_id}", response_model=List[Marital])
async def get_marital_by_patient(patient_id: str):
    """Get all marital records for a specific patient"""
    try:
        records = await marital_service.get_by_patient_id(patient_id)
        return [Marital(**record) for record in records]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[Marital])
async def get_all_marital(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """Get all marital records with pagination"""
    try:
        records = await marital_service.get_all(skip=skip, limit=limit)
        return [Marital(**record) for record in records]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{record_id}", response_model=Marital)
async def update_marital(record_id: str, marital: Marital):
    """Update marital record"""
    try:
        marital_dict = marital.dict(by_alias=True, exclude_unset=True)
        updated_record = await marital_service.update(record_id, marital_dict)
        if not updated_record:
            raise HTTPException(status_code=404, detail="Marital record not found")
        return Marital(**updated_record)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{record_id}")
async def delete_marital(record_id: str):
    """Delete marital record"""
    try:
        deleted = await marital_service.delete(record_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Marital record not found")
        return {"message": "Marital record deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
