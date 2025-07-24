from fastapi import APIRouter, HTTPException, Query
from typing import List
from models.ehr_models import Menstrual
from services.ehr_service import menstrual_service

router = APIRouter()

@router.post("/", response_model=Menstrual)
async def create_menstrual(menstrual: Menstrual):
    """Create new menstrual record"""
    try:
        menstrual_dict = menstrual.model_dump(by_alias=True, exclude_unset=True)
        created_record = await menstrual_service.create(menstrual_dict)
        return Menstrual(**created_record)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{record_id}", response_model=Menstrual)
async def get_menstrual(record_id: str):
    """Get menstrual record by ID"""
    try:
        record = await menstrual_service.get_by_id(record_id)
        if not record:
            raise HTTPException(status_code=404, detail="Menstrual record not found")
        return Menstrual(**record)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/patient/{patient_id}", response_model=List[Menstrual])
async def get_menstrual_by_patient(patient_id: str):
    """Get all menstrual records for a specific patient"""
    try:
        records = await menstrual_service.get_by_patient_id(patient_id)
        return [Menstrual(**record) for record in records]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[Menstrual])
async def get_all_menstrual(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """Get all menstrual records with pagination"""
    try:
        records = await menstrual_service.get_all(skip=skip, limit=limit)
        return [Menstrual(**record) for record in records]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{record_id}", response_model=Menstrual)
async def update_menstrual(record_id: str, menstrual: Menstrual):
    """Update menstrual record"""
    try:
        menstrual_dict = menstrual.dict(by_alias=True, exclude_unset=True)
        updated_record = await menstrual_service.update(record_id, menstrual_dict)
        if not updated_record:
            raise HTTPException(status_code=404, detail="Menstrual record not found")
        return Menstrual(**updated_record)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{record_id}")
async def delete_menstrual(record_id: str):
    """Delete menstrual record"""
    try:
        deleted = await menstrual_service.delete(record_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Menstrual record not found")
        return {"message": "Menstrual record deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
