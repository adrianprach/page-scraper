from crawl import normalize_url
import unittest

class TestNormalizeUrl(unittest.TestCase):

    def test_http(self):
        input_url = "http://www.boot.dev"
        actual = normalize_url(input_url)
        expected = "www.boot.dev"
        self.assertEqual(actual, expected)
    
    def test_https(self):
        input_url = "https://www.boot.dev"
        actual = normalize_url(input_url)
        expected = "www.boot.dev"
        self.assertEqual(actual, expected)

    def test_https_suffix(self):
        input_url = "https://www.boot.dev/blog"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog"
        self.assertEqual(actual, expected)



if __name__ == '__main__':
    unittest.main()
