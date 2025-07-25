"""
Medical Imaging Module

This module provides AI-powered medical image analysis capabilities,
including structured extraction of test results from medical images.
"""

__version__ = "1.0.0"
__author__ = "Medical AI System"

from .models import (
    MedicalImageAnalysisRequest,
    MedicalImageAnalysisResponse,
    TestResult,
    LabValue,
    ImageAnalysisMetadata
)

from .service import MedicalImageAnalysisService
from .router import router

__all__ = [
    "MedicalImageAnalysisRequest",
    "MedicalImageAnalysisResponse", 
    "TestResult",
    "LabValue",
    "ImageAnalysisMetadata",
    "MedicalImageAnalysisService",
    "router"
] 