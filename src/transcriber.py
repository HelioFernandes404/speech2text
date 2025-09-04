import whisper
import torch


def transcribe_audio(audio_path: str, model: str = "large-v3", device: str = "cpu") -> str:
    """Transcribes audio to text using Whisper with maximum precision"""
    try:
        if device == "cuda" and not torch.cuda.is_available():
            print("⚠️ CUDA not available. Using CPU.")
            device = "cpu"

        print(f"🚀 Loading model {model} ({device.upper()})...")
        model = whisper.load_model(model, device=device)

        print("\n🔊 Starting transcription...")
        resultado = model.transcribe(
            audio_path,
            language="en",
            verbose=True,
            temperature=0.0,
            beam_size=5,
            best_of=5,
            compression_ratio_threshold=2.4,
            no_speech_threshold=0.6,
            initial_prompt="High precision transcription with Whisper large-v3."
        )
        
        return str(resultado["text"])
    except Exception as e:
        raise RuntimeError(f"Error in transcription: {str(e)}")