"""
Medical Image Analysis Service

This module provides the core business logic for analyzing medical images
and extracting structured test results using AI models.
"""

import uuid
import time
import json
import tempfile
import os
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime
from PIL import Image, ImageEnhance
import pytesseract
import cv2
import numpy as np

from .models import (
    MedicalImageAnalysisResponse,
    TestResult,
    LabValue,
    ImageAnalysisMetadata,
    TestType,
    ValueStatus
)
from .prompts import MedicalImagePrompts

# For AI integration - using OpenAI as an example
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# For image processing
try:
    import easyocr
    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False


class MedicalImageAnalysisService:
    """Service for analyzing medical images and extracting structured results"""
    
    def __init__(self, 
                 ocr_languages: List[str] = ['zh', 'en'],
                 model_version: str = "v1.0.0"):
        """
        Initialize the medical image analysis service
        
        Args:
            ocr_languages: Languages for OCR processing
            model_version: Version identifier for the analysis model
        """
        self.ocr_languages = ocr_languages
        self.model_version = model_version
        
        # Initialize OCR engine
        if EASYOCR_AVAILABLE:
            self.ocr_reader = easyocr.Reader(ocr_languages)
        else:
            self.ocr_reader = None
            print("Warning: EasyOCR not available, falling back to Tesseract")
        
        # Initialize AI client if available
        self.ai_client = None
        if OPENAI_AVAILABLE:
            # Note: In production, use environment variables for API keys
            pass
    
    async def analyze_medical_image(self, 
                                  image_data: bytes,
                                  image_format: str,
                                  analysis_request: Optional[Dict[str, Any]] = None) -> MedicalImageAnalysisResponse:
        """
        Analyze a medical image and extract structured test results
        
        Args:
            image_data: Raw image bytes
            image_format: Format of the image (jpg, png, etc.)
            analysis_request: Optional analysis parameters
            
        Returns:
            MedicalImageAnalysisResponse with extracted results
        """
        start_time = time.time()
        analysis_id = str(uuid.uuid4())
        
        try:
            # Step 1: Preprocess image
            processed_image = await self._preprocess_image(image_data)
            
            # Step 2: Extract text using OCR
            ocr_result = await self._extract_text_from_image(processed_image)
            raw_text = ocr_result["text"]
            extraction_quality = ocr_result["quality"]
            
            # Step 3: Analyze text with AI to extract structured data
            test_results = await self._analyze_text_with_ai(
                raw_text, 
                analysis_request or {}
            )
            
            # Step 4: Validate and post-process results
            validated_results = await self._validate_results(test_results)
            
            # Step 5: Create metadata
            processing_time = time.time() - start_time
            metadata = ImageAnalysisMetadata(
                image_format=image_format,
                image_size=len(image_data),
                processing_time=processing_time,
                model_version=self.model_version,
                extraction_quality=extraction_quality,
                detected_language="zh"  # Could be detected automatically
            )
            
            # Step 6: Generate suggested actions
            suggested_actions = self._generate_suggested_actions(validated_results)
            
            return MedicalImageAnalysisResponse(
                success=True,
                analysis_id=analysis_id,
                test_results=validated_results,
                raw_text=raw_text,
                metadata=metadata,
                suggested_actions=suggested_actions
            )
            
        except Exception as e:
            processing_time = time.time() - start_time
            
            return MedicalImageAnalysisResponse(
                success=False,
                analysis_id=analysis_id,
                test_results=[],
                raw_text="",
                metadata=ImageAnalysisMetadata(
                    image_format=image_format,
                    image_size=len(image_data),
                    processing_time=processing_time,
                    model_version=self.model_version,
                    extraction_quality="failed",
                    detected_language="unknown"
                ),
                error_message=str(e),
                suggested_actions=["请检查图像质量并重新上传", "确保图像中的文本清晰可读"]
            )
    
    async def _preprocess_image(self, image_data: bytes) -> Image.Image:
        """
        Preprocess image to improve OCR accuracy
        
        Args:
            image_data: Raw image bytes
            
        Returns:
            Preprocessed PIL Image
        """
        # Convert bytes to PIL Image
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(image_data)
            temp_file.flush()
            
            # Load image
            image = Image.open(temp_file.name)
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Enhance image for better OCR
            # Increase contrast
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.5)
            
            # Increase sharpness
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(2.0)
            
            # Clean up temp file
            os.unlink(temp_file.name)
            
            return image
    
    async def _extract_text_from_image(self, image: Image.Image) -> Dict[str, Any]:
        """
        Extract text from image using OCR
        
        Args:
            image: Preprocessed PIL Image
            
        Returns:
            Dictionary with extracted text and quality metrics
        """
        try:
            if self.ocr_reader and EASYOCR_AVAILABLE:
                # Use EasyOCR for better multilingual support
                # Convert PIL to numpy array
                img_array = np.array(image)
                
                # Extract text
                results = self.ocr_reader.readtext(img_array)
                
                # Combine all text with confidence scores
                text_parts = []
                confidence_scores = []
                
                for (bbox, text, confidence) in results:
                    if confidence > 0.3:  # Filter low-confidence text
                        text_parts.append(text)
                        confidence_scores.append(confidence)
                
                combined_text = "\n".join(text_parts)
                avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
                
                quality = "high" if avg_confidence > 0.8 else "medium" if avg_confidence > 0.5 else "low"
                
            else:
                # Fallback to Tesseract
                # Save image temporarily for Tesseract
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                    image.save(temp_file.name)
                    
                    # Configure Tesseract for medical text
                    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz一二三四五六七八九十.,:;()[]{}+-=<>/%'
                    
                    combined_text = pytesseract.image_to_string(
                        Image.open(temp_file.name), 
                        lang='chi_sim+eng',
                        config=custom_config
                    )
                    
                    os.unlink(temp_file.name)
                    quality = "medium"  # Tesseract quality estimation
            
            return {
                "text": combined_text.strip(),
                "quality": quality
            }
            
        except Exception as e:
            print(f"OCR extraction failed: {e}")
            return {
                "text": "",
                "quality": "failed"
            }
    
    async def _analyze_text_with_ai(self, text: str, context: Dict[str, Any]) -> List[TestResult]:
        """
        Use AI to analyze extracted text and create structured results
        
        Args:
            text: Raw OCR text
            context: Analysis context and parameters
            
        Returns:
            List of structured TestResult objects
        """
        if not text.strip():
            return []
        
        try:
            # Determine test type from context or text analysis
            expected_test_type = context.get("expected_test_type", "other")
            
            # Get appropriate prompt
            prompt = MedicalImagePrompts.get_structured_extraction_prompt(expected_test_type)
            
            # For demonstration purposes, create a mock analysis
            # In production, this would use a real AI service like OpenAI GPT-4V
            mock_result = await self._mock_ai_analysis(text, expected_test_type)
            
            return [mock_result] if mock_result else []
            
        except Exception as e:
            print(f"AI analysis failed: {e}")
            return []
    
    async def _mock_ai_analysis(self, text: str, test_type: str) -> Optional[TestResult]:
        """
        Mock AI analysis for demonstration purposes
        In production, replace with actual AI service calls
        """
        # Parse common patterns in medical test text
        lab_values = []
        findings = []
        
        # Simple pattern matching for common test values
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Look for numeric values with units
            if any(char.isdigit() for char in line):
                # Try to identify lab values
                if '血红蛋白' in line or 'Hb' in line or 'HGB' in line:
                    lab_values.append(LabValue(
                        parameter_name="血红蛋白 (Hemoglobin)",
                        value="12.5",
                        unit="g/dL",
                        reference_range="12.0-15.5",
                        status=ValueStatus.NORMAL,
                        notes="正常范围内"
                    ))
                elif '白细胞' in line or 'WBC' in line:
                    lab_values.append(LabValue(
                        parameter_name="白细胞 (White Blood Cells)",
                        value="7.2",
                        unit="×10³/μL",
                        reference_range="4.0-10.0",
                        status=ValueStatus.NORMAL
                    ))
                elif '血糖' in line or 'GLU' in line or 'Glucose' in line:
                    lab_values.append(LabValue(
                        parameter_name="血糖 (Glucose)",
                        value="5.8",
                        unit="mmol/L",
                        reference_range="3.9-6.1",
                        status=ValueStatus.NORMAL
                    ))
            
            # Look for findings
            if any(keyword in line for keyword in ['异常', '偏高', '偏低', '正常', '阴性', '阳性']):
                findings.append(line)
        
        # Create a mock test result
        return TestResult(
            test_name="血液常规检查" if test_type == "blood_test" else "医学检查",
            test_type=TestType(test_type) if test_type in [t.value for t in TestType] else TestType.OTHER,
            test_date=datetime.now(),
            lab_values=lab_values,
            findings=findings[:5],  # Limit findings
            overall_assessment="检查结果在正常范围内" if lab_values else "需要进一步分析",
            confidence_score=0.85 if lab_values else 0.60
        )
    
    async def _validate_results(self, results: List[TestResult]) -> List[TestResult]:
        """
        Validate and clean up extracted results
        
        Args:
            results: Raw test results from AI analysis
            
        Returns:
            Validated and cleaned test results
        """
        validated_results = []
        
        for result in results:
            # Validate lab values
            validated_lab_values = []
            for lab_value in result.lab_values:
                # Basic validation
                if lab_value.parameter_name and lab_value.value:
                    validated_lab_values.append(lab_value)
            
            # Update result with validated values
            result.lab_values = validated_lab_values
            
            # Ensure confidence score is reasonable
            if result.confidence_score > 1.0:
                result.confidence_score = 1.0
            elif result.confidence_score < 0.0:
                result.confidence_score = 0.0
            
            validated_results.append(result)
        
        return validated_results
    
    def _generate_suggested_actions(self, results: List[TestResult]) -> List[str]:
        """
        Generate suggested actions based on analysis results
        
        Args:
            results: Analyzed test results
            
        Returns:
            List of suggested actions
        """
        suggestions = []
        
        if not results:
            suggestions.extend([
                "图像质量可能不够清晰，建议重新上传",
                "确保图像包含完整的检查报告信息"
            ])
            return suggestions
        
        for result in results:
            # Check for abnormal values
            abnormal_count = sum(1 for val in result.lab_values 
                               if val.status in [ValueStatus.HIGH, ValueStatus.LOW, ValueStatus.CRITICAL])
            
            if abnormal_count > 0:
                suggestions.append(f"发现 {abnormal_count} 项异常指标，建议咨询医生")
            
            # Check confidence score
            if result.confidence_score < 0.7:
                suggestions.append("AI分析置信度较低，建议人工复核结果")
            
            # Add general suggestions
            if result.lab_values:
                suggestions.append("建议将结果保存到患者病历中")
        
        if not suggestions:
            suggestions.append("检查结果已成功提取，可以保存到系统中")
        
        return list(set(suggestions))  # Remove duplicates 