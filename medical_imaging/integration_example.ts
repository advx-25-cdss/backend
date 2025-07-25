/**
 * Medical Image Analysis Integration Example
 *
 * This file demonstrates how to integrate the FastAPI medical image analysis
 * endpoints with the React frontend TestBlock component.
 */

// Types matching the backend models
interface LabValue {
   parameter_name: string;
   value: string | number;
   unit?: string;
   reference_range?: string;
   status: "normal" | "high" | "low" | "critical" | "abnormal" | "unknown";
   notes?: string;
}

interface TestResult {
   test_name: string;
   test_type: string;
   test_date?: string;
   patient_info?: {
      name?: string;
      id?: string;
      age?: string;
      gender?: string;
   };
   lab_values: LabValue[];
   findings: string[];
   recommendations: string[];
   overall_assessment?: string;
   confidence_score: number;
}

interface ImageAnalysisMetadata {
   image_format: string;
   image_size: number;
   processing_time: number;
   model_version: string;
   extraction_quality: "high" | "medium" | "low" | "failed";
   detected_language: string;
}

interface MedicalImageAnalysisResponse {
   success: boolean;
   analysis_id: string;
   test_results: TestResult[];
   raw_text?: string;
   metadata: ImageAnalysisMetadata;
   error_message?: string;
   suggested_actions: string[];
}

// API Configuration
const FASTAPI_BASE_URL =
   process.env.FASTAPI_BACKEND_URL || "http://localhost:8000";

/**
 * Medical Image Analysis Service
 *
 * Handles communication with the FastAPI backend for image analysis
 */
export class MedicalImageAnalysisService {
   private baseUrl: string;

   constructor(baseUrl: string = FASTAPI_BASE_URL) {
      this.baseUrl = baseUrl;
   }

   /**
    * Analyze a medical image and extract structured test results
    */
   async analyzeImage(
      imageFile: File,
      options: {
         testId?: string;
         patientId?: string;
         expectedTestType?: string;
         analysisContext?: string;
      } = {}
   ): Promise<MedicalImageAnalysisResponse> {
      const formData = new FormData();
      formData.append("image", imageFile);

      if (options.testId) formData.append("test_id", options.testId);
      if (options.patientId) formData.append("patient_id", options.patientId);
      if (options.expectedTestType)
         formData.append("expected_test_type", options.expectedTestType);
      if (options.analysisContext)
         formData.append("analysis_context", options.analysisContext);

      // use axios
      const response = await fetch(
         `${this.baseUrl}/api/medical-imaging/analyze-image`,
         {
            method: "POST",
            body: formData,
         }
      );

      if (!response.ok) {
         throw new Error(`Analysis failed: ${response.statusText}`);
      }

      return response.json();
   }

   /**
    * Get supported test types for optimized analysis
    */
   async getSupportedTestTypes(): Promise<{
      supported_types: Array<{
         value: string;
         label: string;
         description: string;
      }>;
   }> {
      const response = await fetch(
         `${this.baseUrl}/api/medical-imaging/supported-test-types`
      );

      if (!response.ok) {
         throw new Error(`Failed to get test types: ${response.statusText}`);
      }

      return response.json();
   }

   /**
    * Check service health and capabilities
    */
   async checkHealth(): Promise<any> {
      const response = await fetch(
         `${this.baseUrl}/api/medical-imaging/health`
      );
      return response.json();
   }
}

/**
 * React Hook for Medical Image Analysis
 *
 * Custom hook that integrates with the TestBlock component
 */
export function useMedicalImageAnalysis() {
   const service = new MedicalImageAnalysisService();

   const analyzeTestImage = async (
      testId: string,
      imageFile: File,
      expectedTestType?: string
   ): Promise<{
      success: boolean;
      extractedResults?: string[];
      confidence?: number;
      suggestions?: string[];
      error?: string;
   }> => {
      try {
         const result = await service.analyzeImage(imageFile, {
            testId,
            expectedTestType,
            analysisContext: "frontend_test_block",
         });

         if (result.success && result.test_results.length > 0) {
            const testResult = result.test_results[0];

            // Convert lab values to display format
            const extractedResults = testResult.lab_values.map(
               (lab) =>
                  `${lab.parameter_name}: ${lab.value}${
                     lab.unit ? " " + lab.unit : ""
                  } (${lab.status})`
            );

            // Add findings if available
            if (testResult.findings.length > 0) {
               extractedResults.push(
                  ...testResult.findings.map((finding) => `发现: ${finding}`)
               );
            }

            return {
               success: true,
               extractedResults,
               confidence: testResult.confidence_score,
               suggestions: result.suggested_actions,
            };
         } else {
            return {
               success: false,
               error: result.error_message || "图像分析失败，请检查图像质量",
            };
         }
      } catch (error) {
         return {
            success: false,
            error: error instanceof Error ? error.message : "网络错误，请重试",
         };
      }
   };

   return {
      analyzeTestImage,
      service,
   };
}

/**
 * Integration with TestBlock Component
 *
 * This function shows how to modify the handleImageUpload function
 * in the TestBlock component to use AI analysis
 */
export const enhancedImageUploadHandler = (
   useMedicalImageAnalysis: () => { analyzeTestImage: Function },
   onUpdateTest: (testId: string, updates: any) => void,
   setLoadingResults: (updates: any) => void
) => {
   const { analyzeTestImage } = useMedicalImageAnalysis();

   return async (testId: string, file: File) => {
      if (!file.type.startsWith("image/")) {
         alert("请选择图片文件");
         return;
      }

      if (file.size > 10 * 1024 * 1024) {
         alert("图片大小不能超过10MB");
         return;
      }

      // Set loading state
      setLoadingResults((prev: any) => ({ ...prev, [testId]: true }));

      try {
         // Analyze image with AI
         const analysisResult = await analyzeTestImage(
            testId,
            file,
            "blood_test"
         );

         if (analysisResult.success && analysisResult.extractedResults) {
            // Update test with extracted results
            onUpdateTest(testId, {
               results: analysisResult.extractedResults,
               notes: `AI分析置信度: ${(
                  analysisResult.confidence || 0 * 100
               ).toFixed(1)}%\n\n建议: ${
                  analysisResult.suggestions?.join("; ") || "无"
               }`,
            });

            // Show success message
            alert(
               `成功提取了 ${analysisResult.extractedResults.length} 项检查结果！`
            );
         } else {
            // Show error message
            alert(`图像分析失败: ${analysisResult.error}`);
         }
      } catch (error) {
         console.error("Image analysis error:", error);
         alert("图像分析过程中出现错误，请重试");
      } finally {
         // Clear loading state
         setLoadingResults((prev: any) => ({ ...prev, [testId]: false }));
      }
   };
};

/**
 * Next.js API Route Example
 *
 * Create this file as: /pages/api/medical-imaging/analyze.ts
 * or /app/api/medical-imaging/analyze/route.ts (App Router)
 */
export const nextJSApiRouteExample = `
import { NextRequest, NextResponse } from 'next/server';

const FASTAPI_BACKEND_URL = process.env.FASTAPI_BACKEND_URL || 'http://localhost:8000';

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData();
    
    // Forward the request to FastAPI backend
    const response = await fetch(\`\${FASTAPI_BACKEND_URL}/api/medical-imaging/analyze-image\`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error(\`FastAPI backend responded with \${response.status}\`);
    }

    const result = await response.json();
    return NextResponse.json(result);
  } catch (error) {
    console.error('Error forwarding to FastAPI backend:', error);
    return NextResponse.json(
      { error: 'Failed to analyze medical image' },
      { status: 500 }
    );
  }
}
`;

/**
 * Usage Example in TestBlock Component
 *
 * This shows how to modify the existing TestBlock component
 */
export const testBlockIntegrationExample = `
// Add this to your TestBlock component imports
import { useMedicalImageAnalysis, enhancedImageUploadHandler } from './medical-imaging-integration';

// Inside your TestBlock component
export function TestBlock({ tests, onAdd, onUpdate, onDelete }: TestBlockProps) {
  // ... existing state ...
  
  // Add medical image analysis hook
  const medicalAnalysis = useMedicalImageAnalysis();
  
  // Replace the existing handleImageUpload with enhanced version
  const handleImageUpload = enhancedImageUploadHandler(
    () => medicalAnalysis,
    onUpdate,
    setLoadingResults
  );

  // ... rest of component logic remains the same ...
}
`;

/**
 * Environment Variables
 *
 * Add these to your .env.local file:
 */
export const requiredEnvironmentVariables = `
# FastAPI Backend Configuration
FASTAPI_BACKEND_URL=http://localhost:8000

# Optional: AI Service Configuration
OPENAI_API_KEY=your_openai_api_key_here
AZURE_COGNITIVE_SERVICES_KEY=your_azure_key_here
`;

/**
 * Package Dependencies
 *
 * Add these to your package.json:
 */
export const requiredPackageDependencies = {
   dependencies: {
      // ... existing dependencies ...
   },
   devDependencies: {
      // Add TypeScript types if needed
      "@types/file-saver": "^2.0.5",
   },
};

// Export the service for use in components
export default MedicalImageAnalysisService;
