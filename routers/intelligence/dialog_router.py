from datetime import datetime
from kernel.chat_output import (
    PatientSummary,
    Medicine as MedicineOutput,
    Diagnosis as DiagnosisOutput,
    TestResult as TestResultOutput,
    get_ai_chat_response,
)
from fastapi import APIRouter
from database import db

router = APIRouter()


@router.post("/cases/{case_id}/initiation")
async def initiate_dialogue(case_id: str):
    """
    Initiate a dialogue for a specific case.
    :param case_id: The ID of the case for which the dialogue is being initiated.
    :return: The conversation ID.
    """

    # Here you would typically start a new conversation in your dialogue system
    id, result = await get_ai_chat_response(
        patient_summary, "这是一位病人的病历摘要。简单总结情况。"
    )
    return {
        "conversation_id": id,
        "summary": result,
    }


@router.post("/dialogues/{conversation_id}/continuation")
async def continue_dialogue(conversation_id: str, user_input: str):
    """
    Continue a dialogue with user input.
    :param conversation_id: The ID of the conversation to continue.
    :param user_input: The input from the user to continue the dialogue.
    :return: The updated conversation response.
    """
    # Here you would typically fetch the conversation by ID and append the user input
    # For simplicity, we assume the function get_ai_chat_response handles this
    id, result = await get_ai_chat_response(conversation_id, user_input)
    return {
        "conversation_id": id,
        "response": result,
    }


@router.get("/dialogues/{conversation_id}")
async def get_dialogue(conversation_id: str):
    """
    Get the details of a specific dialogue.
    :param conversation_id: The ID of the conversation to retrieve.
    :return: The details of the conversation.
    """
    # Here you would typically fetch the conversation by ID
    # For simplicity; we assume the function get_ai_chat_response handles this
    conversation = await db.cdss.get_collection("conversations").find_one(
        {"_id": conversation_id}
    )
    if not conversation:
        return {"error": "Conversation not found"}
    return {
        "conversation_id": conversation["_id"],
        "details": conversation,
    }
