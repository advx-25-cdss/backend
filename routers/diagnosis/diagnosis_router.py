from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from models.dianosis_models import Diagnosis
from services.diagnosis_service import DiagnosisService
from datetime import datetime

# Create service instance for diagnoses
diagnosis_service = DiagnosisService("diagnoses")

router = APIRouter(prefix="/diagnoses", tags=["Diagnoses"])

@router.post("/", response_model=dict)
async def create_diagnosis(diagnosis: Diagnosis):
    """Create a new diagnosis"""
    try:
        diagnosis_dict = diagnosis.dict()
        created_diagnosis = await diagnosis_service.create(diagnosis_dict)
        return {"message": "Diagnosis created successfully", "data": created_diagnosis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating diagnosis: {str(e)}")

@router.get("/{diagnosis_id}", response_model=dict)
async def get_diagnosis_by_id(diagnosis_id: str):
    """Get a diagnosis by ID"""
    diagnosis = await diagnosis_service.get_by_id(diagnosis_id)
    if not diagnosis:
        raise HTTPException(status_code=404, detail="Diagnosis not found")
    return {"data": diagnosis}

@router.get("/", response_model=dict)
async def get_diagnoses(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    patient_id: Optional[str] = Query(None, description="Filter by patient ID"),
    case_id: Optional[str] = Query(None, description="Filter by case ID"),
    diagnosis_name: Optional[str] = Query(None, description="Filter by diagnosis name"),
    status: Optional[str] = Query(None, description="Filter by diagnosis status"),
    active_only: bool = Query(False, description="Show only active diagnoses")
):
    """Get all diagnoses with optional filtering"""
    try:
        # Build query based on filters
        query = {}
        if patient_id:
            query["patient_id"] = patient_id
        if case_id:
            query["case_id"] = case_id
        if diagnosis_name:
            query["diagnosis_name"] = {"$regex": diagnosis_name, "$options": "i"}
        if status:
            query["status"] = status
        if active_only:
            query["status"] = "active"

        if query:
            diagnoses = await diagnosis_service.search(query, skip, limit)
            total = await diagnosis_service.count(query)
        else:
            diagnoses = await diagnosis_service.get_all(skip, limit)
            total = await diagnosis_service.count()

        return {
            "data": diagnoses,
            "total": total,
            "skip": skip,
            "limit": limit
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving diagnoses: {str(e)}")

@router.get("/patient/{patient_id}", response_model=dict)
async def get_diagnoses_by_patient(
    patient_id: str,
    active_only: bool = Query(False, description="Show only active diagnoses")
):
    """Get all diagnoses for a specific patient"""
    try:
        diagnoses = await diagnosis_service.get_by_patient_id(patient_id)

        if active_only:
            diagnoses = [d for d in diagnoses if d.get("status") == "active"]

        return {"data": diagnoses, "count": len(diagnoses)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving patient diagnoses: {str(e)}")

@router.get("/case/{case_id}", response_model=dict)
async def get_diagnoses_by_case(case_id: str):
    """Get all diagnoses for a specific case"""
    try:
        diagnoses = await diagnosis_service.get_by_case_id(case_id)
        return {"data": diagnoses, "count": len(diagnoses)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving case diagnoses: {str(e)}")

@router.get("/statistics/", response_model=dict)
async def get_diagnosis_statistics(
    patient_id: Optional[str] = Query(None, description="Filter by patient ID"),
    start_date: Optional[datetime] = Query(None, description="Start date for statistics"),
    end_date: Optional[datetime] = Query(None, description="End date for statistics")
):
    """Get diagnosis statistics and summary"""
    try:
        query = {}
        if patient_id:
            query["patient_id"] = patient_id
        if start_date or end_date:
            date_query = {}
            if start_date:
                date_query["$gte"] = start_date
            if end_date:
                date_query["$lte"] = end_date
            query["diagnosis_date"] = date_query

        all_diagnoses = await diagnosis_service.search(query, 0, 1000)

        # Calculate statistics
        stats = {
            "total_diagnoses": len(all_diagnoses),
            "active_count": len([d for d in all_diagnoses if d.get("status") == "active"]),
            "resolved_count": len([d for d in all_diagnoses if d.get("status") == "resolved"]),
            "recurrent_count": len([d for d in all_diagnoses if d.get("status") == "recurrent"]),
            "by_status": {},
            "common_diagnoses": {}
        }

        # Group by status
        for diagnosis in all_diagnoses:
            status = diagnosis.get("status", "unknown")
            name = diagnosis.get("diagnosis_name", "unknown")

            if status not in stats["by_status"]:
                stats["by_status"][status] = []
            stats["by_status"][status].append({
                "diagnosis_id": diagnosis["_id"],
                "diagnosis_name": name,
                "diagnosis_date": diagnosis["diagnosis_date"]
            })

            # Count common diagnoses
            if name not in stats["common_diagnoses"]:
                stats["common_diagnoses"][name] = 0
            stats["common_diagnoses"][name] += 1

        # Sort common diagnoses by frequency
        stats["common_diagnoses"] = dict(
            sorted(stats["common_diagnoses"].items(), key=lambda x: x[1], reverse=True)
        )

        return {"data": stats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting diagnosis statistics: {str(e)}")

@router.put("/{diagnosis_id}", response_model=dict)
async def update_diagnosis(diagnosis_id: str, diagnosis_update: dict):
    """Update a diagnosis"""
    try:
        # Check if diagnosis exists
        existing_diagnosis = await diagnosis_service.get_by_id(diagnosis_id)
        if not existing_diagnosis:
            raise HTTPException(status_code=404, detail="Diagnosis not found")

        # Update the diagnosis
        updated_diagnosis = await diagnosis_service.update(diagnosis_id, diagnosis_update)
        return {"message": "Diagnosis updated successfully", "data": updated_diagnosis}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating diagnosis: {str(e)}")

@router.patch("/{diagnosis_id}/status", response_model=dict)
async def update_diagnosis_status(diagnosis_id: str, status: str):
    """Update diagnosis status"""
    try:
        # Validate status
        valid_statuses = ['active', 'resolved', 'recurrent']
        if status not in valid_statuses:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
            )

        # Check if diagnosis exists
        existing_diagnosis = await diagnosis_service.get_by_id(diagnosis_id)
        if not existing_diagnosis:
            raise HTTPException(status_code=404, detail="Diagnosis not found")

        # Update only the status
        updated_diagnosis = await diagnosis_service.update(diagnosis_id, {"status": status})
        return {"message": f"Diagnosis status updated to '{status}'", "data": updated_diagnosis}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating diagnosis status: {str(e)}")

@router.patch("/{diagnosis_id}/follow-up", response_model=dict)
async def update_diagnosis_follow_up(diagnosis_id: str, follow_up: str):
    """Update diagnosis follow-up information"""
    try:
        # Check if diagnosis exists
        existing_diagnosis = await diagnosis_service.get_by_id(diagnosis_id)
        if not existing_diagnosis:
            raise HTTPException(status_code=404, detail="Diagnosis not found")

        # Update follow-up
        updated_diagnosis = await diagnosis_service.update(diagnosis_id, {"follow_up": follow_up})
        return {"message": "Diagnosis follow-up updated", "data": updated_diagnosis}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating diagnosis follow-up: {str(e)}")

@router.delete("/{diagnosis_id}", response_model=dict)
async def delete_diagnosis(diagnosis_id: str):
    """Delete a diagnosis"""
    try:
        # Check if diagnosis exists
        existing_diagnosis = await diagnosis_service.get_by_id(diagnosis_id)
        if not existing_diagnosis:
            raise HTTPException(status_code=404, detail="Diagnosis not found")

        # Delete the diagnosis
        deleted = await diagnosis_service.delete(diagnosis_id)
        if deleted:
            return {"message": "Diagnosis deleted successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to delete diagnosis")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting diagnosis: {str(e)}")

@router.get("/search/", response_model=dict)
async def search_diagnoses(
    q: str = Query(..., description="Search query"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """Search diagnoses by name, follow-up, or notes"""
    try:
        # Create a text search query
        query = {
            "$or": [
                {"diagnosis_name": {"$regex": q, "$options": "i"}},
                {"follow_up": {"$regex": q, "$options": "i"}},
                {"notes": {"$regex": q, "$options": "i"}},
                {"additional_info": {"$regex": q, "$options": "i"}}
            ]
        }

        diagnoses = await diagnosis_service.search(query, skip, limit)
        total = await diagnosis_service.count(query)

        return {
            "data": diagnoses,
            "total": total,
            "query": q,
            "skip": skip,
            "limit": limit
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching diagnoses: {str(e)}")
