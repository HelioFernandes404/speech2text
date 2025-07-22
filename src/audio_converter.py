import os
import subprocess


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