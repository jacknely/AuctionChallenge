from unittest import TestCase
from unittest.mock import patch, mock_open
from app.file import File
from pathlib import Path


class FileTests(TestCase):

    def setUp(self):
        self.file = File()

    @patch("builtins.open", new_callable=mock_open, read_data="10|1|SELL|toaster_1|10.00|20")
    def test_parse(self, mock_file):
        current_dir = Path(__file__).parent
        filename = Path.joinpath(current_dir / "test_input.txt")
        self.file.parse(filename)

        mock_file.assert_called_with(filename, encoding='utf-8')

    def test_save(self):
        pass
