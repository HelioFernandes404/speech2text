# Speech2text - Faster Whisper

High-performance audio transcription using faster-whisper (up to 4x faster than standard Whisper).

## Features
- **Record system audio** (capture PC output) or microphone
- Convert audio (MP3/WAV) to text with optimal speed
- CPU optimized with int8 quantization
- GPU support with float16
- Automatic audio resampling to 16kHz

## Stack
- Python + faster-whisper (CTranslate2)
- ffmpeg for audio conversion
- Ubuntu

## Installation

```bash
git@github.com:HelioFernandes404/speech2text.git
cd speech2text
pip install -r requirements
```

## Usage

### 1. Record Audio

```bash
# Record system audio (what's playing on PC)
python record.py --mode system --duration 30

# Record from microphone
python record.py --mode microphone --duration 10

# List available audio devices
python record.py --list-devices

# Record with custom device and output
python record.py --mode system --device 5 --output my_recording.wav --duration 60
```

### 2. Transcribe Audio

```bash
# Basic transcription (CPU, int8)
python main.py --input audio.mp3 --output transcription.txt

# GPU with float16
python main.py --input audio.mp3 --device cuda --compute-type float16

# Options
--model         # Model size: tiny, base, small, medium, large-v3 (default)
--device        # cpu or cuda
--compute-type  # int8 (CPU), float16 (GPU), int8_float16, float32
--keep-wav      # Keep WAV file after conversion
```

### 3. Complete Workflow

```bash
# Record + Transcribe in one go
python record.py --mode system --duration 30 --output meeting.wav
python main.py --input meeting.wav --output meeting.txt
```

## Project Strcture 
```bash
.
├── README.md
├── requirements.txt
├── script.py
└── tx
2 directories, 3 files
```

## Performance Tips
- **CPU**: Use int8 quantization (default)
- **GPU**: Use float16 for small/medium models
- **Large models**: May be slower on GPU (3x) vs CPU
- **Audio**: Automatically resampled to 16kHz mono

## Recording Tips (Linux)
- **System audio**: Uses PulseAudio/PipeWire monitor device
- **If recording fails**: Run `python record.py --list-devices` to find monitor device
- **Monitor device**: Usually has "monitor" or "loopback" in the name
- **Sample rate**: 16kHz is optimal for Whisper (smaller files, same accuracy)

