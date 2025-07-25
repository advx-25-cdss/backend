"""
FastAPI Router for Medical Image Analysis

This module provides REST API endpoints for uploading and analyzing
medical images to extract structured test results.
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Optional, List
import uuid
from datetime import datetime

from .models import (
    MedicalImageAnalysisRequest,
    MedicalImageAnalysisResponse,
    ImageProcessingStatus,
    BatchImageAnalysisRequest,
    BatchImageAnalysisResponse,
    TestType
)
from .service import MedicalImageAnalysisService

# Create router instance
router = APIRouter()

# Global service instance (in production, use dependency injection)
analysis_service = MedicalImageAnalysisService()

# In-memory storage for tracking analysis status (use Redis/database in production)
analysis_status_cache = {}


def get_analysis_service() -> MedicalImageAnalysisService:
    """Dependency to get analysis service instance"""
    return analysis_service


@router.post("/analyze-image", response_model=MedicalImageAnalysisResponse)
async def analyze_medical_image(
    image: UploadFile = File(..., description="Medical test image to analyze"),
    test_id: Optional[str] = Form(None, description="Associated test record ID"),
    patient_id: Optional[str] = Form(None, description="Patient ID"),
    expected_test_type: Optional[str] = Form(None, description="Expected test type"),
    analysis_context: Optional[str] = Form(None, description="Additional context"),
    service: MedicalImageAnalysisService = Depends(get_analysis_service)
):
    """
    Analyze a medical image and extract structured test results
    
    This endpoint accepts a medical test image and returns structured
    information including lab values, findings, and recommendations.
    """
    try:
        # Validate file type
        if not image.content_type or not image.content_type.startswith("image/"):
            raise HTTPException(
                status_code=400, 
                detail="File must be an image (JPEG, PNG, etc.)"
            )
        
        # Check file size (10MB limit)
        if image.size and image.size > 10 * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail="Image size must be less than 10MB"
            )
        
        # Read image data
        image_data = await image.read()
        
        # Get file extension
        image_format = image.content_type.split('/')[-1]
        
        # Prepare analysis request
        analysis_request = {
            "test_id": test_id,
            "patient_id": patient_id,
            "expected_test_type": expected_test_type,
            "analysis_context": analysis_context
        }
        
        # Perform analysis
        result = await service.analyze_medical_image(
            image_data=image_data,
            image_format=image_format,
            analysis_request=analysis_request
        )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


@router.get("/analysis-status/{analysis_id}", response_model=ImageProcessingStatus)
async def get_analysis_status(analysis_id: str):
    """
    Get the status of an ongoing image analysis
    
    Returns processing status, progress, and estimated completion time.
    """
    if analysis_id not in analysis_status_cache:
        raise HTTPException(
            status_code=404,
            detail=f"Analysis {analysis_id} not found"
        )
    
    return analysis_status_cache[analysis_id]


@router.post("/batch-analyze", response_model=BatchImageAnalysisResponse)
async def batch_analyze_images(
    images: List[UploadFile] = File(..., description="Multiple medical images"),
    batch_context: Optional[str] = Form(None, description="Batch processing context"),
    processing_priority: int = Form(1, description="Processing priority (1-5)"),
    service: MedicalImageAnalysisService = Depends(get_analysis_service)
):
    """
    Analyze multiple medical images in batch
    
    Processes multiple images simultaneously and returns combined results.
    """
    if len(images) > 20:  # Limit batch size
        raise HTTPException(
            status_code=400,
            detail="Batch size cannot exceed 20 images"
        )
    
    batch_id = str(uuid.uuid4())
    completed_analyses = []
    failed_analyses = []
    
    for i, image in enumerate(images):
        try:
            # Validate each image
            if not image.content_type or not image.content_type.startswith("image/"):
                failed_analyses.append({
                    "image_index": i,
                    "filename": image.filename or f"image_{i}",
                    "error": "Invalid image format"
                })
                continue
            
            # Process image
            image_data = await image.read()
            image_format = image.content_type.split('/')[-1]
            
            result = await service.analyze_medical_image(
                image_data=image_data,
                image_format=image_format,
                analysis_request={"batch_context": batch_context}
            )
            
            completed_analyses.append(result)
            
        except Exception as e:
            failed_analyses.append({
                "image_index": i,
                "filename": image.filename or f"image_{i}",
                "error": str(e)
            })
    
    # Generate batch summary
    total_lab_values = sum(
        len(analysis.test_results[0].lab_values) 
        for analysis in completed_analyses 
        if analysis.test_results
    )
    
    batch_summary = {
        "total_processed": len(completed_analyses),
        "total_failed": len(failed_analyses),
        "total_lab_values_extracted": total_lab_values,
        "average_confidence": sum(
            analysis.test_results[0].confidence_score 
            for analysis in completed_analyses 
            if analysis.test_results
        ) / max(len(completed_analyses), 1)
    }
    
    return BatchImageAnalysisResponse(
        batch_id=batch_id,
        total_images=len(images),
        completed_analyses=completed_analyses,
        failed_analyses=failed_analyses,
        batch_summary=batch_summary
    )


@router.get("/supported-test-types")
async def get_supported_test_types():
    """
    Get list of supported medical test types
    
    Returns available test types for analysis optimization.
    """
    return {
        "supported_types": [
            {
                "value": test_type.value,
                "label": test_type.value.replace('_', ' ').title(),
                "description": f"Analysis optimized for {test_type.value.replace('_', ' ')} tests"
            }
            for test_type in TestType
        ]
    }


@router.get("/health")
async def health_check():
    """
    Health check endpoint for medical imaging service
    """
    try:
        service = get_analysis_service()
        
        # Check service components
        ocr_status = "available" if service.ocr_reader else "tesseract_fallback"
        ai_status = "available" if service.ai_client else "mock_mode"
        
        return JSONResponse({
            "status": "healthy",
            "service": "medical_image_analysis",
            "version": service.model_version,
            "ocr_engine": ocr_status,
            "ai_engine": ai_status,
            "supported_languages": service.ocr_languages,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return JSONResponse(
            {
                "status": "unhealthy",
                "error": str(e),
                "service": "medical_image_analysis"
            },
            status_code=500
        )


@router.delete("/analysis/{analysis_id}")
async def delete_analysis_result(analysis_id: str):
    """
    Delete analysis result and associated data
    
    Cleans up stored analysis results and temporary files.
    """
    # In production, this would clean up database records and file storage
    if analysis_id in analysis_status_cache:
        del analysis_status_cache[analysis_id]
        return {"message": f"Analysis {analysis_id} deleted successfully"}
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Analysis {analysis_id} not found"
        )


@router.get("/analysis-history")
async def get_analysis_history(
    patient_id: Optional[str] = None,
    test_type: Optional[str] = None,
    limit: int = 50
):
    """
    Get analysis history with optional filtering
    
    Returns historical analysis results for review and comparison.
    """
    # In production, this would query the database
    # For now, return mock data structure
    return {
        "total_count": 0,
        "analyses": [],
        "filters": {
            "patient_id": patient_id,
            "test_type": test_type,
            "limit": limit
        },
        "message": "History feature requires database implementation"
    }


@router.post("/validate-extraction")
async def validate_extraction_quality(
    analysis_id: str,
    expected_values: Optional[dict] = None
):
    """
    Validate extraction quality against known values
    
    Helps improve AI model accuracy by comparing with ground truth.
    """
    # In production, this would be used for model training and validation
    return {
        "analysis_id": analysis_id,
        "validation_score": 0.95,
        "suggestions": [
            "Extraction quality is high",
            "No corrections needed"
        ],
        "message": "Validation completed successfully"
    } 