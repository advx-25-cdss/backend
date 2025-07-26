from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from models.dianosis_models import Medicine
from services.diagnosis_service import medicine_service
from datetime import datetime

router = APIRouter(prefix="/medicines", tags=["Medicines"])


@router.post("/", response_model=dict)
async def create_medicine(medicine: Medicine):
    """Create a new medicine prescription"""
    try:
        medicine_dict = medicine.model_dump()
        created_medicine = await medicine_service.create(medicine_dict)
        return {"message": "Medicine created successfully", "data": created_medicine}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error creating medicine: {str(e)}"
        )


@router.get("/{medicine_id}", response_model=dict)
async def get_medicine_by_id(medicine_id: str):
    """Get a medicine by ID"""
    medicine = await medicine_service.get_by_id(medicine_id)
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return {"data": medicine}


@router.get("/", response_model=dict)
async def get_medicines(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    patient_id: Optional[str] = Query(None, description="Filter by patient ID"),
    case_id: Optional[str] = Query(None, description="Filter by case ID"),
    medicine_name: Optional[str] = Query(None, description="Filter by medicine name"),
    route: Optional[str] = Query(None, description="Filter by administration route"),
    active_only: bool = Query(False, description="Show only active prescriptions"),
):
    """Get all medicines with optional filtering"""
    try:
        # Build query based on filters
        query = {}
        if patient_id:
            query["patient_id"] = patient_id
        if case_id:
            query["case_id"] = case_id
        if medicine_name:
            query["medicine_name"] = {"$regex": medicine_name, "$options": "i"}
        if route:
            query["route"] = route
        if active_only:
            # Show only medicines without end_date or end_date in future
            current_time = datetime.now()
            query["$or"] = [{"end_date": None}, {"end_date": {"$gt": current_time}}]

        if query:
            medicines = await medicine_service.search(query, skip, limit)
            total = await medicine_service.count(query)
        else:
            medicines = await medicine_service.get_all(skip, limit)
            total = await medicine_service.count()

        return {"data": medicines, "total": total, "skip": skip, "limit": limit}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving medicines: {str(e)}"
        )


@router.get("/patient/{patient_id}", response_model=dict)
async def get_medicines_by_patient(
    patient_id: str,
    active_only: bool = Query(False, description="Show only active prescriptions"),
):
    """Get all medicines for a specific patient"""
    try:
        medicines = await medicine_service.get_by_patient_id(patient_id)

        if active_only:
            # Filter for active prescriptions
            current_time = datetime.now()
            medicines = [
                med
                for med in medicines
                if med.get("end_date") is None or med.get("end_date") > current_time
            ]

        return {"data": medicines, "count": len(medicines)}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving patient medicines: {str(e)}"
        )


@router.get("/case/{case_id}", response_model=dict)
async def get_medicines_by_case(case_id: str):
    """Get all medicines for a specific case"""
    try:
        medicines = await medicine_service.get_by_case_id(case_id)
        return {"data": medicines, "count": len(medicines)}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving case medicines: {str(e)}"
        )


@router.put("/{medicine_id}", response_model=dict)
async def update_medicine(medicine_id: str, medicine_update: dict):
    """Update a medicine prescription"""
    try:
        # Check if medicine exists
        existing_medicine = await medicine_service.get_by_id(medicine_id)
        if not existing_medicine:
            raise HTTPException(status_code=404, detail="Medicine not found")

        # Update the medicine
        updated_medicine = await medicine_service.update(medicine_id, medicine_update)
        return {"message": "Medicine updated successfully", "data": updated_medicine}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error updating medicine: {str(e)}"
        )


@router.patch("/{medicine_id}/discontinue", response_model=dict)
async def discontinue_medicine(medicine_id: str, end_date: Optional[datetime] = None):
    """Discontinue a medicine prescription"""
    try:
        # Check if medicine exists
        existing_medicine = await medicine_service.get_by_id(medicine_id)
        if not existing_medicine:
            raise HTTPException(status_code=404, detail="Medicine not found")

        # Set end date to now if not provided
        if end_date is None:
            end_date = datetime.now()

        # Update medicine with end date
        updated_medicine = await medicine_service.update(
            medicine_id, {"end_date": end_date}
        )
        return {
            "message": "Medicine discontinued successfully",
            "data": updated_medicine,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error discontinuing medicine: {str(e)}"
        )


@router.patch("/{medicine_id}/reactivate", response_model=dict)
async def reactivate_medicine(medicine_id: str):
    """Reactivate a discontinued medicine prescription"""
    try:
        # Check if medicine exists
        existing_medicine = await medicine_service.get_by_id(medicine_id)
        if not existing_medicine:
            raise HTTPException(status_code=404, detail="Medicine not found")

        # Remove end date to reactivate
        updated_medicine = await medicine_service.update(
            medicine_id, {"end_date": None}
        )
        return {
            "message": "Medicine reactivated successfully",
            "data": updated_medicine,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error reactivating medicine: {str(e)}"
        )


@router.delete("/{medicine_id}", response_model=dict)
async def delete_medicine(medicine_id: str):
    """Delete a medicine prescription"""
    try:
        # Check if medicine exists
        existing_medicine = await medicine_service.get_by_id(medicine_id)
        if not existing_medicine:
            raise HTTPException(status_code=404, detail="Medicine not found")

        # Delete the medicine
        deleted = await medicine_service.delete(medicine_id)
        if deleted:
            return {"message": "Medicine deleted successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to delete medicine")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error deleting medicine: {str(e)}"
        )


@router.get("/interactions/check", response_model=dict)
async def check_drug_interactions(patient_id: str):
    """Check for potential drug interactions for a patient's active medications"""
    try:
        # Get all active medicines for the patient
        medicines = await medicine_service.get_by_patient_id(patient_id)
        current_time = datetime.now()
        active_medicines = [
            med
            for med in medicines
            if med.get("end_date") is None or med.get("end_date") > current_time
        ]

        # Simple interaction check (in real implementation, this would use a drug interaction database)
        interactions = []
        medicine_names = [med["medicine_name"].lower() for med in active_medicines]

        # Example interaction checks (expand with real drug interaction logic)
        known_interactions = {
            ("warfarin", "aspirin"): "Increased bleeding risk",
            ("metformin", "contrast dye"): "Risk of lactic acidosis",
            ("digoxin", "furosemide"): "Increased digoxin toxicity risk",
        }

        for i, med1 in enumerate(medicine_names):
            for med2 in medicine_names[i + 1 :]:
                interaction_key = tuple(sorted([med1, med2]))
                if interaction_key in known_interactions:
                    interactions.append(
                        {
                            "medicine1": med1,
                            "medicine2": med2,
                            "interaction": known_interactions[interaction_key],
                        }
                    )

        return {
            "patient_id": patient_id,
            "active_medicines": active_medicines,
            "interactions": interactions,
            "interaction_count": len(interactions),
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error checking drug interactions: {str(e)}"
        )


@router.get("/search/", response_model=dict)
async def search_medicines(
    q: str = Query(..., description="Search query"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
):
    """Search medicines by name, dosage, or notes"""
    try:
        # Create a text search query
        query = {
            "$or": [
                {"medicine_name": {"$regex": q, "$options": "i"}},
                {"dosage": {"$regex": q, "$options": "i"}},
                {"frequency": {"$regex": q, "$options": "i"}},
                {"notes": {"$regex": q, "$options": "i"}},
            ]
        }

        medicines = await medicine_service.search(query, skip, limit)
        total = await medicine_service.count(query)

        return {
            "data": medicines,
            "total": total,
            "query": q,
            "skip": skip,
            "limit": limit,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error searching medicines: {str(e)}"
        )
