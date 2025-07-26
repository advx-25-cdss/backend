from datetime import datetime, timezone

from bson import ObjectId

from database import db
from kernel.chat_output import (
    PatientSummary,
    Medicine as MedicineOutput,
    Diagnosis as DiagnosisOutput,
    TestResult as TestResultOutput,
)


async def summarize_user_data(case_id: str) -> PatientSummary:
    patient_case = await db.cdss.get_collection("cases").find_one({"_id": ObjectId(case_id)})
    patient_id = patient_case.get("patient_id") if patient_case else None
    if not patient_id:
        raise "Patient ID not found for the given case."
    patient_demographics = await db.cdss.get_collection("demographics").find_one(
        {"patient_id": patient_id}
    )
    if not patient_demographics:
        raise "Patient demographics not found for the given patient ID."
    transcription_results = await db.cdss.get_collection("transcriptions").find_one(
        {"case_id": case_id}
    )
    demographics = await db.cdss.get_collection("demographics").find_one(
        {"patient_id": patient_id}
    )
    print("Demographics:", demographics)
    patient_info = {
        "id": patient_id,
        "name": demographics.get("name", "Unknown"),
        "age": demographics.get("age", "Unknown"),
        "gender": demographics.get("gender", "Unknown"),
        "chief_complaint": transcription_results.get("chief_complaint", "Unknown"),
        "history_of_present_illness": transcription_results.get(
            "history_of_present_illness", "Unknown"
        ),
    }
    print("Patient Info:", patient_info)
    meditation_info = (
        await db.cdss.get_collection("medications")
        .find(
            {
                "patient_id": patient_id,
                "$or": [
                    { "end_date": { "$exists": False } },
                    { "end_date": { "$gt": datetime.now() } }
                ]
            }
        )
        .to_list(length=None)
    )
    print("Current Medications:", meditation_info)
    current_medications = []
    for med in meditation_info:
        current_medications.append(
            MedicineOutput(
                medicine_name=med.get("medicine_name", "Unknown"),
                dosage=med.get("dosage", "Unknown"),
                route=med.get("route", "Unknown"),
                frequency=med.get("frequency", "Unknown"),
                notes=med.get("notes", ""),
            )
        )
    diagnoses_history = (
        await db.cdss.get_collection("diagnoses")
        .find({"patient_id": patient_id})
        .to_list(length=None)
    )
    diagnoses = []
    for diagnosis in diagnoses_history:
        diagnoses.append(
            DiagnosisOutput(
                diagnosis_name=diagnosis.get("diagnosis_name", "Unknown"),
                diagnosis_date=datetime.now(timezone.utc).isoformat(),
                status=diagnosis.get("status", "Unknown"),
                notes=diagnosis.get("notes", ""),
                follow_up=diagnosis.get("follow_up", ""),
            )
        )
    test_results_history = (
        await db.cdss.get_collection("tests")
        .find({"patient_id": patient_id})
        .to_list(length=None)
    )
    test_results = []
    for test in test_results_history:
        test_results.append(
            TestResultOutput(
                test_name=test.get("test_name", "Unknown"),
                results=[],
                notes=test.get("notes", ""),
            )
        )
    treatments_history = (
        await db.cdss.get_collection("treatments")
        .find({"patient_id": patient_id})
        .to_list(length=None)
    )
    treatments = []
    for treatment in treatments_history:
        treatments.append(
            {
                "treatment_name": treatment.get("treatment_name", "Unknown"),
                "treatment_type": treatment.get("treatment_type", "Unknown"),
                "treatment_date": treatment.get("treatment_date", "Unknown"),
            }
        )
    patient_summary = PatientSummary(
        patient_info=patient_info,
        current_medications=current_medications,
        diagnoses_history=diagnoses,
        test_results_history=test_results,
        treatments_history=treatments,
    )
    return patient_summary
