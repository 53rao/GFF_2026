"""
tts.py — Text-to-Speech Wrapper (ElevenLabs / Twilio)
=====================================================
Converts dynamic AI agent dialogue text into natural, low-latency audio streams
for playback over outbound Twilio voice calls.
"""

from __future__ import annotations

from typing import AsyncGenerator


class TTSClient:
    """Wrapper around ElevenLabs or Twilio neural text-to-speech engine."""

    def __init__(self, voice_id: str | None = None) -> None:
        pass

    async def generate_speech_stream(self, text: str) -> AsyncGenerator[bytes, None]:
        """Converts text into a stream of audio bytes for low-latency phone playback."""
        raise NotImplementedError
