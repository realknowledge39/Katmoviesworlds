import json, os, unittest
from unittest.mock import patch
from scripts.shrinkearn_adapter import create_short_link, ShrinkEarnError

class FakeResponse:
    def __init__(self, body): self.body = body
    def __enter__(self): return self
    def __exit__(self, *args): pass
    def read(self, limit): return self.body

class AdapterTests(unittest.TestCase):
    @patch.dict(os.environ, {"SHRINKEARN_API_KEY": "test-key"})
    @patch("scripts.shrinkearn_adapter.urlopen")
    def test_json_success(self, mock_open):
        mock_open.return_value = FakeResponse(json.dumps({"status":"success","shortenedUrl":"https://srnky.com/demo"}).encode())
        self.assertEqual(create_short_link("https://example.com/movie"), "https://srnky.com/demo")
    @patch.dict(os.environ, {}, clear=True)
    def test_missing_key(self):
        with self.assertRaises(ShrinkEarnError): create_short_link("https://example.com")
    @patch.dict(os.environ, {"SHRINKEARN_API_KEY":"test"})
    def test_rejects_invalid_url(self):
        with self.assertRaises(ValueError): create_short_link("javascript:alert(1)")

if __name__ == "__main__": unittest.main()
