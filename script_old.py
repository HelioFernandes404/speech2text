import os
import subprocess
import argparse
import whisper
import torch

def converter_mp3_to_wav(input_mp3: str, output_wav: str) -> bool:
    """Converte arquivo MP3 para WAV com configurações otimizadas para transcrição"""
    try:
        if not os.path.exists(input_mp3):
            print(f"❌ Arquivo {input_mp3} não encontrado!")
            return False

        print("⏳ Convertendo MP3 para WAV...")
        
        cmd = [
            'ffmpeg',
            '-i', input_mp3,
            '-ar', '16000',
            '-ac', '1',
            '-acodec', 'pcm_s16le',
            '-loglevel', 'error',
            '-y',
            output_wav
        ]
        
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ Conversão concluída: {output_wav} (16kHz, mono, 16-bit)")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro na conversão:\n{e.stderr}")
    except Exception as e:
        print(f"❌ Erro inesperado: {str(e)}")
    
    return False

def verify_audio(wav_path: str) -> bool:
    """Verifica as propriedades do arquivo WAV gerado"""
    try:
        print("\n🔍 Verificando arquivo WAV...")
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'stream=sample_rate,channels,bits_per_sample',
            '-of', 'default=noprint_wrappers=1',
            wav_path
        ]
        resultado = subprocess.run(cmd, capture_output=True, text=True)
        print(resultado.stdout)
        return True
    except Exception as e:
        print(f"Erro na verificação: {str(e)}")
        return False

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
        
        return resultado["text"]
    except Exception as e:
        raise RuntimeError(f"Erro na transcrição: {str(e)}")

def processar_entrada(args):
    """Fluxo principal de processamento de áudio"""
    # Verificar arquivo de entrada
    if not os.path.exists(args.input):
        raise FileNotFoundError(f"Arquivo {args.input} não encontrado!")

    path_audio = args.input
    wav_temp = None

    # Converter MP3 para WAV se necessário
    if args.input.lower().endswith('.mp3'):
        wav_temp = os.path.splitext(args.input)[0] + ".wav"
        if not converter_mp3_to_wav(args.input, wav_temp):
            raise RuntimeError("Falha na conversão MP3 para WAV")
        verify_audio(wav_temp)
        path_audio = wav_temp

    # Transcrever áudio
    texto = transcribe_audio(path_audio, args.modelo, args.dispositivo)

    # Salvar transcrição
    with open(args.saida, 'w', encoding='utf-8') as f:
        f.write(texto)

    # Limpar arquivo temporário
    if wav_temp and not args.manter_wav:
        try:
            os.remove(wav_temp)
            print(f"🗑️ Arquivo temporário {wav_temp} removido")
        except Exception as e:
            print(f"⚠️ Erro ao remover arquivo temporário: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Convert MP3 to txt with Whisper")
    parser.add_argument("--input", dest="entrada", required=True, help="Caminho do arquivo de entrada (MP3/WAV)")
    parser.add_argument("--output", dest="saida", default="transcricao.txt", help="Arquivo de saída para transcrição")
    parser.add_argument("--model", dest="modelo", default="large-v3", help="Modelo Whisper (tiny, base, small, medium, large-v3)")
    parser.add_argument("--device", dest="dispositivo", default="cpu", choices=["cpu", "cuda"], help="Dispositivo de processamento")
    parser.add_argument("--keep-wav", dest="manter_wav", action="store_true", help="Manter arquivo WAV após conversão")
    
    args = parser.parse_args()

    try:
        processar_entrada(args)
        print(f"\n✅ Transcrição finalizada! Resultado salvo em: {args.saida}")
    except Exception as e:
        print(f"\n❌ Falha no processamento: {str(e)}")
        exit(1)
        
if __name__ == "__main__":
    main()