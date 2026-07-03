"""
stt.py — Speech-to-Text Wrapper (Whisper / Deepgram)
====================================================
Wraps streaming and batch speech transcription services to convert customer
voice audio into text during active Twilio calls or post-call recordings.
"""

from __future__ import annotations

from typing import AsyncGenerator


class STTClient:
    """Wrapper around Deepgram or OpenAI Whisper speech-to-text API."""

    def __init__(self) -> None:
        pass

    async def transcribe_audio_stream(self, audio_stream: AsyncGenerator[bytes, None]) -> AsyncGenerator[str, None]:
        """Transcribes raw real-time voice chunks into live text increments."""
        raise NotImplementedError

    async def transcribe_recording(self, recording_url: str) -> str:
        """Transcribes a completed audio recording URL into full text."""
        raise NotImplementedError
