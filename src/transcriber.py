from faster_whisper import WhisperModel


def transcribe_audio(audio_path: str, model: str = "large-v3", device: str = "cpu", compute_type: str = "int8") -> str:
    """Transcreve áudio para texto em português usando faster-whisper

    Args:
        audio_path: Caminho do arquivo de áudio
        model: Tamanho do modelo (tiny, base, small, medium, large-v3)
        device: Dispositivo de processamento (cpu ou cuda)
        compute_type: Tipo de quantização (int8, int8_float16, float16, float32)
    """
    try:
        # Adjust compute_type based on device
        if device == "cpu" and compute_type == "float16":
            print("⚠️ float16 not optimal for CPU. Using int8.")
            compute_type = "int8"

        print(f"🚀 Loading model {model} ({device.upper()}, {compute_type})...")
        model = WhisperModel(model, device=device, compute_type=compute_type)

        print("\n🔊 Iniciando transcrição em português...")
        segments, info = model.transcribe(
            audio_path,
            language="pt",
            beam_size=5,
            best_of=5,
            temperature=0.0,
            compression_ratio_threshold=2.4,
            no_speech_threshold=0.6,
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=500)
        )

        # Combine all segments into full text
        transcription = " ".join([segment.text for segment in segments])

        print(f"\n📊 Idioma detectado: {info.language} (confiança: {info.language_probability:.2%})")

        return transcription.strip()
    except Exception as e:
        raise RuntimeError(f"Erro na transcrição: {str(e)}")