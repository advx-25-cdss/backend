from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from models.dianosis_models import Treatment
from services.diagnosis_service import DiagnosisService
from datetime import datetime

# Create service instance for treatments
treatment_service = DiagnosisService("treatments")

router = APIRouter(prefix="/treatments", tags=["Treatments"])

@router.post("/", response_model=dict)
async def create_treatment(treatment: Treatment):
    """Create a new treatment"""
    try:
        treatment_dict = treatment.dict()
        created_treatment = await treatment_service.create(treatment_dict)
        return {"message": "Treatment created successfully", "data": created_treatment}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating treatment: {str(e)}")

@router.get("/{treatment_id}", response_model=dict)
async def get_treatment_by_id(treatment_id: str):
    """Get a treatment by ID"""
    treatment = await treatment_service.get_by_id(treatment_id)
    if not treatment:
        raise HTTPException(status_code=404, detail="Treatment not found")
    return {"data": treatment}

@router.get("/", response_model=dict)
async def get_treatments(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    patient_id: Optional[str] = Query(None, description="Filter by patient ID"),
    case_id: Optional[str] = Query(None, description="Filter by case ID"),
    treatment_name: Optional[str] = Query(None, description="Filter by treatment name"),
    treatment_type: Optional[str] = Query(None, description="Filter by treatment type"),
    outcome: Optional[str] = Query(None, description="Filter by outcome")
):
    """Get all treatments with optional filtering"""
    try:
        # Build query based on filters
        query = {}
        if patient_id:
            query["patient_id"] = patient_id
        if case_id:
            query["case_id"] = case_id
        if treatment_name:
            query["treatment_name"] = {"$regex": treatment_name, "$options": "i"}
        if treatment_type:
            query["treatment_type"] = treatment_type
        if outcome:
            query["outcome"] = {"$regex": outcome, "$options": "i"}

        if query:
            treatments = await treatment_service.search(query, skip, limit)
            total = await treatment_service.count(query)
        else:
            treatments = await treatment_service.get_all(skip, limit)
            total = await treatment_service.count()

        return {
            "data": treatments,
            "total": total,
            "skip": skip,
            "limit": limit
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving treatments: {str(e)}")

@router.get("/patient/{patient_id}", response_model=dict)
async def get_treatments_by_patient(patient_id: str):
    """Get all treatments for a specific patient"""
    try:
        treatments = await treatment_service.get_by_patient_id(patient_id)
        return {"data": treatments, "count": len(treatments)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving patient treatments: {str(e)}")

@router.get("/case/{case_id}", response_model=dict)
async def get_treatments_by_case(case_id: str):
    """Get all treatments for a specific case"""
    try:
        treatments = await treatment_service.get_by_case_id(case_id)
        return {"data": treatments, "count": len(treatments)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving case treatments: {str(e)}")

@router.get("/types/summary", response_model=dict)
async def get_treatment_types_summary(patient_id: Optional[str] = None):
    """Get summary of treatment types"""
    try:
        query = {}
        if patient_id:
            query["patient_id"] = patient_id

        # Aggregate treatment types
        pipeline = [
            {"$match": query},
            {"$group": {
                "_id": "$treatment_type",
                "count": {"$sum": 1},
                "treatments": {"$push": {
                    "treatment_id": "$_id",
                    "treatment_name": "$treatment_name",
                    "treatment_date": "$treatment_date",
                    "outcome": "$outcome"
                }}
            }},
            {"$sort": {"count": -1}}
        ]

        # Note: This is a simplified aggregation. In production, you'd use MongoDB's aggregation pipeline
        all_treatments = await treatment_service.search(query, 0, 1000)

        # Group by treatment type manually
        summary = {}
        for treatment in all_treatments:
            t_type = treatment.get("treatment_type", "unknown")
            if t_type not in summary:
                summary[t_type] = {
                    "count": 0,
                    "treatments": []
                }
            summary[t_type]["count"] += 1
            summary[t_type]["treatments"].append({
                "treatment_id": treatment["_id"],
                "treatment_name": treatment["treatment_name"],
                "treatment_date": treatment["treatment_date"],
                "outcome": treatment.get("outcome")
            })

        return {"data": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting treatment summary: {str(e)}")

@router.put("/{treatment_id}", response_model=dict)
async def update_treatment(treatment_id: str, treatment_update: dict):
    """Update a treatment"""
    try:
        # Check if treatment exists
        existing_treatment = await treatment_service.get_by_id(treatment_id)
        if not existing_treatment:
            raise HTTPException(status_code=404, detail="Treatment not found")

        # Update the treatment
        updated_treatment = await treatment_service.update(treatment_id, treatment_update)
        return {"message": "Treatment updated successfully", "data": updated_treatment}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating treatment: {str(e)}")

@router.patch("/{treatment_id}/outcome", response_model=dict)
async def update_treatment_outcome(treatment_id: str, outcome: str):
    """Update treatment outcome"""
    try:
        # Check if treatment exists
        existing_treatment = await treatment_service.get_by_id(treatment_id)
        if not existing_treatment:
            raise HTTPException(status_code=404, detail="Treatment not found")

        # Update only the outcome
        updated_treatment = await treatment_service.update(treatment_id, {"outcome": outcome})
        return {"message": f"Treatment outcome updated", "data": updated_treatment}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating treatment outcome: {str(e)}")

@router.delete("/{treatment_id}", response_model=dict)
async def delete_treatment(treatment_id: str):
    """Delete a treatment"""
    try:
        # Check if treatment exists
        existing_treatment = await treatment_service.get_by_id(treatment_id)
        if not existing_treatment:
            raise HTTPException(status_code=404, detail="Treatment not found")

        # Delete the treatment
        deleted = await treatment_service.delete(treatment_id)
        if deleted:
            return {"message": "Treatment deleted successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to delete treatment")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting treatment: {str(e)}")

@router.get("/search/", response_model=dict)
async def search_treatments(
    q: str = Query(..., description="Search query"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """Search treatments by name, outcome, or notes"""
    try:
        # Create a text search query
        query = {
            "$or": [
                {"treatment_name": {"$regex": q, "$options": "i"}},
                {"outcome": {"$regex": q, "$options": "i"}},
                {"notes": {"$regex": q, "$options": "i"}},
                {"treatment_type": {"$regex": q, "$options": "i"}}
            ]
        }

        treatments = await treatment_service.search(query, skip, limit)
        total = await treatment_service.count(query)

        return {
            "data": treatments,
            "total": total,
            "query": q,
            "skip": skip,
            "limit": limit
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching treatments: {str(e)}")
