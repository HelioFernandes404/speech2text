import whisper
import torch


def transcribe_audio(audio_path: str, modelo: str = "large-v3", device: str = "cpu") -> str:
    """Transcreve áudio para texto usando Whisper com máxima precisão"""
    try:
        if device == "cuda" and not torch.cuda.is_available():
            print("⚠️ CUDA não disponível. Usando CPU.")
            device = "cpu"

        print(f"🚀 Carregando modelo {modelo} ({device.upper()})...")
        model = whisper.load_model(modelo, device=device)

        print("\n🔊 Iniciando transcrição...")
        resultado = model.transcribe(
            audio_path,
            language="pt",
            verbose=True,
            temperature=0.0,
            beam_size=5,
            best_of=5,
            compression_ratio_threshold=2.4,
            no_speech_threshold=0.6,
            initial_prompt="Transcrição de alta precisão com Whisper large-v3."
        )
        
        return str(resultado["text"])
    except Exception as e:
        raise RuntimeError(f"Erro na transcrição: {str(e)}")