#!/usr/bin/env python3
"""
Script automatizado: grava áudio do sistema e transcreve automaticamente
Uso: python start.py [--duration SEGUNDOS]
"""
import argparse
import os
import sys
from datetime import datetime
from src.audio_recorder import record_system_audio
from src.processor import process_input


class Args:
    """Classe auxiliar para argumentos"""
    def __init__(self, input_file, output_file, model, device, compute_type, keep_wav):
        self.input = input_file
        self.output = output_file
        self.model = model
        self.device = device
        self.compute_type = compute_type
        self.keep_wav = keep_wav


def main():
    parser = argparse.ArgumentParser(
        description="🎙️ Gravação e transcrição automática de áudio do sistema"
    )

    parser.add_argument("--duration", "-d", type=int, default=30,
                        help="Duração da gravação em segundos (padrão: 30)")

    parser.add_argument("--model", "-m", default="large-v3",
                        choices=["tiny", "base", "small", "medium", "large-v3"],
                        help="Modelo Whisper (padrão: large-v3)")

    parser.add_argument("--device", default="cpu",
                        choices=["cpu", "cuda"],
                        help="Dispositivo de processamento (padrão: cpu)")

    parser.add_argument("--compute-type", default="int8",
                        choices=["int8", "int8_float16", "float16", "float32"],
                        help="Tipo de quantização (padrão: int8)")

    parser.add_argument("--keep-audio", action="store_true",
                        help="Manter arquivo de áudio após transcrição")

    parser.add_argument("--output-dir", default="output",
                        help="Diretório para salvar arquivos (padrão: output/)")

    args = parser.parse_args()

    # Criar diretório de output se não existir
    os.makedirs(args.output_dir, exist_ok=True)

    # Gerar nomes de arquivos com timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    audio_file = os.path.join(args.output_dir, f"audio_{timestamp}.wav")
    text_file = os.path.join(args.output_dir, f"transcricao_{timestamp}.txt")

    print("=" * 60)
    print("🎙️  GRAVAÇÃO E TRANSCRIÇÃO AUTOMÁTICA")
    print("=" * 60)
    print(f"⏱️  Duração: {args.duration} segundos")
    print(f"🤖 Modelo: {args.model}")
    print(f"💾 Salvando em: {args.output_dir}/")
    print("=" * 60)

    try:
        # Etapa 1: Gravar áudio
        print("\n📍 ETAPA 1/2: Gravando áudio do sistema...")
        success = record_system_audio(
            audio_file,
            duration=args.duration,
            sample_rate=16000
        )

        if not success:
            print("\n❌ Falha na gravação!")
            sys.exit(1)

        # Etapa 2: Transcrever
        print("\n📍 ETAPA 2/2: Transcrevendo áudio...")

        # Criar objeto args para o processor
        proc_args = Args(
            input_file=audio_file,
            output_file=text_file,
            model=args.model,
            device=args.device,
            compute_type=args.compute_type,
            keep_wav=args.keep_audio
        )

        process_input(proc_args)

        # Mostrar resultado
        print("\n" + "=" * 60)
        print("✅ PROCESSAMENTO CONCLUÍDO!")
        print("=" * 60)

        with open(text_file, 'r', encoding='utf-8') as f:
            transcricao = f.read()

        print(f"\n📄 Transcrição ({len(transcricao.split())} palavras):")
        print("-" * 60)
        print(transcricao)
        print("-" * 60)

        print(f"\n💾 Arquivos salvos:")
        if args.keep_audio or os.path.exists(audio_file):
            print(f"   🎵 Áudio: {audio_file}")
        print(f"   📝 Texto: {text_file}")

        print("\n✨ Processo finalizado com sucesso!\n")

    except KeyboardInterrupt:
        print("\n\n⚠️ Processo interrompido pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
