from fastapi import APIRouter
import base64

from pydantic import BaseModel

router = APIRouter()

class InitiateConversationContext(BaseModel):
    case_id: str
    patient_id: str

router.post("")
async def initiate_decisive_conversation(context: InitiateConversationContext):
    pass