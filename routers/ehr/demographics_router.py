from fastapi import APIRouter, HTTPException, Query
from typing import List
from models.ehr_models import Demographics
from services.ehr_service import demographics_service


router = APIRouter()


@router.post("/", response_model=Demographics)
async def create_demographics(demographics: Demographics):
    """Create new demographics record"""
    try:
        demographics_dict = demographics.model_dump(by_alias=True, exclude_unset=True)
        created_record = await demographics_service.create(demographics_dict)
        return Demographics(**created_record)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{record_id}", response_model=Demographics)
async def get_demographics(record_id: str):
    """Get demographics record by ID"""
    try:
        record = await demographics_service.get_by_id(record_id)
        if not record:
            raise HTTPException(status_code=404, detail="Demographics record not found")
        return Demographics(**record)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/patient/{patient_id}", response_model=List[Demographics])
async def get_demographics_by_patient(patient_id: str):
    """Get all demographics records for a specific patient"""
    try:
        records = await demographics_service.get_by_patient_id(patient_id)
        return [Demographics(**record) for record in records]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[Demographics])
async def get_all_demographics(
    skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000)
):
    """Get all demographics records with pagination"""
    try:
        records = await demographics_service.get_all(skip=skip, limit=limit)
        return [Demographics(**record) for record in records]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{record_id}", response_model=Demographics)
async def update_demographics(record_id: str, demographics: Demographics):
    """Update demographics record"""
    try:
        demographics_dict = demographics.model_dump(by_alias=True, exclude_unset=True)
        updated_record = await demographics_service.update(record_id, demographics_dict)
        if not updated_record:
            raise HTTPException(status_code=404, detail="Demographics record not found")
        return Demographics(**updated_record)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{record_id}")
async def delete_demographics(record_id: str):
    """Delete demographics record"""
    try:
        deleted = await demographics_service.delete(record_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Demographics record not found")
        return {"message": "Demographics record deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
