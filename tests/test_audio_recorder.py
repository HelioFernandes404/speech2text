import unittest
from unittest.mock import patch, MagicMock
from src.audio_recorder import find_monitor_device, list_audio_devices


class TestAudioRecorder(unittest.TestCase):
    """Testes para o módulo de gravação de áudio"""

    @patch('src.audio_recorder.sd.query_devices')
    def test_find_monitor_device_com_monitor(self, mock_query):
        """Testa detecção de dispositivo monitor"""
        # Simular dispositivos
        mock_query.return_value = [
            {'name': 'Monitor of Built-in Audio', 'max_input_channels': 2, 'index': 0},
            {'name': 'Built-in Microphone', 'max_input_channels': 1, 'index': 1},
        ]

        device_id, device_name = find_monitor_device()

        self.assertEqual(device_id, 0)
        self.assertIn('monitor', device_name.lower())

    @patch('src.audio_recorder.sd.query_devices')
    def test_find_monitor_device_sem_monitor(self, mock_query):
        """Testa fallback quando não há dispositivo monitor"""
        # Simular ausência de monitor
        mock_query.side_effect = [
            [{'name': 'Microphone', 'max_input_channels': 1, 'index': 0}],
            {'name': 'Default Input', 'max_input_channels': 1, 'index': 0}
        ]

        device_id, device_name = find_monitor_device()

        self.assertIsNotNone(device_id)
        self.assertIsNotNone(device_name)


if __name__ == '__main__':
    unittest.main()
