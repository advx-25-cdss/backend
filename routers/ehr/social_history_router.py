from fastapi import APIRouter, HTTPException, Query
from typing import List
from models.ehr_models import SocialHistory
from services.ehr_service import social_history_service

router = APIRouter()


@router.post("/", response_model=SocialHistory)
async def create_social_history(sh: SocialHistory):
    """Create new social history record"""
    try:
        sh_dict = sh.model_dump(by_alias=True, exclude_unset=True)
        created_record = await social_history_service.create(sh_dict)
        return SocialHistory(**created_record)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{record_id}", response_model=SocialHistory)
async def get_social_history(record_id: str):
    """Get social history record by ID"""
    try:
        record = await social_history_service.get_by_id(record_id)
        if not record:
            raise HTTPException(
                status_code=404, detail="Social history record not found"
            )
        return SocialHistory(**record)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/patient/{patient_id}", response_model=List[SocialHistory])
async def get_social_history_by_patient(patient_id: str):
    """Get all social history records for a specific patient"""
    try:
        records = await social_history_service.get_by_patient_id(patient_id)
        return [SocialHistory(**record) for record in records]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[SocialHistory])
async def get_all_social_history(
    skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000)
):
    """Get all social history records with pagination"""
    try:
        records = await social_history_service.get_all(skip=skip, limit=limit)
        return [SocialHistory(**record) for record in records]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{record_id}", response_model=SocialHistory)
async def update_social_history(record_id: str, sh: SocialHistory):
    """Update social history record"""
    try:
        sh_dict = sh.dict(by_alias=True, exclude_unset=True)
        updated_record = await social_history_service.update(record_id, sh_dict)
        if not updated_record:
            raise HTTPException(
                status_code=404, detail="Social history record not found"
            )
        return SocialHistory(**updated_record)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{record_id}")
async def delete_social_history(record_id: str):
    """Delete social history record"""
    try:
        deleted = await social_history_service.delete(record_id)
        if not deleted:
            raise HTTPException(
                status_code=404, detail="Social history record not found"
            )
        return {"message": "Social history record deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
