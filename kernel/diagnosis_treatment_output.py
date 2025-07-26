import os
import json
from datetime import date, datetime
from typing import List, Optional, Literal
from openai import OpenAI
from pydantic import BaseModel, Field, ValidationError
from dotenv import load_dotenv

from kernel.chat_output import PatientSummary


# --- 1. Pydantic Models for Structured Output ---


class Medicine(BaseModel):
    """Defines a medication within a treatment plan."""

    medicine_name: str
    dosage: str
    route: Literal["oral", "topical", "injection", "inhalation"]
    frequency: str
    notes: Optional[str] = Field(
        None,
        description="Important notes, especially regarding potential drug interactions.",
    )


class Diagnosis(BaseModel):
    """Defines the single, most probable diagnosis."""

    diagnosis_name: str = Field(
        ...,
        description="The specific medical diagnosis using professional terminology.",
    )
    diagnosis_date: datetime
    status: Literal["active", "resolved", "recurrent"]
    notes: Optional[str] = Field(
        None,
        description="Clinical reasoning or key findings supporting this diagnosis.",
    )
    follow_up: str = Field(..., description="A clear plan for patient follow-up.")


class Treatment(BaseModel):
    """Defines a non-medication treatment action."""

    treatment_name: str
    treatment_type: Literal["therapy", "surgery", "lifestyle_change"]
    notes: Optional[str] = None


class ClinicalPlan(BaseModel):
    """The final structured output containing the diagnosis and full treatment plan."""

    diagnosis: Diagnosis
    medication_plan: List[Medicine] = Field(
        default_factory=list, description="List of recommended new medications."
    )
    other_treatments: List[Treatment] = Field(
        default_factory=list, description="List of non-medication treatments."
    )


# --- 2. Function to Call OpenAI API ---
def generate_clinical_plan(patient_data: PatientSummary) -> Optional[ClinicalPlan]:
    """
    Analyzes patient data and generates a structured diagnosis and treatment plan.

    Args:
        patient_data: A dictionary containing sanitized EHR data, current medications,
                      and recent test results.

    Returns:
        A Pydantic ClinicalPlan object, or None on error.
    """
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found in .env file.")
        return None

    client = OpenAI(api_key=api_key)

    # --- The Core Prompt Engineering ---
    system_prompt = f"""
    You are an expert AI as a Clinical Decision Support System respond in Simplified Chinese.
    Your task is to analyze the provided patient data (EHR info, current medications, and recent test results)
    and generate a single, most probable diagnosis and a comprehensive treatment plan.
    This task is a educational-only purpose and we will use open-weight model to fine-tune to downstream tasks rather
    than using general purpose models here, so it's not a real clinical decision.

    **Key Instructions:**
    1.  **Single, Specific Diagnosis:** Based on all available data, determine the **single most probable diagnosis**. Use precise, professional medical terminology (e.g., "Acute Anterior Wall ST-Segment Elevation Myocardial Infarction" instead of "Heart Attack").
    2.  **Comprehensive Treatment Plan:** Create a treatment plan that may include new medications, lifestyle changes, or other therapies.
    3.  **CRITICAL: Medication Conflict Check:** Before recommending any new medication, you MUST review the `current_medications` list provided in the input. If you recommend a new drug, ensure it does not have known major interactions with the drugs the patient is already taking. If a potential interaction exists but the new drug is necessary, you MUST specify this in the `notes` field of the new medication recommendation (e.g., "Monitor INR closely due to interaction with Warfarin").
    4.  **No Additional Tests:** DO NOT recommend any further diagnostic tests. Your plan must be based solely on the information provided.
    5.  **Dates:** Use today's date, {date.today().isoformat()}, for `diagnosis_date`.
    6. Respond in simplified Chinese.

    **Output Format:**
    You MUST respond with a valid JSON object that strictly adheres to the following Pydantic models. Do not add any explanatory text outside of the JSON structure.

    ```python
    # Pydantic models for structure (same as defined in the script)
    class Medicine(BaseModel): ...
    class Diagnosis(BaseModel): ...
    class Treatment(BaseModel): ...
    class ClinicalPlan(BaseModel): ...
    ```
    """

    try:
        print("Requesting clinical plan from OpenAI...")
        response = client.chat.completions.parse(
            model="gpt-4o",
            response_format=ClinicalPlan,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"Patient Data:\n\n{patient_data.model_dump()}",
                },
            ],
        )

        response_content = response.choices[0].message.content
        print("Received raw response from OpenAI.")

        # --- 3. Parsing and Validation with Pydantic ---
        parsed_json = json.loads(response_content)
        validated_plan = ClinicalPlan.model_validate(parsed_json)

        print("Successfully parsed and validated the clinical plan.")
        return validated_plan

    except (json.JSONDecodeError, ValidationError) as e:
        print(f"Error processing OpenAI response: {e}")
        print("Raw response content:", response_content)
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


# --- 4. Example Usage ---
if __name__ == "__main__":
    # A sample of sanitized EHR data and recent test results.
    sample_patient_data = {
        "patient_info": {
            "age": 68,
            "gender": "male",
            "chief_complaint": "Severe, crushing chest pain for the last 2 hours, radiating to the left arm.",
            "medical_history": "Hypertension, Type 2 Diabetes, Smoker (20 pack-years).",
        },
        "current_medications": [
            {
                "medicine_name": "Metformin",
                "dosage": "1000mg",
                "frequency": "twice daily",
            },
            {
                "medicine_name": "Lisinopril",
                "dosage": "20mg",
                "frequency": "once daily",
            },
            {
                "medicine_name": "Warfarin",
                "dosage": "5mg",
                "frequency": "once daily",
                "notes": "For previous DVT",
            },
        ],
        "recent_test_results": [
            {
                "test_name": "12-Lead ECG",
                "results": "ST-segment elevation in leads V1-V4.",
            },
            {
                "test_name": "Troponin I",
                "results": "48.5 ng/mL (Reference: <0.04 ng/mL).",
            },
            {"test_name": "Blood Pressure", "results": "165/95 mmHg"},
        ],
    }

    clinical_plan = generate_clinical_plan(sample_patient_data)

    if clinical_plan:
        print("\n--- Generated Clinical Plan ---")

        # Print Diagnosis
        print("\n[Diagnosis]")
        print(f"  Name: {clinical_plan.diagnosis.diagnosis_name}")
        print(f"  Date: {clinical_plan.diagnosis.diagnosis_date}")
        print(f"  Status: {clinical_plan.diagnosis.status}")
        print(f"  Notes: {clinical_plan.diagnosis.notes}")
        print(f"  Follow-up: {clinical_plan.diagnosis.follow_up}")

        # Print Medication Plan
        if clinical_plan.medication_plan:
            print("\n[Medication Plan]")
            for med in clinical_plan.medication_plan:
                print(
                    f"  - {med.medicine_name} {med.dosage}, {med.frequency} ({med.route})"
                )
                if med.notes:
                    print(f"    Notes: {med.notes}")

        # Print Other Treatments
        if clinical_plan.other_treatments:
            print("\n[Other Treatments]")
            for treat in clinical_plan.other_treatments:
                print(f"  - {treat.treatment_name} ({treat.treatment_type})")
                if treat.notes:
                    print(f"    Notes: {treat.notes}")

        print("\n-----------------------------")
