import whisper
import os
import sys
import argparse
import ffmpeg
import subprocess

def converter_para_wav():
    """Converte audio.ogg para audio.wav com parâmetros otimizados"""
    try:
        print("⏳ Convertendo OGG/Opus para WAV...")
        (
            ffmpeg.input('audio.ogg')
            .output('audio.wav',
                   ar=16000,  # Taxa de amostragem fixa
                   ac=1,       # Canal mono
                   acodec='pcm_s16le',  # Formato PCM 16-bit
                   loglevel='error'
                   )
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        print("✅ Conversão concluída: audio.wav (16kHz, mono, 16-bit)")
        return True
    except ffmpeg.Error as e:
        print(f"❌ Erro na conversão: {e.stderr.decode()}")
        return False

def analisar_audio():
    try:
        print("\n🔍 Metadados do áudio:")
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries',
             'stream=codec_name,sample_rate,channels:format=duration',
             '-of', 'default=noprint_wrappers=1', 'audio.wav'],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        return True
    except Exception as e:
        print(f"Erro na análise: {str(e)}")
        return False

def transcrever_audio(model_name, device='cpu'):
    try:
        model = whisper.load_model(model_name, device=device)
        
        print("\n⚙️ Parâmetros de transcrição:")
        print(f"Modelo: {model_name.upper()}")
        print(f"Dispositivo: {'GPU' if device == 'cuda' else 'CPU'}")
        print("Formato: WAV 16kHz mono")
        print("Decoding: Beam Search com temperatura 0.0\n")
        
        result = model.transcribe(
            'audio.wav',
            language='pt',
            verbose=True,
            temperature=0.0,       # Máxima determinização
            beam_size=7,           # Busca mais abrangente
            compression_ratio_threshold=2.4,
            logprob_threshold=-1.0,
            no_speech_threshold=0.6,
            condition_on_previous_text=False,
            initial_prompt="Áudio convertido para WAV de alta qualidade com 16kHz e canal mono."
        )
        return result['text']
    except Exception as e:
        raise RuntimeError(f"Falha na transcrição: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Transcrição Especializada para WAV')
    parser.add_argument('--model', type=str, default='large-v3',
                      help='Modelo Whisper (medium, large-v3)')
    parser.add_argument('--device', type=str, default='cpu',
                      help='Dispositivo de processamento (cpu ou cuda)')
    parser.add_argument('--keep-wav', action='store_true',
                      help='Manter arquivo WAV após processamento')
    parser.add_argument('--output', type=str, default='transcricao.txt',
                      help='Nome do arquivo de saída')
    args = parser.parse_args()

    if not os.path.exists("audio.ogg"):
        print("Erro: Arquivo audio.ogg não encontrado!")
        sys.exit(1)

    if not converter_para_wav():
        sys.exit(1)

    if not analisar_audio():
        sys.exit(1)

    try:
        texto = transcrever_audio(args.model, args.device)
        
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(texto)
        
        print(f"\n🎉 Transcrição finalizada!\nArquivo: {os.path.abspath(args.output)}")
        print(f"Texto ({len(texto)} caracteres):\n{'-'*50}")
        print(texto[:500] + "..." if len(texto) > 500 else texto)
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        sys.exit(1)
    finally:
        if not args.keep_wav and os.path.exists('audio.wav'):
            os.remove('audio.wav')
            print("\nArquivo temporário audio.wav removido")

if __name__ == "__main__":
    main()