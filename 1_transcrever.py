import whisper
import os
import sys
import argparse

def check_ffmpeg():
    try:
        import ffmpeg
    except ImportError:
        print("Erro: FFmpeg é necessário. Por favor instale primeiro.")
        print("\nComandos de instalação:")
        print("Ubuntu/Debian: sudo apt install ffmpeg")
        print("MacOS: brew install ffmpeg")
        print("Windows: choco install ffmpeg")
        return False
    return True

def main():
    parser = argparse.ArgumentParser(description='Transcrição de Áudio com Whisper')
    parser.add_argument('--model', type=str, default='medium', 
                      help='Modelo a ser usado (tiny, base, small, medium, large)')
    args = parser.parse_args()

    if not check_ffmpeg():
        sys.exit(1)

    if not os.path.exists("audio.ogg"):
        print("Erro: Arquivo audio.ogg não encontrado!")
        sys.exit(1)

    try:
        print(f"Carregando modelo {args.model}... (isso pode demorar)")
        model = whisper.load_model(args.model)
        
        print("Processando áudio...")
        result = model.transcribe(
            "audio.ogg",
            language='pt',  # Forçar idioma português
            verbose=True,     # Mostrar progresso
            task='transcribe',
            fp16=False,       # Mais compatibilidade com CPUs
            initial_prompt="Transcrição em português brasileiro usando termos comuns."  # Melhora precisão
        )
        
        with open("transcricao.txt", "w", encoding="utf-8") as f:
            f.write(result["text"])
        
        print("\nTranscrição finalizada com sucesso!")
        print(f"Arquivo salvo em: {os.path.abspath('transcricao.txt')}")
        
    except Exception as e:
        print(f"Erro durante a execução: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()