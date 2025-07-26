from fastapi import APIRouter, HTTPException, Query
from typing import List
from models.ehr_models import HistoryPresentIllness
from services.ehr_service import history_present_illness_service

router = APIRouter()


@router.post("/", response_model=HistoryPresentIllness)
async def create_history_present_illness(hpi: HistoryPresentIllness):
    """Create new history of present illness record"""
    try:
        hpi_dict = hpi.model_dump(by_alias=True, exclude_unset=True)
        created_record = await history_present_illness_service.create(hpi_dict)
        return HistoryPresentIllness(**created_record)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{record_id}", response_model=HistoryPresentIllness)
async def get_history_present_illness(record_id: str):
    """Get history of present illness record by ID"""
    try:
        record = await history_present_illness_service.get_by_id(record_id)
        if not record:
            raise HTTPException(
                status_code=404, detail="History of present illness record not found"
            )
        return HistoryPresentIllness(**record)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/patient/{patient_id}", response_model=List[HistoryPresentIllness])
async def get_history_present_illness_by_patient(patient_id: str):
    """Get all history of present illness records for a specific patient"""
    try:
        records = await history_present_illness_service.get_by_patient_id(patient_id)
        return [HistoryPresentIllness(**record) for record in records]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[HistoryPresentIllness])
async def get_all_history_present_illness(
    skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000)
):
    """Get all history of present illness records with pagination"""
    try:
        records = await history_present_illness_service.get_all(skip=skip, limit=limit)
        return [HistoryPresentIllness(**record) for record in records]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{record_id}", response_model=HistoryPresentIllness)
async def update_history_present_illness(record_id: str, hpi: HistoryPresentIllness):
    """Update history of present illness record"""
    try:
        hpi_dict = hpi.dict(by_alias=True, exclude_unset=True)
        updated_record = await history_present_illness_service.update(
            record_id, hpi_dict
        )
        if not updated_record:
            raise HTTPException(
                status_code=404, detail="History of present illness record not found"
            )
        return HistoryPresentIllness(**updated_record)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{record_id}")
async def delete_history_present_illness(record_id: str):
    """Delete history of present illness record"""
    try:
        deleted = await history_present_illness_service.delete(record_id)
        if not deleted:
            raise HTTPException(
                status_code=404, detail="History of present illness record not found"
            )
        return {"message": "History of present illness record deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
