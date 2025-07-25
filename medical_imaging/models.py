from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from enum import Enum


class TestType(str, Enum):
    """Types of medical tests"""
    BLOOD_TEST = "blood_test"
    URINE_TEST = "urine_test"
    X_RAY = "x_ray"
    CT_SCAN = "ct_scan"
    MRI = "mri"
    ULTRASOUND = "ultrasound"
    ECG = "ecg"
    PATHOLOGY = "pathology"
    MICROBIOLOGY = "microbiology"
    OTHER = "other"


class ValueStatus(str, Enum):
    """Status of lab values"""
    NORMAL = "normal"
    HIGH = "high"
    LOW = "low"
    CRITICAL = "critical"
    ABNORMAL = "abnormal"
    UNKNOWN = "unknown"


class LabValue(BaseModel):
    """Individual laboratory value extracted from image"""
    parameter_name: str = Field(..., description="Name of the parameter (e.g., 'Hemoglobin', 'Glucose')")
    value: Union[str, float, int] = Field(..., description="Measured value")
    unit: Optional[str] = Field(None, description="Unit of measurement (e.g., 'mg/dL', 'g/L')")
    reference_range: Optional[str] = Field(None, description="Normal reference range")
    status: ValueStatus = Field(ValueStatus.UNKNOWN, description="Status of the value")
    notes: Optional[str] = Field(None, description="Additional notes about the value")


class TestResult(BaseModel):
    """Structured test result extracted from medical image"""
    test_name: str = Field(..., description="Name of the test")
    test_type: TestType = Field(TestType.OTHER, description="Type of medical test")
    test_date: Optional[datetime] = Field(None, description="Date when test was performed")
    patient_info: Optional[Dict[str, str]] = Field(None, description="Patient information if visible")
    lab_values: List[LabValue] = Field(default_factory=list, description="Individual lab values")
    findings: List[str] = Field(default_factory=list, description="Key findings or observations")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations if any")
    overall_assessment: Optional[str] = Field(None, description="Overall assessment or summary")
    confidence_score: float = Field(0.0, ge=0.0, le=1.0, description="AI confidence in extraction")


class ImageAnalysisMetadata(BaseModel):
    """Metadata about the image analysis process"""
    image_format: str = Field(..., description="Format of the uploaded image")
    image_size: int = Field(..., description="Size of image in bytes")
    processing_time: float = Field(..., description="Time taken to process in seconds")
    model_version: str = Field(..., description="Version of AI model used")
    extraction_quality: str = Field(..., description="Quality of text extraction (high/medium/low)")
    detected_language: str = Field(default="zh", description="Detected language in image")


class MedicalImageAnalysisRequest(BaseModel):
    """Request model for medical image analysis"""
    test_id: Optional[str] = Field(None, description="ID of the test record")
    patient_id: Optional[str] = Field(None, description="ID of the patient")
    expected_test_type: Optional[TestType] = Field(None, description="Expected type of test")
    analysis_context: Optional[str] = Field(None, description="Additional context for analysis")


class MedicalImageAnalysisResponse(BaseModel):
    """Response model for medical image analysis"""
    success: bool = Field(..., description="Whether analysis was successful")
    analysis_id: str = Field(..., description="Unique ID for this analysis")
    test_results: List[TestResult] = Field(default_factory=list, description="Extracted test results")
    raw_text: Optional[str] = Field(None, description="Raw OCR text extracted from image")
    metadata: ImageAnalysisMetadata = Field(..., description="Analysis metadata")
    error_message: Optional[str] = Field(None, description="Error message if analysis failed")
    suggested_actions: List[str] = Field(default_factory=list, description="Suggested next steps")


class ImageProcessingStatus(BaseModel):
    """Status model for tracking image processing"""
    analysis_id: str = Field(..., description="Unique analysis ID")
    status: str = Field(..., description="Current processing status")
    progress: int = Field(..., ge=0, le=100, description="Processing progress percentage")
    estimated_completion: Optional[datetime] = Field(None, description="Estimated completion time")
    current_step: str = Field(..., description="Current processing step")


class BatchImageAnalysisRequest(BaseModel):
    """Request model for batch processing multiple images"""
    images: List[Dict[str, Any]] = Field(..., description="List of image data")
    batch_context: Optional[str] = Field(None, description="Context for the entire batch")
    processing_priority: int = Field(1, ge=1, le=5, description="Processing priority (1=highest)")


class BatchImageAnalysisResponse(BaseModel):
    """Response model for batch image analysis"""
    batch_id: str = Field(..., description="Unique batch ID")
    total_images: int = Field(..., description="Total number of images in batch")
    completed_analyses: List[MedicalImageAnalysisResponse] = Field(default_factory=list)
    failed_analyses: List[Dict[str, str]] = Field(default_factory=list)
    batch_summary: Dict[str, Any] = Field(default_factory=dict, description="Summary of batch results") 