import whisper
import argparse
import torch
import sys

def transcrever_com_maxima_precisao(arquivo_audio, modelo="large-v3", device="cpu"):
    try:
        # Força o uso de CPU se CUDA não está disponível
        if device == "cuda":
            if torch.cuda.is_available():
                print("🚀 Usando CUDA.")
            else:
                print("⚠️ CUDA não está disponível neste sistema. Usando CPU.")
                device = "cpu"

        model = whisper.load_model(modelo, device=device)

        print(f"\n🔊 Transcrevendo com máxima precisão (modelo: {modelo.upper()}, dispositivo: {device.upper()})")
        
        resultado = model.transcribe(
            arquivo_audio,
            language="pt",
            verbose=True,
            temperature=0.0,
            beam_size=5,
            best_of=5,
            compression_ratio_threshold=2.4,
            no_speech_threshold=0.6,
            initial_prompt="Transcrição de alta precisão com Whisper large-v3."
        )
        
        return resultado["text"]
    except Exception as e:
        raise RuntimeError(f"Erro na transcrição: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcrição com Máxima Precisão (Whisper large-v3)")
    parser.add_argument("--audio", type=str, default="audio.wav", help="Arquivo de áudio (WAV, MP3, etc.)")
    parser.add_argument("--model", type=str, default="large-v3", help="Modelo Whisper (tiny, base, small, medium, large-v3)")
    parser.add_argument("--device", type=str, default="cpu", help="Dispositivo (cpu ou cuda) — será forçado para CPU se CUDA indisponível")
    parser.add_argument("--output", type=str, default="transcricao_precisa.txt", help="Arquivo de saída")
    args = parser.parse_args()

    try:
        texto = transcrever_com_maxima_precisao(args.audio, args.model, args.device)
        if isinstance(texto, list):
            texto = "\n".join(str(t) for t in texto)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(texto)
        print(f"\n✅ Transcrição finalizada! Salvo em: {args.output}")
    except Exception as e:
        print(f"\n❌ Falha: {str(e)}")
