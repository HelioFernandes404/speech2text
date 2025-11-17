import unittest
import os
import tempfile
from src.audio_converter import converter_mp3_to_wav, verify_audio


class TestAudioConverter(unittest.TestCase):
    """Testes para o módulo de conversão de áudio"""

    def setUp(self):
        """Configuração antes de cada teste"""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Limpeza após cada teste"""
        # Limpar arquivos temporários
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_converter_arquivo_inexistente(self):
        """Testa conversão com arquivo que não existe"""
        input_file = os.path.join(self.temp_dir, "nao_existe.mp3")
        output_file = os.path.join(self.temp_dir, "output.wav")

        result = converter_mp3_to_wav(input_file, output_file)
        self.assertFalse(result)

    def test_verify_audio_arquivo_inexistente(self):
        """Testa verificação com arquivo que não existe"""
        wav_file = os.path.join(self.temp_dir, "nao_existe.wav")

        result = verify_audio(wav_file)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
