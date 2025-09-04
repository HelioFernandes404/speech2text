import os
import subprocess
import argparse
import whisper
import torch

def converter_mp3_to_wav(input_mp3: str, output_wav: str) -> bool:
    """Converts MP3 file to WAV with optimized settings for transcription"""
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
    """Verifies the properties of the generated WAV file"""
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
        print(f"Error in verification: {str(e)}")
        return False

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
        
        return resultado["text"]
    except Exception as e:
        raise RuntimeError(f"Error in transcription: {str(e)}")

def process_input(args):
    """Main audio processing workflow"""
    # Verify input file
    if not os.path.exists(args.input):
        raise FileNotFoundError(f"File {args.input} not found!")

    path_audio = args.input
    wav_temp = None

    # Convert MP3 to WAV if necessary
    if args.input.lower().endswith('.mp3'):
        wav_temp = os.path.splitext(args.input)[0] + ".wav"
        if not converter_mp3_to_wav(args.input, wav_temp):
            raise RuntimeError("Failed to convert MP3 to WAV")
        verify_audio(wav_temp)
        path_audio = wav_temp

    # Transcribe audio
    text = transcribe_audio(path_audio, args.model, args.device)

    # Save transcription
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(text)

    # Clean temporary file
    if wav_temp and not args.keep_wav:
        try:
            os.remove(wav_temp)
            print(f"🗑️ Temporary file {wav_temp} removed")
        except Exception as e:
            print(f"⚠️ Error removing temporary file: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Convert MP3 to txt with Whisper")
    parser.add_argument("--input", dest="input", required=True, help="Input file path (MP3/WAV)")
    parser.add_argument("--output", dest="output", default="transcription.txt", help="Output file for transcription")
    parser.add_argument("--model", dest="model", default="large-v3", help="Whisper model (tiny, base, small, medium, large-v3)")
    parser.add_argument("--device", dest="device", default="cpu", choices=["cpu", "cuda"], help="Processing device")
    parser.add_argument("--keep-wav", dest="keep_wav", action="store_true", help="Keep WAV file after conversion")
    
    args = parser.parse_args()

    try:
        process_input(args)
        print(f"\n✅ Transcription completed! Result saved to: {args.output}")
    except Exception as e:
        print(f"\n❌ Processing failed: {str(e)}")
        exit(1)
        
if __name__ == "__main__":
    main()