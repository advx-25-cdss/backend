from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
import tempfile
import os
import uuid
from typing import List, Dict, Any
from kernel.transcribe import ContinuousTranscriber
from kernel.summarize import get_summarizer
import asyncio
import json

router = APIRouter()

# Global state to store transcription segments and conversation data
transcription_state = {
    "segments": [],
    "current_session_id": None,
    "is_active": False,
    "last_update": None
}

# Initialize transcriber and summarizer
transcriber = ContinuousTranscriber()
summarizer = get_summarizer()

class TranscriptionSegment:
    def __init__(self, text: str, speaker: str = "unknown", timestamp: str = None):
        self.id = str(uuid.uuid4())
        self.speaker = speaker
        self.text = text
        self.timestamp = timestamp or datetime.now().strftime("%H:%M:%S")
        self.start_time = datetime.now().timestamp()
        self.end_time = self.start_time
    
    def to_dict(self):
        return {
            "id": self.id,
            "speaker": self.speaker,
            "text": self.text,
            "timestamp": self.timestamp,
            "startTime": self.start_time,
            "endTime": self.end_time
        }

@router.post("/transcribe-chunk")
async def transcribe_chunk(
    audio: UploadFile = File(...),
    timestamp: str = Form(...)
):
    """
    Process audio chunk and return transcription
    """
    try:
        if not audio.content_type.startswith("audio/"):
            raise HTTPException(status_code=400, detail="Invalid audio file")
        
        # Create temporary file for audio processing
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            content = await audio.read()
            temp_file.write(content)
            temp_filename = temp_file.name
        
        try:
            # Transcribe the audio chunk
            transcript = transcriber.transcribe_audio(temp_filename)
            
            if transcript.strip():
                # Create new transcription segment
                segment = TranscriptionSegment(
                    text=transcript,
                    speaker="unknown",  # Will be enhanced later with speaker detection
                    timestamp=datetime.fromtimestamp(int(timestamp) / 1000).strftime("%H:%M:%S")
                )
                
                # Add to global state
                transcription_state["segments"].append(segment.to_dict())
                transcription_state["last_update"] = datetime.now().timestamp()
                transcription_state["is_active"] = True
                
                return JSONResponse({
                    "success": True,
                    "transcript": transcript,
                    "segment_id": segment.id,
                    "timestamp": segment.timestamp
                })
            else:
                return JSONResponse({
                    "success": True,
                    "transcript": "",
                    "message": "No speech detected"
                })
                
        finally:
            # Clean up temporary file
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

@router.get("/get-latest-transcription")
async def get_latest_transcription():
    """
    Get the latest transcription segments
    """
    try:
        return JSONResponse({
            "segments": transcription_state["segments"],
            "is_active": transcription_state["is_active"],
            "last_update": transcription_state["last_update"],
            "session_id": transcription_state["current_session_id"]
        })
    except Exception as e:
        return JSONResponse({
            "segments": [],
            "is_active": False,
            "error": str(e)
        })

@router.post("/summarize-conversation")
async def summarize_conversation():
    """
    Summarize the current conversation and clear the transcription state
    """
    try:
        if not transcription_state["segments"]:
            return JSONResponse({
                "success": False,
                "message": "No conversation to summarize"
            })
        
        # Combine all transcription segments into one text
        full_transcription = "\n".join([
            f"[{segment['timestamp']}] {segment['text']}" 
            for segment in transcription_state["segments"]
        ])
        
        # Generate summary using the AI summarizer
        ai_summary = summarizer.generate_summary(full_transcription)
        key_points = summarizer.extract_key_points(full_transcription)
        
        # Calculate duration from timestamps
        if transcription_state["segments"]:
            first_segment = transcription_state["segments"][0]
            last_segment = transcription_state["segments"][-1]
            duration_seconds = last_segment.get("endTime", 0) - first_segment.get("startTime", 0)
            duration = f"{int(duration_seconds // 60)}:{int(duration_seconds % 60):02d}"
        else:
            duration = "0:00"
        
        summary = {
            "conversation_summary": ai_summary,
            "key_points": key_points,
            "total_segments": len(transcription_state["segments"]),
            "duration": duration,
            "timestamp": datetime.now().isoformat()
        }
        
        # Archive current conversation (you might want to save to database)
        archived_conversation = {
            "session_id": transcription_state["current_session_id"] or str(uuid.uuid4()),
            "segments": transcription_state["segments"].copy(),
            "summary": summary,
            "archived_at": datetime.now().isoformat()
        }
        
        # Clear current transcription state
        transcription_state["segments"] = []
        transcription_state["current_session_id"] = None
        transcription_state["is_active"] = False
        transcription_state["last_update"] = None
        
        return JSONResponse({
            "success": True,
            "summary": summary,
            "archived_conversation": archived_conversation
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summarization failed: {str(e)}")

@router.post("/start-session")
async def start_transcription_session():
    """
    Start a new transcription session
    """
    session_id = str(uuid.uuid4())
    transcription_state["current_session_id"] = session_id
    transcription_state["segments"] = []
    transcription_state["is_active"] = True
    transcription_state["last_update"] = datetime.now().timestamp()
    
    return JSONResponse({
        "success": True,
        "session_id": session_id,
        "message": "Transcription session started"
    })

@router.post("/stop-session")
async def stop_transcription_session():
    """
    Stop the current transcription session
    """
    transcription_state["is_active"] = False
    
    return JSONResponse({
        "success": True,
        "session_id": transcription_state["current_session_id"],
        "total_segments": len(transcription_state["segments"]),
        "message": "Transcription session stopped"
    })

@router.get("/session-status")
async def get_session_status():
    """
    Get current session status
    """
    return JSONResponse({
        "session_id": transcription_state["current_session_id"],
        "is_active": transcription_state["is_active"],
        "segment_count": len(transcription_state["segments"]),
        "last_update": transcription_state["last_update"]
    })

@router.get("/health")
async def transcription_health_check():
    """
    Health check endpoint for transcription service
    """
    try:
        # Test if transcriber is initialized
        transcriber_status = "ready" if transcriber else "not_initialized"
        
        # Test if summarizer is available
        summarizer_status = "ready" if summarizer.model_loaded else "fallback_mode"
        
        return JSONResponse({
            "status": "healthy",
            "transcriber": transcriber_status,
            "summarizer": summarizer_status,
            "current_session": transcription_state["current_session_id"],
            "active_segments": len(transcription_state["segments"]),
            "service": "transcription_api"
        })
    except Exception as e:
        return JSONResponse({
            "status": "unhealthy",
            "error": str(e),
            "service": "transcription_api"
        }, status_code=500)
