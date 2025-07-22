import os
from .audio_converter import converter_mp3_to_wav, verify_audio
from .transcriber import transcribe_audio


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