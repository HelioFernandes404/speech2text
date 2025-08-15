# TODO: double check on en-us 
import os
from .audio_converter import converter_mp3_to_wav, verify_audio
from .transcriber import transcribe_audio


def processar_entrada(args):
    """Fluxo principal de processamento de áudio"""
    """Flow the main process the audio"""
    # Verificar arquivo de entrada
    # Verifcy files the input 
    if not os.path.exists(args.input):
        raise FileNotFoundError(f"File {args.input} not found!")

    path_audio = args.input
    wav_temp = None

    # Converter MP3 para WAV se necessário
    # Converte the MP3 to WAV if necessrion 
    if args.input.lower().endswith('.mp3'):
        wav_temp = os.path.splitext(args.input)[0] + ".wav"
        if not converter_mp3_to_wav(args.input, wav_temp):
            raise RuntimeError("Fail on conversion MP3 to WAV") 
        verify_audio(wav_temp) 
        path_audio = wav_temp
    # TODO: traduzir for en-us 
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
