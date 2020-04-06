from unittest import TestCase
from unittest.mock import patch, mock_open
from app.file import File
from pathlib import Path


class FileTests(TestCase):
    def setUp(self):
        self.file = File()

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="10|1|SELL|toaster_1|10.00|20",
    )
    def test_parse(self, mock_file):
        current_dir = Path(__file__).parent
        filename = f"{current_dir}/test_input.txt"
        self.file.parse(filename)

        mock_file.assert_called_with(filename, encoding="utf-8")

    @patch("app.file.csv.writer")
    def test_save(self, mock_writer):
        current_dir = Path(__file__).parent
        filename = f"{current_dir}/test_output.txt"
        test_data = ["23", "45"]
        self.file.save(test_data, filename)

        self.assertTrue(mock_writer.called)
