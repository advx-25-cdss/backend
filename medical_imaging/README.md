# Medical Image Analysis Module

This module provides AI-powered medical image analysis capabilities for extracting structured test results from medical images such as blood tests, X-rays, CT scans, and other diagnostic images.

## 🎯 Features

-  **Multi-format Support**: Analyze JPEG, PNG, and other common image formats
-  **OCR Text Extraction**: Advanced OCR with Chinese and English support
-  **AI-Powered Analysis**: Structure extraction using language models
-  **Multiple Test Types**: Support for blood tests, urine tests, imaging studies, etc.
-  **Batch Processing**: Analyze multiple images simultaneously
-  **Quality Assessment**: Confidence scoring and extraction quality metrics
-  **Real-time Processing**: Fast analysis suitable for clinical workflows

## 📁 Module Structure

```
medical_imaging/
├── __init__.py              # Module initialization and exports
├── models.py                # Pydantic models for API contracts
├── prompts.py               # AI prompts for different test types
├── service.py               # Core business logic and AI integration
├── router.py                # FastAPI endpoints
├── integration_example.ts   # TypeScript integration examples
└── README.md               # This documentation
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file with optional AI service keys:

```env
OPENAI_API_KEY=your_openai_key_here  # Optional for production AI
AZURE_COGNITIVE_SERVICES_KEY=your_azure_key  # Optional
```

### 3. Start the Service

The medical imaging router is automatically included when you run the main FastAPI application:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Test the API

```bash
# Health check
curl http://localhost:8000/api/medical-imaging/health

# Analyze an image
curl -X POST -F "image=@test_blood_report.jpg" \
     -F "expected_test_type=blood_test" \
     http://localhost:8000/api/medical-imaging/analyze-image
```

## 📋 API Endpoints

### Core Analysis Endpoints

-  **POST `/analyze-image`** - Analyze a medical image
-  **GET `/analysis-status/{analysis_id}`** - Check analysis progress
-  **POST `/batch-analyze`** - Process multiple images
-  **GET `/supported-test-types`** - List supported test types

### Utility Endpoints

-  **GET `/health`** - Service health check
-  **GET `/analysis-history`** - Historical results (requires database)
-  **DELETE `/analysis/{analysis_id}`** - Delete analysis results
-  **POST `/validate-extraction`** - Validate extraction quality

## 🔧 Supported Test Types

| Test Type    | Code           | Description                           |
| ------------ | -------------- | ------------------------------------- |
| Blood Test   | `blood_test`   | CBC, chemistry panels, lipid profiles |
| Urine Test   | `urine_test`   | Routine urinalysis, microscopy        |
| X-Ray        | `x_ray`        | Chest X-rays, bone imaging            |
| CT Scan      | `ct_scan`      | Computed tomography reports           |
| MRI          | `mri`          | Magnetic resonance imaging            |
| Ultrasound   | `ultrasound`   | Sonography reports                    |
| ECG          | `ecg`          | Electrocardiogram analysis            |
| Pathology    | `pathology`    | Histopathology reports                |
| Microbiology | `microbiology` | Culture and sensitivity               |

## 💻 Frontend Integration

### React Hook Usage

```typescript
import { useMedicalImageAnalysis } from "./medical-imaging-integration";

function MyComponent() {
   const { analyzeTestImage } = useMedicalImageAnalysis();

   const handleImageUpload = async (file: File) => {
      const result = await analyzeTestImage("test-123", file, "blood_test");

      if (result.success) {
         console.log("Extracted results:", result.extractedResults);
         console.log("AI confidence:", result.confidence);
      }
   };
}
```

### Next.js API Route

Create `/app/api/medical-imaging/analyze/route.ts`:

```typescript
import { NextRequest, NextResponse } from "next/server";

const FASTAPI_BACKEND_URL =
   process.env.FASTAPI_BACKEND_URL || "http://localhost:8000";

export async function POST(request: NextRequest) {
   const formData = await request.formData();

   const response = await fetch(
      `${FASTAPI_BACKEND_URL}/api/medical-imaging/analyze-image`,
      {
         method: "POST",
         body: formData,
      }
   );

   return NextResponse.json(await response.json());
}
```

## 🤖 AI Integration

### OCR Engines

The module supports multiple OCR engines with automatic fallback:

1. **EasyOCR** (Primary) - Better multilingual support
2. **Tesseract** (Fallback) - Reliable text extraction

### Language Models

Currently supports:

-  **Mock Analysis** (Default) - Pattern-based extraction for development
-  **OpenAI GPT** (Optional) - Advanced AI analysis with API key
-  **Custom Models** - Extensible for domain-specific models

### Prompt Engineering

Specialized prompts for different test types are stored in `prompts.py`:

-  Medical terminology awareness
-  Chinese/English bilingual support
-  Context-specific extraction rules
-  Quality validation guidelines

## 📊 Response Format

### Successful Analysis

```json
{
   "success": true,
   "analysis_id": "uuid-string",
   "test_results": [
      {
         "test_name": "血液常规检查",
         "test_type": "blood_test",
         "test_date": "2024-01-15T10:30:00",
         "lab_values": [
            {
               "parameter_name": "血红蛋白 (Hemoglobin)",
               "value": "12.5",
               "unit": "g/dL",
               "reference_range": "12.0-15.5",
               "status": "normal",
               "notes": "正常范围内"
            }
         ],
         "findings": ["血红蛋白水平正常"],
         "recommendations": ["继续定期检查"],
         "overall_assessment": "检查结果在正常范围内",
         "confidence_score": 0.95
      }
   ],
   "metadata": {
      "image_format": "jpeg",
      "image_size": 524288,
      "processing_time": 2.34,
      "model_version": "v1.0.0",
      "extraction_quality": "high",
      "detected_language": "zh"
   },
   "suggested_actions": ["检查结果已成功提取，可以保存到系统中"]
}
```

## 🔧 Configuration

### Service Configuration

```python
# In your application startup
from medical_imaging import MedicalImageAnalysisService

service = MedicalImageAnalysisService(
    ocr_languages=['zh', 'en'],  # Supported languages
    model_version="v1.0.0"       # Version tracking
)
```

### Image Processing Settings

-  **Max file size**: 10MB
-  **Supported formats**: JPEG, PNG, TIFF, BMP
-  **OCR confidence threshold**: 0.3
-  **Processing timeout**: 30 seconds

## 🚧 Development Notes

### Mock Mode vs Production

The service includes a mock analysis mode for development:

-  **Mock Mode**: Pattern-based extraction for testing
-  **Production Mode**: Real AI model integration

### Extending the Service

1. **Add new test types**: Update `TestType` enum in `models.py`
2. **Custom prompts**: Add specialized prompts in `prompts.py`
3. **New AI models**: Extend the service class with additional providers

### Performance Optimization

-  Use batch processing for multiple images
-  Implement result caching for repeated analyses
-  Consider GPU acceleration for large-scale deployments

## 🧪 Testing

### Unit Tests

```bash
# Run medical imaging tests
pytest medical_imaging/tests/

# Test specific functionality
pytest -k "test_image_analysis"
```

### Integration Tests

```bash
# Test with sample images
curl -X POST -F "image=@samples/blood_test_sample.jpg" \
     http://localhost:8000/api/medical-imaging/analyze-image
```

## 🔒 Security Considerations

-  **File validation**: Strict image format checking
-  **Size limits**: Prevent large file uploads
-  **Input sanitization**: Clean OCR text before AI processing
-  **Rate limiting**: Implement request throttling for production

## 📈 Monitoring & Logging

The service includes comprehensive logging:

-  Analysis performance metrics
-  OCR quality scores
-  AI confidence levels
-  Error tracking and debugging

## 🤝 Contributing

1. Follow the existing code structure
2. Add tests for new functionality
3. Update documentation for API changes
4. Consider performance implications

## 📄 License

This module is part of the medical EHR system and follows the same licensing terms.

---

For questions or support, please refer to the main project documentation or contact the development team.
