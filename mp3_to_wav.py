import os
import subprocess

def converter_mp3_para_wav():
    """Converte audio.mp3 para audio.wav com configurações otimizadas para transcrição"""
    try:
        input_path = input("Digite o caminho do arquivo MP3: ").strip()
        if not os.path.exists(input_path):
            print(f"❌ Arquivo {input_path} não encontrado!")
            return False

        print("⏳ Convertendo MP3 para WAV...")
        
        cmd = [
            'ffmpeg',
            '-i', 'audio.mp3',
            '-ar', '16000',        # Taxa de amostragem 16kHz
            '-ac', '1',            # Áudio mono
            '-acodec', 'pcm_s16le',# Codificação PCM 16-bit
            '-loglevel', 'error',  # Mostrar apenas erros
            '-y',                 # Sobrescrever arquivo existente
            'audio.wav'
        ]
        
        resultado = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        if resultado.returncode == 0:
            print("✅ Conversão concluída: audio.wav (16kHz, mono, 16-bit)")
            return True
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro na conversão:\n{e.stderr}")
    except Exception as e:
        print(f"❌ Erro inesperado: {str(e)}")
    
    return False

def verificar_audio():
    """Verifica as propriedades do arquivo WAV gerado"""
    try:
        print("\n🔍 Verificando arquivo WAV...")
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'stream=sample_rate,channels,bits_per_sample',
            '-of', 'default=noprint_wrappers=1',
            'audio.wav'
        ]
        resultado = subprocess.run(cmd, capture_output=True, text=True)
        print(resultado.stdout)
        return True
    except Exception as e:
        print(f"Erro na verificação: {str(e)}")
        return False

if __name__ == "__main__":
    if converter_mp3_para_wav():
        verificar_audio()
    else:
        print("Falha na conversão do arquivo MP3.")