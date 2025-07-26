from pydantic import BaseModel
from kernel.chat_output import (
    get_ai_chat_response, continue_dialogue,
)
from fastapi import APIRouter
from database import db
from kernel.decision import summarize_user_data

router = APIRouter()


@router.post("/cases/{case_id}/initiation")
async def initiate_dialogue(case_id: str):
    """
    Initiate a dialogue for a specific case.
    :param case_id: The ID of the case for which the dialogue is being initiated.
    :return: The conversation ID.
    """
    patient_summary = await summarize_user_data(case_id)

    # Here you would typically start a new conversation in your dialogue system
    id, result = await get_ai_chat_response(
        patient_summary, "这是一位病人的病历摘要。简单总结情况。", case_id
    )
    return {
        "conversation_id": str(id),
        "summary": result,
    }


class UserInputData(BaseModel):
    user_input: str


@router.post("/dialogues/{conversation_id}/continuation")
async def continue_dialogue_(conversation_id: str, input_data: UserInputData):
    """
    Continue a dialogue with user input.
    :param conversation_id: The ID of the conversation to continue.
    :param user_input: The input from the user to continue the dialogue.
    :return: The updated conversation response.
    """
    # Here you would typically fetch the conversation by ID and append the user input
    # For simplicity, we assume the function get_ai_chat_response handles this
    result = await continue_dialogue(conversation_id, input_data.user_input)
    return {
        "summary": result,
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
