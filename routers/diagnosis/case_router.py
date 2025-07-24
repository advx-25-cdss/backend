from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from models.dianosis_models import Case
from services.diagnosis_service import case_service
from datetime import datetime

router = APIRouter(prefix="/cases", tags=["Cases"])

@router.post("/", response_model=dict)
async def create_case(case: Case):
    """Create a new case"""
    try:
        case_dict = case.dict()
        created_case = await case_service.create(case_dict)
        return {"message": "Case created successfully", "data": created_case}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating case: {str(e)}")

@router.get("/{case_id}", response_model=dict)
async def get_case_by_id(case_id: str):
    """Get a case by ID"""
    case = await case_service.get_by_id(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return {"data": case}

@router.get("/", response_model=dict)
async def get_cases(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    patient_id: Optional[str] = Query(None, description="Filter by patient ID"),
    status: Optional[str] = Query(None, description="Filter by case status"),
    case_number: Optional[str] = Query(None, description="Filter by case number")
):
    """Get all cases with optional filtering"""
    try:
        # Build query based on filters
        query = {}
        if patient_id:
            query["patient_id"] = patient_id
        if status:
            query["status"] = status
        if case_number:
            query["case_number"] = case_number

        if query:
            cases = await case_service.search(query, skip, limit)
            total = await case_service.count(query)
        else:
            cases = await case_service.get_all(skip, limit)
            total = await case_service.count()

        return {
            "data": cases,
            "total": total,
            "skip": skip,
            "limit": limit
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving cases: {str(e)}")

@router.get("/patient/{patient_id}", response_model=dict)
async def get_cases_by_patient(patient_id: str):
    """Get all cases for a specific patient"""
    try:
        cases = await case_service.get_by_patient_id(patient_id)
        return {"data": cases, "count": len(cases)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving patient cases: {str(e)}")

@router.put("/{case_id}", response_model=dict)
async def update_case(case_id: str, case_update: dict):
    """Update a case"""
    try:
        # Check if case exists
        existing_case = await case_service.get_by_id(case_id)
        if not existing_case:
            raise HTTPException(status_code=404, detail="Case not found")

        # Update the case
        updated_case = await case_service.update(case_id, case_update)
        return {"message": "Case updated successfully", "data": updated_case}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating case: {str(e)}")

@router.patch("/{case_id}/status", response_model=dict)
async def update_case_status(case_id: str, status: str):
    """Update case status"""
    try:
        # Validate status
        valid_statuses = ['open', 'closed', 'in_progress']
        if status not in valid_statuses:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
            )

        # Check if case exists
        existing_case = await case_service.get_by_id(case_id)
        if not existing_case:
            raise HTTPException(status_code=404, detail="Case not found")

        # Update only the status
        updated_case = await case_service.update(case_id, {"status": status})
        return {"message": f"Case status updated to '{status}'", "data": updated_case}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating case status: {str(e)}")

@router.delete("/{case_id}", response_model=dict)
async def delete_case(case_id: str):
    """Delete a case"""
    try:
        # Check if case exists
        existing_case = await case_service.get_by_id(case_id)
        if not existing_case:
            raise HTTPException(status_code=404, detail="Case not found")

        # Delete the case
        deleted = await case_service.delete(case_id)
        if deleted:
            return {"message": "Case deleted successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to delete case")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting case: {str(e)}")

@router.get("/search/", response_model=dict)
async def search_cases(
    q: str = Query(..., description="Search query"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """Search cases by SOAP notes, case number, or notes"""
    try:
        # Create a text search query
        query = {
            "$or": [
                {"soap": {"$regex": q, "$options": "i"}},
                {"case_number": {"$regex": q, "$options": "i"}},
                {"notes": {"$regex": q, "$options": "i"}},
                {"transcriptions": {"$regex": q, "$options": "i"}}
            ]
        }

        cases = await case_service.search(query, skip, limit)
        total = await case_service.count(query)

        return {
            "data": cases,
            "total": total,
            "query": q,
            "skip": skip,
            "limit": limit
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching cases: {str(e)}")
