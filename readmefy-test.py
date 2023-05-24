import os
import sys
import unittest
from unittest.mock import patch, mock_open
import readmefy

class TestReadmefy(unittest.TestCase):
    def setUp(self):
        self.dir_path = os.getcwd()
        self.code_files = [
            os.path.join(self.dir_path, "mock", "main.py"),
            os.path.join(self.dir_path, "mock", "script.js"),
            os.path.join(self.dir_path, "mock", "index.html")
        ]
        self.api_key = sys.argv[1]

    def test_get_code_files_in_dir(self):
        # Test that the function returns a list of code files in the directory
        with patch("os.listdir") as mock_listdir:
            mock_listdir.return_value = ["main.py", "script.js", "index.html", "README.md"]
            code_files = readmefy.get_code_files_in_dir(os.path.join(self.dir_path, "mock"))
            self.assertEqual(code_files, self.code_files)

    def test_read_file_content(self):
        # Test that the function reads the content of a file
        with patch("builtins.open", mock_open(read_data="file content")) as mock_file:
            file_content = readmefy.read_file_content(self.code_files[0])
            self.assertEqual(file_content, "file content")

    @patch("requests.post")
    def test_generate_readme(self, mock_post):
        # Test that the function generates the README.md file
        mock_post.return_value.json.return_value = {
            "choices": [{"text": "This is a summary."}]
        }
        readmefy.generate_readme(self.api_key, self.dir_path, self.code_files)
        self.assertTrue(os.path.exists("README.md"))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python readmefy-test.py <API_KEY>")
        sys.exit(1)
    api_key = sys.argv[1]
    unittest.main(argv=[""], defaultTest="TestReadmefy", testRunner=None, testLoader=unittest.TestLoader())