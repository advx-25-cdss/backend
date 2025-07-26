from datetime import datetime, timezone

from bson import ObjectId
from fastapi import APIRouter
from database import db
from kernel.decision import summarize_user_data
from kernel.diagnosis_treatment_output import generate_clinical_plan
from kernel.tests_struct_output import get_test_recommendations
from models.dianosis_models import Test, Diagnosis

router = APIRouter()


@router.post("/{case_id}/tests")
async def get_recommended_tests(case_id: str):
    """
    Get recommended tests for a specific case.
    This endpoint retrieves tests that are recommended based on the case ID.
    """
    # Placeholder for actual implementation
    transcript = await db.cdss.get_collection("transcriptions").find_one(
        {"case_id": case_id}
    )
    if not transcript:
        return {"message": "No transcription found for the given case ID."}
    recommends = get_test_recommendations(transcript["text"])
    for recommendation in recommends.recommendations:
        print(recommendation)
        if not recommendation.test_name:
            continue
        await db.cdss.get_collection("tests").insert_one(
            Test(
                _id="",
                case_id=case_id,
                patient_id=(await db.cdss.get_collection("cases").find_one(
                    {"_id": ObjectId(case_id)}
                ))["patient_id"],
                test_name=recommendation.test_name,
                test_date=datetime.now(timezone.utc),
                notes=recommendation.notes,
                results=[],
            ).model_dump()
        )



@router.post("/{case_id}/treatments")
async def get_recommended_treatments(case_id: str):
    """
    Get recommended treatments for a specific case.
    This endpoint retrieves treatments that are recommended based on the case ID.
    """
    # Placeholder for actual implementation
    conversation = await db.cdss.get_collection("conversations").find_one(
        {"case_id": case_id}
    )
    text = (
        conversation["conversation"][0]["content"]
        if conversation and "conversation" in conversation
        else ""
    )
    if not text:
        return {"message": "No conversation found for the given case ID."}
    data = await summarize_user_data(text)
    recommendations = generate_clinical_plan(data)
    print(recommendations)
    diagnosis = Diagnosis(
        _id="",
        case_id=case_id,
        patient_id=data.patient_info.get("id", ""),
        diagnosis_name=recommendations.diagnosis.diagnosis_name,
        diagnosis_date=recommendations.diagnosis.diagnosis_date,
        status=recommendations.diagnosis.status,
        notes=recommendations.diagnosis.notes,
        probability=0.0,
        follow_up=recommendations.diagnosis.follow_up,
        additional_info="",
    )
    await db.cdss.get_collection("diagnoses").insert_one(diagnosis.model_dump())
    for med in recommendations.medication_plan:
        await db.cdss.get_collection("medications").insert_one(
            {
                "_id": "",
                "case_id": case_id,
                "patient_id": data.patient_info.get("id", ""),
                "medicine_name": med.medicine_name,
                "dosage": med.dosage,
                "route": med.route,
                "frequency": med.frequency,
                "start_date": datetime.now(timezone.utc),
                "end_date": None,
                "notes": med.notes,
            }
        )
    for treatment in recommendations.other_treatments:
        await db.cdss.get_collection("treatments").insert_one(
            {
                "_id": "",
                "case_id": case_id,
                "patient_id": data.patient_info.get("id", ""),
                "treatment_name": treatment.treatment_name,
                "treatment_type": treatment.treatment_type,
                "notes": treatment.notes,
                "outcome": "",
            }
        )

