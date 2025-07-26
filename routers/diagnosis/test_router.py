from fastapi import APIRouter, HTTPException, Query, UploadFile, File
from typing import List, Optional
from models.dianosis_models import Test
from services.diagnosis_service import test_service
import base64

router = APIRouter(prefix="/tests", tags=["Tests"])


@router.post("/", response_model=dict)
async def create_test(test: Test):
    """Create a new test"""
    try:
        test_dict = test.model_dump()
        created_test = await test_service.create(test_dict)
        return {"message": "Test created successfully", "data": created_test}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating test: {str(e)}")


@router.post("/{test_id}/upload-results", response_model=dict)
async def upload_test_results(test_id: str, files: List[UploadFile] = File(...)):
    """Upload test result files"""
    try:
        # Check if test exists
        existing_test = await test_service.get_by_id(test_id)
        if not existing_test:
            raise HTTPException(status_code=404, detail="Test not found")

        # Process uploaded files
        results = []
        for file in files:
            # Read file content and encode to base64
            content = await file.read()
            encoded_content = base64.b64encode(content).decode("utf-8")

            # Store file info
            file_info = {
                "filename": file.filename,
                "content_type": file.content_type,
                "size": len(content),
                "data": encoded_content,
            }
            results.append(file_info)

        # Update test with results
        update_data = {"results": results}
        updated_test = await test_service.update(test_id, update_data)

        return {
            "message": f"Uploaded {len(files)} file(s) successfully",
            "data": updated_test,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading files: {str(e)}")


@router.get("/{test_id}", response_model=dict)
async def get_test_by_id(test_id: str):
    """Get a test by ID"""
    test = await test_service.get_by_id(test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    return {"data": test}


@router.get("/", response_model=dict)
async def get_tests(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    patient_id: Optional[str] = Query(None, description="Filter by patient ID"),
    case_id: Optional[str] = Query(None, description="Filter by case ID"),
    test_name: Optional[str] = Query(None, description="Filter by test name"),
):
    """Get all tests with optional filtering"""
    try:
        # Build query based on filters
        query = {}
        if patient_id:
            query["patient_id"] = patient_id
        if case_id:
            query["case_id"] = case_id
        if test_name:
            query["test_name"] = {"$regex": test_name, "$options": "i"}

        if query:
            tests = await test_service.search(query, skip, limit)
            total = await test_service.count(query)
        else:
            tests = await test_service.get_all(skip, limit)
            total = await test_service.count()

        return {"data": tests, "total": total, "skip": skip, "limit": limit}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving tests: {str(e)}")


@router.get("/patient/{patient_id}", response_model=dict)
async def get_tests_by_patient(patient_id: str):
    """Get all tests for a specific patient"""
    try:
        tests = await test_service.get_by_patient_id(patient_id)
        return {"data": tests, "count": len(tests)}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving patient tests: {str(e)}"
        )


@router.get("/case/{case_id}", response_model=dict)
async def get_tests_by_case(case_id: str):
    """Get all tests for a specific case"""
    try:
        tests = await test_service.get_by_case_id(case_id)
        return {"data": tests, "count": len(tests)}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving case tests: {str(e)}"
        )


@router.put("/{test_id}", response_model=dict)
async def update_test(test_id: str, test_update: dict):
    """Update a test"""
    try:
        # Check if test exists
        existing_test = await test_service.get_by_id(test_id)
        if not existing_test:
            raise HTTPException(status_code=404, detail="Test not found")

        # Update the test
        updated_test = await test_service.update(test_id, test_update)
        updated_test["_id"] = str(updated_test["_id"])  # Convert ObjectId to str
        return {"message": "Test updated successfully", "data": updated_test}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating test: {str(e)}")


@router.delete("/{test_id}", response_model=dict)
async def delete_test(test_id: str):
    """Delete a test"""
    try:
        # Check if test exists
        existing_test = await test_service.get_by_id(test_id)
        if not existing_test:
            raise HTTPException(status_code=404, detail="Test not found")

        # Delete the test
        deleted = await test_service.delete(test_id)
        if deleted:
            return {"message": "Test deleted successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to delete test")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting test: {str(e)}")


@router.get("/{test_id}/download-results", response_model=dict)
async def get_test_results(test_id: str):
    """Get test results files (as base64 encoded data)"""
    try:
        test = await test_service.get_by_id(test_id)
        if not test:
            raise HTTPException(status_code=404, detail="Test not found")

        if not test.get("results"):
            raise HTTPException(status_code=404, detail="No test results found")

        return {
            "message": "Test results retrieved successfully",
            "data": {"test_id": test_id, "results": test["results"]},
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving test results: {str(e)}"
        )


@router.delete("/{test_id}/results", response_model=dict)
async def delete_test_results(test_id: str):
    """Delete test result files"""
    try:
        # Check if test exists
        existing_test = await test_service.get_by_id(test_id)
        if not existing_test:
            raise HTTPException(status_code=404, detail="Test not found")

        # Remove results
        updated_test = await test_service.update(test_id, {"results": None})
        return {"message": "Test results deleted successfully", "data": updated_test}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error deleting test results: {str(e)}"
        )
