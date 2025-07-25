# Transcription System Integration Guide

This guide explains how the real-time transcription system works between the React frontend and FastAPI backend.

## System Overview

The transcription system allows real-time audio recording and transcription during patient consultations. It consists of:

1. **React Frontend**: Handles audio recording, chunked audio upload, and real-time UI updates
2. **Next.js API Routes**: Middleware that forwards requests to the FastAPI backend
3. **FastAPI Backend**: Processes audio chunks, performs transcription, and manages session state
4. **AI Models**: Whisper for transcription and DialoGPT for conversation summarization

## Architecture

```
React Frontend (Audio Recording)
         ↓
Next.js API Routes (Middleware)
         ↓
FastAPI Backend (Processing)
         ↓
AI Models (Whisper + DialoGPT)
```

## Backend Endpoints

### FastAPI Endpoints (Port 8000)

1. **POST /api/transcription/transcribe-chunk**

   -  Processes audio chunks and returns transcription
   -  Input: FormData with audio file and timestamp
   -  Output: Transcription result with segment ID

2. **GET /api/transcription/get-latest-transcription**

   -  Returns all current transcription segments
   -  Output: Array of transcription segments with metadata

3. **POST /api/transcription/summarize-conversation**

   -  Summarizes the entire conversation and clears state
   -  Output: AI-generated summary with key points

4. **POST /api/transcription/start-session**

   -  Starts a new transcription session
   -  Output: New session ID

5. **POST /api/transcription/stop-session**

   -  Stops the current transcription session
   -  Output: Session summary

6. **GET /api/transcription/health**
   -  Health check for transcription services
   -  Output: Status of transcriber and summarizer models

### Next.js API Routes (Frontend Middleware)

1. **POST /api/transcribe-chunk**

   -  Forwards audio chunks to FastAPI backend
   -  Handles FormData forwarding

2. **GET /api/get-latest-transcription**

   -  Retrieves latest transcription from FastAPI
   -  Handles error cases gracefully

3. **POST /api/summarize-conversation**
   -  Forwards summarization requests to FastAPI
   -  Handles JSON request/response

## Setup Instructions

### 1. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Start FastAPI Server

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Configure Frontend Environment

Create a `.env.local` file in your Next.js project:

```env
FASTAPI_BACKEND_URL=http://localhost:8000
```

### 4. Start Frontend Development Server

```bash
npm run dev
```

## Usage Flow

### 1. Starting Transcription

1. User clicks "开始转录" (Start Transcription) button
2. Frontend requests microphone permission
3. Audio recording starts with 1-second chunks
4. Each chunk is sent to `/api/transcribe-chunk`
5. Backend processes chunk with Whisper model
6. Transcription result is stored in memory
7. Frontend polls `/api/get-latest-transcription` for updates

### 2. Real-time Updates

1. Frontend polls every 500ms for new transcriptions
2. New segments are displayed in real-time
3. Speaker identification (doctor/patient) is currently set to "unknown"
4. Timestamps are automatically added to each segment

### 3. Ending Session

1. User clicks "停止" (Stop) button
2. Audio recording stops
3. `/api/summarize-conversation` is called
4. AI generates conversation summary
5. Session state is cleared
6. Summary is returned to frontend

## Key Features

### Audio Processing

-  Supports WebM/Opus audio format from browser
-  Automatic conversion to WAV for Whisper processing
-  16kHz sample rate optimization for speech recognition
-  Silence detection to avoid empty transcriptions

### AI Models

-  **Whisper Medium**: For accurate speech-to-text transcription
-  **DialoGPT**: For conversation summarization (with fallback to rule-based)
-  Optimized inference settings for real-time performance

### State Management

-  In-memory session storage (can be extended to database)
-  Real-time segment tracking with unique IDs
-  Session-based conversation management
-  Automatic cleanup after summarization

### Error Handling

-  Graceful fallback for model loading failures
-  Audio format conversion error handling
-  Network error resilience
-  Empty audio chunk detection

## Configuration Options

### Transcription Settings

```python
# In kernel/transcribe.py
transcriber = ContinuousTranscriber(
    model="openai/whisper-medium",  # Model size
    sample_rate=16000,              # Audio sample rate
    channels=1,                     # Mono audio
)
```

### Summarization Settings

```python
# In kernel/summarize.py
summarizer = TranscriptionSummarizer(
    model_name="microsoft/DialoGPT-medium"  # Summary model
)
```

## Troubleshooting

### Common Issues

1. **"PyAudio not available" error**

   -  This is expected and doesn't affect web-based transcription
   -  Only impacts direct microphone recording (not used)

2. **Model loading failures**

   -  Check internet connection for first-time model download
   -  Models are cached locally after first download
   -  Fallback summarization will work if AI model fails

3. **Audio format errors**

   -  Ensure browser supports WebM recording
   -  pydub handles format conversion automatically

4. **CORS issues**
   -  FastAPI is configured with permissive CORS for development
   -  Adjust CORS settings for production deployment

### Testing

1. **Health Check**

   ```bash
   curl http://localhost:8000/api/transcription/health
   ```

2. **Manual Audio Upload**
   ```bash
   curl -X POST -F "audio=@test.wav" -F "timestamp=1234567890" \
        http://localhost:8000/api/transcription/transcribe-chunk
   ```

## Performance Considerations

-  First model load may take 30-60 seconds
-  Subsequent transcriptions are much faster
-  Consider using smaller Whisper models for faster inference
-  Memory usage scales with conversation length

## Future Enhancements

1. **Speaker Identification**: Implement speaker diarization
2. **Database Persistence**: Store conversations permanently
3. **Real-time Streaming**: WebSocket-based real-time updates
4. **Medical Context**: Fine-tune models for medical terminology
5. **Multi-language Support**: Support for multiple languages

## File Structure

```
backend/
├── kernel/
│   ├── transcribe.py       # Whisper transcription logic
│   └── summarize.py        # Conversation summarization
├── routers/diagnosis/
│   └── transcription_router.py  # FastAPI endpoints
└── main.py                 # FastAPI app configuration

frontend/
├── components/
│   └── TranscriptionArea.tsx    # React transcription UI
└── api/
    ├── transcribe-chunk/
    ├── get-latest-transcription/
    └── summarize-conversation/  # Next.js API routes
```

This integration provides a complete real-time transcription system suitable for medical consultations with AI-powered summarization capabilities.
