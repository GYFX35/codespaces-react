import unittest
from unittest.mock import patch, Mock
from .fake_news_detector import analyze_url_for_fake_news

class TestFakeNewsDetector(unittest.TestCase):

    @patch('urllib.request.urlopen')
    def test_fake_news_url(self, mock_urlopen):
        # Mock the response for a fake news URL
        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = b'<html><head><title>Fake News</title></head><body>This is a shocking story!</body></html>'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        url = "http://abcnews.com.co/news/breaking-news-report.html"
        result = analyze_url_for_fake_news(url)
        self.assertGreater(result["score"], 0)
        self.assertIn("Domain 'abcnews.com.co' is a known source of fake news.", result["indicators_found"])

    @patch('urllib.request.urlopen')
    def test_legitimate_news_url(self, mock_urlopen):
        # Mock the response for a legitimate news URL
        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = b'<html><head><title>Real News</title></head><body>This is a real news story.</body></html>'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        url = "https://www.bbc.com/news"
        result = analyze_url_for_fake_news(url)
        self.assertEqual(result["score"], 0)
        self.assertEqual(len(result["indicators_found"]), 0)

if __name__ == '__main__':
    unittest.main()
