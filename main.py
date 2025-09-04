import argparse
from src.processor import process_input


def main():
    parser = argparse.ArgumentParser(description="Convert MP3 to text with Whisper")
    parser.add_argument("--input", required=True, help="Input file path (MP3/WAV)")
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