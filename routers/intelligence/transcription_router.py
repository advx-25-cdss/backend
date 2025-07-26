import collections
import io
import logging
import os
import tempfile
import wave
from fastapi import APIRouter, WebSocket
import librosa
import numpy as np
import websockets
import json
import asyncio
from typing import Optional
from . import client

from pydub import AudioSegment

from .prompts.decision import SUMMARIZE_PROMPT


class WhisperProviderClient:
    def __init__(self, ai_provider_url: str):
        self.ai_provider_url = ai_provider_url
        self.websocket: Optional[websockets.ClientConnection] = None
        # Sliding window buffer (6 seconds at 16kHz = 96,000 samples)
        self.audio_buffer = collections.deque(maxlen=6 * 16 * 1000)
        self.overlap_buffer = collections.deque(maxlen=16 * 1000)  # 1 second overlap

    async def connect(self):
        """Establish connection to Whisper provider"""
        try:
            self.websocket = await websockets.connect(self.ai_provider_url)
            logging.info(f"Connected to Whisper provider: {self.ai_provider_url}")
        except Exception as e:
            logging.error(f"Failed to connect to Whisper provider: {e}")
            raise

    async def disconnect(self):
        """Close connection to Whisper provider"""
        if self.websocket:
            await self.websocket.close()
            self.websocket = None

    async def send_audio(self, audio_data: bytes) -> str:
        """Send audio to Whisper provider and get transcription"""
        if not self.websocket:
            await self.connect()

        try:
            # Send audio data
            await self.websocket.send(audio_data)

            # Wait for transcription response
            response = await asyncio.wait_for(
                self.websocket.recv(),
                timeout=10.0
            )

            return response

        except websockets.exceptions.ConnectionClosed:
            logging.warning("Whisper provider connection closed, reconnecting...")
            await self.connect()
            return await self.send_audio(audio_data)

        except asyncio.TimeoutError:
            logging.error("Whisper provider timeout")
            return json.dumps({
                "transcript": "",
                "status": "timeout"
            })


# Global Whisper provider client
ai_client = WhisperProviderClient("ws://127.0.0.1:8001/ws/asr")

async def forward_to_ai_provider(audio_data: bytes) -> str:
    return await ai_client.send_audio(audio_data)


def webm_to_librosa_temp(data: bytes):
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_wav:
        temp_wav.write(data)
        temp_path = temp_wav.name
        with wave.open(temp_path, 'wb') as wf:
            wf.setnchannels(1)  # Mono
            wf.setsampwidth(2)  # Sample width in bytes
            wf.setframerate(16000)  # Sample rate
            wf.writeframes(data)
    try:
        # Load with librosa
        y, sr = librosa.load(temp_path, sr=None)

        return y

    finally:
        # Clean up temp files
        # os.unlink(temp_webm_path)
        # if 'temp_wav_path' in locals():
        #     os.unlink(temp_wav_path)
        pass


router = APIRouter()

# @router.post("")
# async def transcribe_audio(audio: bytes):
#

@router.get("/{case_id}/describe")
async def describe_case(case_id: str):
    """
    Describe a case by its ID.
    This is a placeholder function that simulates describing a case.
    """
    # Simulate a case description
    client.chat.completions.create(
        model='gpt-4.1',
        messages=[
            {"role": "system", "content": "You are summarizing a transcription of the conversation among patient and physician."},
            {"role": "user", "content": SUMMARIZE_PROMPT + f"Case ID: {case_id}"}
        ]
    )

