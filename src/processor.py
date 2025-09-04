# TODO: double check on en-us
import os
from .audio_converter import converter_mp3_to_wav, verify_audio
from .transcriber import transcribe_audio


def process_input(args):
    """Main audio processing workflow"""
    # Verify input file
    if not os.path.exists(args.input):
        raise FileNotFoundError(f"File {args.input} not found!")

    path_audio = args.input
    wav_temp = None

    # Convert MP3 to WAV if necessary
    if args.input.lower().endswith(".mp3"):
        wav_temp = os.path.splitext(args.input)[0] + ".wav"
        if not converter_mp3_to_wav(args.input, wav_temp):
            raise RuntimeError("Failed to convert MP3 to WAV")
        verify_audio(wav_temp)
        path_audio = wav_temp
    # Transcribe audio
    text = transcribe_audio(path_audio, args.model, args.device)

    # Save transcription
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(text)

    # Clean temporary file
    if wav_temp and not args.keep_wav:
        try:
            os.remove(wav_temp)
            print(f"🗑️ Temporary file {wav_temp} removed")
        except Exception as e:
            print(f"⚠️ Error removing temporary file: {str(e)}")
