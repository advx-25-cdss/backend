"""
Mock diagnosis data for testing the Clinical Decision Support System.
This file contains mock cases, tests, medicines, diagnoses, and treatments for 20 patients.
"""

from datetime import datetime, timezone, timedelta
from bson import ObjectId
from models.dianosis_models import Case, Test, Medicine, Diagnosis, Treatment
import random


# Helper function to generate ObjectId strings
def generate_object_id():
    return str(ObjectId())


# Helper function to create patient IDs
def generate_patient_id(index):
    return f"PT{str(index).zfill(4)}"


# Sample SOAP notes for different medical conditions
SOAP_NOTES = [
    """S: 45-year-old female presents with chest pain that started 2 hours ago. Pain is sharp, 7/10 severity, located in the center of chest, radiating to left arm. Associated with shortness of breath and nausea.
O: BP 140/90, HR 88, RR 18, Temp 37.1°C, O2 Sat 96%. Patient appears anxious and diaphoretic. Heart sounds regular, no murmurs. Lungs clear bilaterally.
A: Acute chest pain, rule out acute coronary syndrome
P: ECG, cardiac enzymes, chest X-ray, aspirin 325mg, IV access established""",
    """S: 32-year-old male with 3-day history of fever, cough, and fatigue. Reports temperature up to 39°C at home. Dry cough, no sputum production. No shortness of breath at rest.
O: Temp 38.5°C, BP 110/70, HR 95, RR 16, O2 Sat 98%. Appears tired but not in distress. Throat erythematous, no exudate. Lungs clear to auscultation.
A: Viral upper respiratory infection
P: Supportive care, rest, fluids, acetaminophen for fever, return if worsening""",
    """S: 28-year-old female with 2-week history of polyuria, polydipsia, and unexplained weight loss (10 lbs). Family history of diabetes. Reports increased fatigue and blurred vision.
O: BP 125/80, HR 82, RR 14, Weight 130 lbs (down from 140). Random glucose 285 mg/dL. No ketones in urine.
A: New onset diabetes mellitus, likely Type 1
P: Endocrinology consult, diabetes education, insulin initiation, HbA1c, autoantibodies""",
    """S: 55-year-old male presents with severe abdominal pain that started 6 hours ago. Pain is constant, 9/10, located in epigastrium, radiating to back. Nausea and vomiting x3.
O: Temp 37.8°C, BP 150/95, HR 105, RR 20. Appears in significant distress. Abdomen tender in epigastrium, no rebound. Bowel sounds hypoactive.
A: Acute pancreatitis, rule out gallstone pancreatitis
P: NPO, IV fluids, pain control, lipase, amylase, CT abdomen, surgery consult""",
    """S: 38-year-old female with 1-week history of joint pain and morning stiffness lasting >1 hour. Bilateral hand and wrist pain, some swelling noted. Fatigue and low-grade fever.
O: Temp 37.5°C, BP 118/75, HR 78. Bilateral MCP and PIP joint swelling and tenderness. Limited range of motion in wrists.
A: Inflammatory arthritis, rule out rheumatoid arthritis
P: RF, anti-CCP, ESR, CRP, CBC, rheumatology referral, NSAIDs""",
]

# Generate mock cases for 20 patients
MOCK_CASES = []
MOCK_TESTS = []
MOCK_MEDICINES = []
MOCK_DIAGNOSES = []
MOCK_TREATMENTS = []

# Medical conditions with associated tests, medicines, diagnoses, and treatments
CONDITIONS = [
    {
        "soap": SOAP_NOTES[0],
        "status": "in_progress",
        "tests": ["ECG", "Troponin I", "CK-MB", "Chest X-ray"],
        "medicines": [
            {
                "name": "Aspirin",
                "dosage": "325mg",
                "route": "oral",
                "frequency": "once daily",
            },
            {
                "name": "Metoprolol",
                "dosage": "50mg",
                "route": "oral",
                "frequency": "twice daily",
            },
        ],
        "diagnoses": [
            {
                "name": "Acute Coronary Syndrome",
                "probability": 0.75,
                "status": "active",
            },
            {"name": "Unstable Angina", "probability": 0.60, "status": "active"},
        ],
        "treatments": [
            {"name": "Cardiac Catheterization", "type": "surgery"},
            {"name": "Dual Antiplatelet Therapy", "type": "medication"},
        ],
    },
    {
        "soap": SOAP_NOTES[1],
        "status": "closed",
        "tests": ["Rapid Strep Test", "CBC", "Throat Culture"],
        "medicines": [
            {
                "name": "Acetaminophen",
                "dosage": "650mg",
                "route": "oral",
                "frequency": "every 6 hours",
            },
        ],
        "diagnoses": [
            {
                "name": "Viral Upper Respiratory Infection",
                "probability": 0.90,
                "status": "resolved",
            }
        ],
        "treatments": [
            {"name": "Supportive Care", "type": "lifestyle_change"},
            {"name": "Rest and Hydration", "type": "lifestyle_change"},
        ],
    },
    {
        "soap": SOAP_NOTES[2],
        "status": "open",
        "tests": [
            "HbA1c",
            "Fasting Glucose",
            "C-peptide",
            "GAD Antibodies",
            "Urinalysis",
        ],
        "medicines": [
            {
                "name": "Insulin Lispro",
                "dosage": "10 units",
                "route": "injection",
                "frequency": "before meals",
            },
            {
                "name": "Metformin",
                "dosage": "500mg",
                "route": "oral",
                "frequency": "twice daily",
            },
        ],
        "diagnoses": [
            {
                "name": "Type 1 Diabetes Mellitus",
                "probability": 0.85,
                "status": "active",
            },
            {"name": "Diabetic Ketoacidosis", "probability": 0.30, "status": "active"},
        ],
        "treatments": [
            {"name": "Insulin Therapy Initiation", "type": "medication"},
            {"name": "Diabetes Education", "type": "therapy"},
        ],
    },
    {
        "soap": SOAP_NOTES[3],
        "status": "in_progress",
        "tests": ["Lipase", "Amylase", "CT Abdomen", "CBC", "Liver Function Tests"],
        "medicines": [
            {
                "name": "Morphine",
                "dosage": "4mg",
                "route": "injection",
                "frequency": "every 4 hours PRN",
            },
            {
                "name": "Ondansetron",
                "dosage": "4mg",
                "route": "injection",
                "frequency": "every 8 hours",
            },
        ],
        "diagnoses": [
            {"name": "Acute Pancreatitis", "probability": 0.80, "status": "active"},
            {"name": "Gallstone Pancreatitis", "probability": 0.65, "status": "active"},
        ],
        "treatments": [
            {"name": "NPO Management", "type": "lifestyle_change"},
            {"name": "IV Fluid Resuscitation", "type": "therapy"},
        ],
    },
    {
        "soap": SOAP_NOTES[4],
        "status": "open",
        "tests": ["Rheumatoid Factor", "Anti-CCP", "ESR", "CRP", "Joint X-rays"],
        "medicines": [
            {
                "name": "Ibuprofen",
                "dosage": "600mg",
                "route": "oral",
                "frequency": "three times daily",
            },
            {
                "name": "Methotrexate",
                "dosage": "15mg",
                "route": "oral",
                "frequency": "weekly",
            },
        ],
        "diagnoses": [
            {"name": "Rheumatoid Arthritis", "probability": 0.70, "status": "active"},
            {"name": "Inflammatory Arthritis", "probability": 0.85, "status": "active"},
        ],
        "treatments": [
            {"name": "DMARD Therapy", "type": "medication"},
            {"name": "Physical Therapy", "type": "therapy"},
        ],
    },
]

# Generate data for 20 patients
for i in range(1, 21):
    patient_id = generate_patient_id(i)

    # Each patient gets 1-3 cases
    num_cases = random.randint(1, 3)

    for case_num in range(num_cases):
        case_id = generate_object_id()
        case_number = (
            generate_object_id()
        )  # Using ObjectId for case number as requested

        # Select a random condition
        condition = random.choice(CONDITIONS)

        # Create case
        case_date = datetime.now(timezone.utc) - timedelta(days=random.randint(1, 90))

        case = Case(
            _id=case_id,
            patient_id=patient_id,
            case_number=case_number,
            soap=condition["soap"],
            case_date=case_date,
            transcriptions=f"Audio transcription for case {case_number} - patient reported symptoms clearly",
            status=condition["status"],
            notes=f"Additional notes for patient {patient_id}, case {case_num + 1}",
            created_at=case_date,
            updated_at=case_date + timedelta(hours=random.randint(1, 48)),
        )
        MOCK_CASES.append(case)

        # Create tests for this case
        for test_name in condition["tests"]:
            test_id = generate_object_id()
            test_date = case_date + timedelta(hours=random.randint(1, 24))

            # Generate mock test results
            test_results = []
            if test_name == "ECG":
                test_results = [
                    {"rhythm": "sinus", "rate": "88", "intervals": "normal"}
                ]
            elif "Glucose" in test_name:
                test_results = [{"value": random.randint(80, 300), "unit": "mg/dL"}]
            elif test_name in ["CBC", "CMP"]:
                test_results = [
                    {"wbc": "8.5", "rbc": "4.2", "hgb": "13.5", "hct": "40.2"}
                ]
            else:
                test_results = [{"result": "pending", "status": "in_progress"}]

            test = Test(
                _id=test_id,
                case_id=case_id,
                patient_id=patient_id,
                test_name=test_name,
                test_date=test_date,
                notes=f"Test ordered for {test_name}",
                results=test_results,
                created_at=test_date,
                updated_at=test_date + timedelta(hours=2),
            )
            MOCK_TESTS.append(test)

        # Create medicines for this case
        for med_info in condition["medicines"]:
            medicine_id = generate_object_id()
            start_date = case_date + timedelta(hours=random.randint(2, 12))

            medicine = Medicine(
                _id=medicine_id,
                case_id=case_id,
                patient_id=patient_id,
                medicine_name=med_info["name"],
                dosage=med_info["dosage"],
                route=med_info["route"],
                frequency=med_info["frequency"],
                start_date=start_date,
                end_date=start_date + timedelta(days=random.randint(7, 30))
                if condition["status"] == "closed"
                else None,
                notes=f"Prescribed for {med_info['name']} therapy",
                created_at=start_date,
                updated_at=start_date + timedelta(hours=1),
            )
            MOCK_MEDICINES.append(medicine)

        # Create diagnoses for this case
        for diag_info in condition["diagnoses"]:
            diagnosis_id = generate_object_id()
            diagnosis_date = case_date + timedelta(hours=random.randint(4, 24))

            diagnosis = Diagnosis(
                _id=diagnosis_id,
                case_id=case_id,
                patient_id=patient_id,
                diagnosis_name=diag_info["name"],
                diagnosis_date=diagnosis_date,
                status=diag_info["status"],
                probability=diag_info["probability"],
                notes=f"Diagnosis based on clinical presentation and test results",
                follow_up="Follow up in 1-2 weeks or as needed",
                additional_info=f"Confidence level: {diag_info['probability']*100:.0f}%",
                created_at=diagnosis_date,
                updated_at=diagnosis_date + timedelta(hours=2),
            )
            MOCK_DIAGNOSES.append(diagnosis)

        # Create treatments for this case
        for treat_info in condition["treatments"]:
            treatment_id = generate_object_id()
            treatment_date = case_date + timedelta(hours=random.randint(6, 48))

            treatment = Treatment(
                _id=treatment_id,
                case_id=case_id,
                patient_id=patient_id,
                treatment_name=treat_info["name"],
                treatment_date=treatment_date,
                treatment_type=treat_info["type"],
                outcome="Ongoing" if condition["status"] != "closed" else "Improved",
                notes=f"Treatment plan: {treat_info['name']}",
                created_at=treatment_date,
                updated_at=treatment_date + timedelta(hours=4),
            )
            MOCK_TREATMENTS.append(treatment)

# Summary of generated data
print(f"Generated mock data:")
print(f"- {len(MOCK_CASES)} cases")
print(f"- {len(MOCK_TESTS)} tests")
print(f"- {len(MOCK_MEDICINES)} medicines")
print(f"- {len(MOCK_DIAGNOSES)} diagnoses")
print(f"- {len(MOCK_TREATMENTS)} treatments")
print(f"For patients: {', '.join([generate_patient_id(i) for i in range(1, 21)])}")
