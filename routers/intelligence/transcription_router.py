from datetime import datetime, timezone
from fastapi import APIRouter
from pydantic import BaseModel

from database import db
import openai


router = APIRouter()


class SaveTranscriptionRequest(BaseModel):
    text: str


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
"""
    response = openai.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text},
        ],
    )
    if response and response.choices:
        return response.choices[0].message.content
    return "No summary available."


@router.put("/{case_id}/incremental")
async def save_transcription(case_id: str, save_request: SaveTranscriptionRequest):
    """
    Initiate a dialogue for a specific case.
    This endpoint can be used to start a conversation with an AI provider.
    """
    base = ""
    for already in db.cdss.get_collection("transcriptions").find({"case_id": case_id}):
        base += already["text"] + "\n"
    save_request.text = base + save_request.text
    structured = summarize_transcription(save_request.text)
    await db.cdss.get_collection("transcriptions").delete_many({"case_id": case_id})
    await db.cdss.get_collection("transcriptions").insert_one(
        {
            "case_id": case_id,
            "text": save_request.text,
            "created_at": datetime.now(timezone.utc),
            **structured,
        }
    )

    return {"message": "Transcription saved successfully."}
