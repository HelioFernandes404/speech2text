import argparse
from src.processor import processar_entrada


def main():
    parser = argparse.ArgumentParser(description="Convert MP3 to txt with Whisper")
    parser.add_argument("--input", required=True, help="Caminho do arquivo de entrada (MP3/WAV)")
    parser.add_argument("--output", dest="saida", default="transcricao.txt", help="Arquivo de saída para transcrição")
    parser.add_argument("--model", dest="modelo", default="large-v3", help="Modelo Whisper (tiny, base, small, medium, large-v3)")
    parser.add_argument("--device", dest="dispositivo", default="cpu", choices=["cpu", "cuda"], help="Dispositivo de processamento")
    parser.add_argument("--keep-wav", dest="manter_wav", action="store_true", help="Manter arquivo WAV após conversão")
    
    args = parser.parse_args()

    try:
        processar_entrada(args)
        print(f"\n✅ Transcrição finalizada! Resultado salvo em: {args.saida}")
    except Exception as e:
        print(f"\n❌ Falha no processamento: {str(e)}")
        exit(1)
        

if __name__ == "__main__":
    main()