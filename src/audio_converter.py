import os
import subprocess

def converter_mp3_to_wav(input_mp3: str, output_wav: str) -> bool:
    """Converts MP3 file to WAV with optimized configuration for transcription"""
    try:
        if not os.path.exists(input_mp3):
            print(f"❌ File {input_mp3} not found!")
            return False

        print("⏳ Converting MP3 to WAV...")
        
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
        print(f"✅ Conversion completed: {output_wav} (16kHz, mono, 16-bit)")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in conversion:\n{e.stderr}")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
    
    return False


def verify_audio(wav_path: str) -> bool:
    """Verify the properties of the generated WAV file"""
    try:
        print("\n🔍 Verifying WAV file...")
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
        print(f"Error during checking: {str(e)}")
        return False