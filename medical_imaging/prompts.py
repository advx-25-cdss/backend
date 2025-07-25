"""
AI Prompts for Medical Image Analysis

This module contains structured prompts for analyzing medical images
and extracting structured test results.
"""

from typing import Dict, Any


class MedicalImagePrompts:
    """Collection of prompts for medical image analysis"""
    
    @staticmethod
    def get_base_analysis_prompt() -> str:
        """Base prompt for medical image analysis"""
        return """
You are an expert medical AI assistant specializing in analyzing medical test images and extracting structured information.

Your task is to analyze the provided medical image and extract all relevant test results, lab values, and medical information in a structured format.

IMPORTANT GUIDELINES:
1. Extract ALL visible test parameters, values, units, and reference ranges
2. Identify the type of medical test (blood test, urine test, X-ray, etc.)
3. Note any abnormal values and their clinical significance
4. Maintain high accuracy - only extract information you can clearly see
5. If text is unclear or ambiguous, note this in your response
6. Pay attention to Chinese medical terminology and units
7. Preserve the original language of medical terms when appropriate

EXTRACTION FOCUS:
- Patient information (name, ID, age, gender if visible)
- Test date and time
- Laboratory values with units and reference ranges
- Abnormal findings and their significance
- Overall assessment or diagnosis if present
- Recommendations or follow-up instructions

OUTPUT FORMAT: Provide a structured JSON response with the extracted information.
"""

    @staticmethod
    def get_blood_test_prompt() -> str:
        """Specific prompt for blood test analysis"""
        return MedicalImagePrompts.get_base_analysis_prompt() + """

BLOOD TEST SPECIFIC INSTRUCTIONS:
- Focus on complete blood count (CBC), biochemistry panels, lipid profiles
- Extract values for: hemoglobin, white blood cells, platelets, glucose, cholesterol, etc.
- Identify critical values that require immediate attention
- Note the testing laboratory and methodology if visible
- Pay attention to fasting status indicators
- Extract liver function, kidney function, and metabolic panel results

Common Chinese Blood Test Terms:
- 血红蛋白 (Hemoglobin) - Hb/HGB
- 白细胞 (White Blood Cells) - WBC
- 血小板 (Platelets) - PLT
- 血糖 (Glucose) - GLU
- 胆固醇 (Cholesterol) - CHOL
- 肝功能 (Liver Function)
- 肾功能 (Kidney Function)
"""

    @staticmethod
    def get_urine_test_prompt() -> str:
        """Specific prompt for urine test analysis"""
        return MedicalImagePrompts.get_base_analysis_prompt() + """

URINE TEST SPECIFIC INSTRUCTIONS:
- Extract routine urine analysis parameters
- Focus on: protein, glucose, blood cells, bacteria, specific gravity
- Note microscopic examination results
- Identify infection indicators or abnormal findings
- Extract quantitative values where available

Common Chinese Urine Test Terms:
- 尿蛋白 (Urine Protein) - PRO
- 尿糖 (Urine Glucose) - GLU
- 红细胞 (Red Blood Cells) - RBC
- 白细胞 (White Blood Cells) - WBC
- 细菌 (Bacteria) - BAC
- 比重 (Specific Gravity) - SG
"""

    @staticmethod
    def get_imaging_test_prompt() -> str:
        """Specific prompt for medical imaging (X-ray, CT, MRI, etc.)"""
        return MedicalImagePrompts.get_base_analysis_prompt() + """

MEDICAL IMAGING SPECIFIC INSTRUCTIONS:
- Extract radiologist findings and impressions
- Note anatomical structures examined
- Identify abnormalities, lesions, or pathological findings
- Extract measurements and dimensions if provided
- Note imaging technique and contrast usage
- Focus on diagnostic conclusions and recommendations

Common Chinese Imaging Terms:
- 正常 (Normal)
- 异常 (Abnormal)
- 病变 (Lesion/Pathological change)
- 影像学表现 (Imaging findings)
- 印象 (Impression)
- 建议 (Recommendations)
"""

    @staticmethod
    def get_pathology_test_prompt() -> str:
        """Specific prompt for pathology test analysis"""
        return MedicalImagePrompts.get_base_analysis_prompt() + """

PATHOLOGY TEST SPECIFIC INSTRUCTIONS:
- Extract histopathological findings
- Note tissue type and specimen source
- Identify cellular abnormalities or malignancies
- Extract immunohistochemistry results if present
- Focus on diagnostic conclusions and staging
- Note any molecular markers or genetic findings

Common Chinese Pathology Terms:
- 病理诊断 (Pathological Diagnosis)
- 镜下所见 (Microscopic Findings)
- 免疫组化 (Immunohistochemistry)
- 恶性 (Malignant)
- 良性 (Benign)
"""

    @staticmethod
    def get_ecg_test_prompt() -> str:
        """Specific prompt for ECG/EKG analysis"""
        return MedicalImagePrompts.get_base_analysis_prompt() + """

ECG SPECIFIC INSTRUCTIONS:
- Extract heart rate, rhythm, and intervals
- Note any arrhythmias or conduction abnormalities
- Identify ST-segment changes or T-wave abnormalities
- Extract axis deviations and chamber enlargements
- Focus on clinical interpretation and recommendations

Common Chinese ECG Terms:
- 心率 (Heart Rate) - HR
- 心律 (Heart Rhythm)
- 窦性心律 (Sinus Rhythm)
- 心电图 (Electrocardiogram)
- 异常 Q 波 (Abnormal Q waves)
"""

    @staticmethod
    def get_structured_extraction_prompt(test_type: str = "general") -> str:
        """Get structured extraction prompt based on test type"""
        
        base_prompt = MedicalImagePrompts.get_base_analysis_prompt()
        
        specific_prompts = {
            "blood_test": MedicalImagePrompts.get_blood_test_prompt(),
            "urine_test": MedicalImagePrompts.get_urine_test_prompt(),
            "x_ray": MedicalImagePrompts.get_imaging_test_prompt(),
            "ct_scan": MedicalImagePrompts.get_imaging_test_prompt(),
            "mri": MedicalImagePrompts.get_imaging_test_prompt(),
            "ultrasound": MedicalImagePrompts.get_imaging_test_prompt(),
            "ecg": MedicalImagePrompts.get_ecg_test_prompt(),
            "pathology": MedicalImagePrompts.get_pathology_test_prompt(),
        }
        
        return specific_prompts.get(test_type, base_prompt) + """

FINAL INSTRUCTIONS:
Analyze the image thoroughly and provide a JSON response with the following structure:
{
    "test_name": "Name of the test",
    "test_type": "Type of test (blood_test, urine_test, etc.)",
    "test_date": "Date of test if visible (YYYY-MM-DD format)",
    "patient_info": {
        "name": "Patient name if visible",
        "id": "Patient ID if visible",
        "age": "Age if visible",
        "gender": "Gender if visible"
    },
    "lab_values": [
        {
            "parameter_name": "Parameter name",
            "value": "Measured value",
            "unit": "Unit of measurement",
            "reference_range": "Normal range",
            "status": "normal|high|low|critical|abnormal",
            "notes": "Additional notes"
        }
    ],
    "findings": ["Key finding 1", "Key finding 2"],
    "recommendations": ["Recommendation 1", "Recommendation 2"],
    "overall_assessment": "Overall summary of results",
    "confidence_score": 0.95
}

Ensure high accuracy and only extract information you can clearly identify in the image.
"""

    @staticmethod
    def get_quality_check_prompt() -> str:
        """Prompt for checking extraction quality"""
        return """
Review the extracted medical test results and assess the quality of extraction:

1. COMPLETENESS: Are all visible parameters extracted?
2. ACCURACY: Are the values and units correctly transcribed?
3. CONSISTENCY: Are the findings consistent with the lab values?
4. CLINICAL RELEVANCE: Are abnormal findings properly identified?
5. FORMATTING: Is the output properly structured?

Provide quality score (0.0-1.0) and improvement suggestions.
"""

    @staticmethod
    def get_validation_prompt(extracted_data: Dict[str, Any]) -> str:
        """Prompt for validating extracted data"""
        return f"""
Validate the following extracted medical test data for clinical accuracy and completeness:

EXTRACTED DATA:
{extracted_data}

VALIDATION CHECKLIST:
1. Are the lab values within plausible ranges?
2. Do the units match the parameters?
3. Are reference ranges typical for the tests?
4. Are abnormal findings clinically significant?
5. Is the overall assessment consistent with individual values?

Provide validation score and flag any potential errors or inconsistencies.
""" 