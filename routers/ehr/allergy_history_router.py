from fastapi import APIRouter, HTTPException, Query
from typing import List
from models.ehr_models import AllergyHistory
from services.ehr_service import allergy_history_service

router = APIRouter()

@router.post("/", response_model=AllergyHistory)
async def create_allergy_history(ah: AllergyHistory):
    """Create new allergy history record"""
    try:
        ah_dict = ah.model_dump(by_alias=True, exclude_unset=True)
        created_record = await allergy_history_service.create(ah_dict)
        return AllergyHistory(**created_record)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{record_id}", response_model=AllergyHistory)
async def get_allergy_history(record_id: str):
    """Get allergy history record by ID"""
    try:
        record = await allergy_history_service.get_by_id(record_id)
        if not record:
            raise HTTPException(status_code=404, detail="Allergy history record not found")
        return AllergyHistory(**record)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/patient/{patient_id}", response_model=List[AllergyHistory])
async def get_allergy_history_by_patient(patient_id: str):
    """Get all allergy history records for a specific patient"""
    try:
        records = await allergy_history_service.get_by_patient_id(patient_id)
        return [AllergyHistory(**record) for record in records]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[AllergyHistory])
async def get_all_allergy_history(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """Get all allergy history records with pagination"""
    try:
        records = await allergy_history_service.get_all(skip=skip, limit=limit)
        return [AllergyHistory(**record) for record in records]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{record_id}", response_model=AllergyHistory)
async def update_allergy_history(record_id: str, ah: AllergyHistory):
    """Update allergy history record"""
    try:
        ah_dict = ah.model_dump(by_alias=True, exclude_unset=True)
        updated_record = await allergy_history_service.update(record_id, ah_dict)
        if not updated_record:
            raise HTTPException(status_code=404, detail="Allergy history record not found")
        return AllergyHistory(**updated_record)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{record_id}")
async def delete_allergy_history(record_id: str):
    """Delete allergy history record"""
    try:
        deleted = await allergy_history_service.delete(record_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Allergy history record not found")
        return {"message": "Allergy history record deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
