#!/usr/bin/env python3
"""
Example usage of the speech2text application
"""

import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.audio_converter import converter_mp3_to_wav, verify_audio
from src.transcriber import transcribe_audio


def example_basic_usage():
    """Basic example of converting and transcribing audio"""
    input_file = "sample_audio.mp3"
    wav_file = "sample_audio.wav"
    
    # Convert MP3 to WAV
    if converter_mp3_to_wav(input_file, wav_file):
        verify_audio(wav_file)
        
        # Transcribe audio
        text = transcribe_audio(wav_file, modelo="base", device="cpu")
        
        # Save transcription
        with open("transcription.txt", "w", encoding="utf-8") as f:
            f.write(text)
        
        print("✅ Transcription completed!")
    else:
        print("❌ Failed to convert audio")


if __name__ == "__main__":
    example_basic_usage()