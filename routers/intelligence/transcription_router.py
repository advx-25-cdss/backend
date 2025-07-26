import json
from datetime import datetime, timezone
from fastapi import APIRouter
from pydantic import BaseModel

from database import db
import openai


router = APIRouter()


class SaveTranscriptionRequest(BaseModel):
    text: str


class ResponseFormatSummarization(BaseModel):
    chief_complaint: str
    history_of_present_illness: str
    other_relevant_info: str


async def summarize_transcription(text: str):
    """
    Summarizes the transcription text.
    This function should implement the logic to summarize the transcription.
    """
    prompt = f"""You are a clinical experts who are summarizing the conversation between a patient and a doctor.
The patient is describing their symptoms and the doctor is asking questions to understand the patient's condition.
Please note that the transcription and summarization is continuous, so you should summarize the conversation as it progresses.
We could not tell patient and physician apart, so you should summarize the conversation as a whole.
Your output language should be the same as the input language.
You should contain user's chief complaint, history of present illness, and any other relevant information.
"""
    response = openai.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text},
        ],
        response_format=ResponseFormatSummarization
    )
    return response.choices[0].message.content



@router.post("/{case_id}/incremental")
async def save_transcription(case_id: str, save_request: SaveTranscriptionRequest):
    """
    Initiate a dialogue for a specific case.
    This endpoint can be used to start a conversation with an AI provider.
    """
    base = ""
    for already in (await db.cdss.get_collection("transcriptions").find({"case_id": case_id}).to_list(None)):
        base += already["text"] + "\n"
    save_request.text = base + save_request.text
    structured = await summarize_transcription(save_request.text)
    await db.cdss.get_collection("transcriptions").delete_many({"case_id": case_id})
    try:
        structured = json.loads(structured)
    except json.JSONDecodeError:
        structured = {
            "chief_complaint": "Unknown",
            "history_of_present_illness": "Unknown",
            "other_relevant_info": "Unknown",
        }
    await db.cdss.get_collection("transcriptions").insert_one({
        "case_id": case_id,
        "text": save_request.text,
        "created_at": datetime.now(timezone.utc),
        **structured,
    })

    return {"message": "Transcription saved successfully."}
