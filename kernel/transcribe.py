import os
from datetime import datetime
import pyaudio
import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import wave
import librosa
import numpy as np
from pydub import AudioSegment
import tempfile


class ContinuousTranscriber:
    def __init__(
        self,
        model="openai/whisper-medium",
        slice_duration=5,
        sample_rate=16000,
        channels=1,
        chunk_size=1024,
    ):
        self.processor = WhisperProcessor.from_pretrained(model)
        self.model = WhisperForConditionalGeneration.from_pretrained(model)
        self.slice_duration = slice_duration
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.is_recording = False

        # Initialize PyAudio only if needed for direct recording
        try:
            self.audio = pyaudio.PyAudio()
        except:
            self.audio = None
            print("PyAudio not available, only file-based transcription will work")

    def convert_webm_to_wav(self, input_file: str, output_file: str = None):
        """Convert WebM audio to WAV format suitable for transcription"""
        try:
            if output_file is None:
                output_file = input_file.replace('.webm', '.wav')
            
            # Load audio using pydub (supports various formats including WebM)
            audio = AudioSegment.from_file(input_file)
            
            # Convert to mono if stereo
            if audio.channels > 1:
                audio = audio.set_channels(1)
            
            # Set sample rate to 16kHz for Whisper
            audio = audio.set_frame_rate(self.sample_rate)
            
            # Export as WAV
            audio.export(output_file, format="wav")
            
            return output_file
        except Exception as e:
            print(f"Error converting audio format: {e}")
            # Try to transcribe original file if conversion fails
            return input_file

    def transcribe_audio(self, filename: str):
        """Transcribe the audio file using the Whisper model."""
        try:
            # Convert to WAV if needed
            if filename.endswith('.webm') or filename.endswith('.opus'):
                with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_wav:
                    wav_filename = self.convert_webm_to_wav(filename, temp_wav.name)
            else:
                wav_filename = filename
            
            # Load audio with librosa
            audio_array, sr = librosa.load(wav_filename, sr=self.sample_rate)
            
            # Check if audio is too short or empty
            if len(audio_array) < 0.5 * self.sample_rate:  # Less than 0.5 seconds
                return ""
            
            # Check if audio is mostly silence
            if np.max(np.abs(audio_array)) < 0.01:  # Very quiet audio
                return ""
            
            # Process with Whisper
            audio_input = self.processor(
                audio_array, 
                sampling_rate=self.sample_rate, 
                return_tensors="pt"
            ).input_features
            
            with torch.no_grad():
                predicted_ids = self.model.generate(
                    audio_input.float(),
                    max_length=448,  # Limit output length
                    num_beams=1,     # Faster inference
                    do_sample=False  # Deterministic output
                )
            
            transcription = self.processor.batch_decode(
                predicted_ids, 
                skip_special_tokens=True
            )[0]
            
            # Clean up temporary WAV file if created
            if wav_filename != filename and os.path.exists(wav_filename):
                os.remove(wav_filename)
            
            return transcription.strip()
            
        except Exception as e:
            print(f"Transcription error: {e}")
            return ""

    def transcribe_audio_chunk_from_bytes(self, audio_bytes: bytes, audio_format: str = "webm"):
        """Transcribe audio directly from bytes without saving to disk first"""
        try:
            # Create temporary file from bytes
            with tempfile.NamedTemporaryFile(suffix=f'.{audio_format}', delete=False) as temp_file:
                temp_file.write(audio_bytes)
                temp_filename = temp_file.name
            
            try:
                # Transcribe the temporary file
                result = self.transcribe_audio(temp_filename)
                return result
            finally:
                # Clean up temporary file
                if os.path.exists(temp_filename):
                    os.remove(temp_filename)
                    
        except Exception as e:
            print(f"Error transcribing audio from bytes: {e}")
            return ""

    def start_transcribe(self, filename: str):
        """Record audio directly from microphone (legacy method)"""
        if self.audio is None:
            raise RuntimeError("PyAudio not available for direct recording")
            
        stream = self.audio.open(
            rate=self.sample_rate,
            channels=self.channels,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.chunk_size,
        )
        print(f"Recording {self.slice_duration}s audio slice...")
        frames = []
        self.is_recording = True

        # Record for the specified duration
        for _ in range(
            0, int(self.sample_rate / self.chunk_size * self.slice_duration)
        ):
            if not self.is_recording:
                break
            data = stream.read(self.chunk_size)
            frames.append(data)

        stream.stop_stream()
        stream.close()

        # Save the audio slice to a temporary file
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b"".join(frames))

        return len(frames) > 0

    def process_audio_slice(self, slice_number):
        """Process a single audio slice - record and transcribe (legacy method)"""
        temp_filename = f"temp_audio_slice_{slice_number}.wav"

        try:
            # Record audio slice
            if self.start_transcribe(temp_filename):
                # Transcribe the audio
                transcript = self.transcribe_audio(temp_filename)

                # Display results
                timestamp = datetime.now().strftime("%H:%M:%S")
                if transcript:
                    print(f"[{timestamp}] Slice {slice_number}: {transcript}")
                else:
                    print(f"[{timestamp}] Slice {slice_number}: (no speech detected)")

        except Exception as e:
            print(f"Error processing slice {slice_number}: {e}")

        finally:
            # Clean up temporary file
            if os.path.exists(temp_filename):
                os.remove(temp_filename)

    def cleanup(self):
        """Clean up resources"""
        self.is_recording = False
        if self.audio:
            self.audio.terminate()


# Example usage
if __name__ == "__main__":
    # Create recognizer instance
    recognizer = ContinuousTranscriber(
        slice_duration=5,  # 5-second slices
        sample_rate=16000,  # 16kHz sample rate (good for speech)
        channels=1,  # Mono audio
        chunk_size=1024,  # Chunk size for reading audio
    )

    # Start continuous recognition
    file_name = "transcription_output.mp3"
    recognizer.start_transcribe(file_name)
    result = recognizer.transcribe_audio(file_name)
    print(result)

    # Clean up
    recognizer.cleanup()
    print("Audio recognition stopped.")
