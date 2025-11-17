# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Speech2text is a Python application for recording system audio and transcribing it to Portuguese text using OpenAI's Whisper model (via faster-whisper implementation with CTranslate2 for 4x performance improvement).

## Key Commands

### Setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Testing
```bash
python -m unittest discover tests/ -v
```

### Usage Modes

**Automated workflow (record + transcribe):**
```bash
python start.py --duration 30  # Records system audio and transcribes automatically
```

**Manual recording:**
```bash
python record.py --mode system --duration 60
python record.py --list-devices  # List audio devices
```

**Manual transcription:**
```bash
python main.py --input audio.wav --output text.txt
```

## Architecture

The codebase follows a modular pipeline architecture:

```
User Input → Recorder/Processor → Converter → Transcriber → Output
```

### Core Modules (src/)

1. **audio_recorder.py**: System audio capture using sounddevice
   - Auto-detects PulseAudio/PipeWire monitor devices
   - Supports both system audio and microphone input
   - Records at 16kHz (optimal for Whisper)

2. **audio_converter.py**: MP3→WAV conversion using ffmpeg
   - Converts to 16kHz, mono, 16-bit PCM
   - Verifies output with ffprobe

3. **transcriber.py**: Audio→Text using faster-whisper
   - **Language: Hardcoded to Portuguese ("pt")**
   - Uses WhisperModel with int8 quantization for CPU
   - VAD filter enabled for better voice detection
   - Returns combined text from all segments

4. **processor.py**: Main workflow orchestrator
   - Handles MP3→WAV conversion if needed
   - Calls transcriber with proper arguments
   - Manages temp file cleanup

### Entry Points

- **start.py**: Automated record+transcribe workflow (saves to output/)
- **record.py**: Audio recording CLI
- **main.py**: Transcription CLI

## Important Configuration

### Language Setting
**All transcriptions are configured for Portuguese (pt-br).** The language is hardcoded in `src/transcriber.py:25`:

```python
segments, info = model.transcribe(
    audio_path,
    language="pt",  # Fixed to Portuguese
    ...
)
```

To change language, modify this parameter.

### Audio Settings
- Sample rate: 16kHz (optimal for Whisper)
- Channels: Mono
- Format: WAV PCM 16-bit

### Model Selection
Default: `large-v3` (most accurate)
Alternatives: `tiny`, `base`, `small`, `medium` (faster, less accurate)

## Linux Audio Capture

Uses sounddevice to capture from PulseAudio/PipeWire monitor devices. The system auto-detects devices with "monitor" or "loopback" in their name. If detection fails, falls back to default input device.

## Dependencies

- **faster-whisper**: CTranslate2-based Whisper implementation
- **sounddevice**: Audio I/O
- **soundfile**: Audio file reading/writing
- **ffmpeg**: External dependency for MP3 conversion (must be installed on system)

## Output Structure

Automated workflow (`start.py`) saves to:
```
output/
├── audio_TIMESTAMP.wav
└── transcricao_TIMESTAMP.txt
```
