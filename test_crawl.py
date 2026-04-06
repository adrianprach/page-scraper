from crawl import extract_page_data, get_first_paragraph_from_html, get_heading_from_html, get_images_from_html_relative, get_urls_from_html, normalize_url
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

    def test_get_heading_from_html(self):
        input_html = """
        <html>
          <body>
            <h1>Welcome to Boot.dev</h1>
            <main>
              <p>Learn to code by building real projects.</p>
              <p>This is the second paragraph.</p>
            </main>
          </body>
        </html>
        """
        actual = get_heading_from_html(input_html)
        expected = "Welcome to Boot.dev"
        self.assertEqual(actual, expected)

    def test_get_second_heading_from_html(self):
        input_html = """
        <html>
          <body>
            <h2>This is second heading.</h2>
            <main>
              <p>Learn to code by building real projects.</p>
              <p>This is the second paragraph.</p>
            </main>
          </body>
        </html>
        """
        actual = get_heading_from_html(input_html)
        expected = "This is second heading."
        self.assertEqual(actual, expected)

    def test_get_first_heading_from_html(self):
        input_html = """
        <html>
          <body>
            <h1>This is first.</h1>
            <h2>This is second heading.</h2>
            <main>
              <p>Learn to code by building real projects.</p>
              <p>This is the second paragraph.</p>
            </main>
          </body>
        </html>
        """
        actual = get_heading_from_html(input_html)
        expected = "This is first."
        self.assertEqual(actual, expected)


    def test_get_first_paragraph_from_html(self):
        input_html = """
        <html>
          <body>
            <h1>Welcome to Boot.dev</h1>
            <main>
              <p>Learn to code by building real projects.</p>
              <p>This is the second paragraph.</p>
            </main>
          </body>
        </html>
        """
        actual = get_first_paragraph_from_html(input_html)
        expected = "Learn to code by building real projects."
        self.assertEqual(actual, expected)

    def test_get_main_paragraph_from_html(self):
        input_html = """
        <html>
          <body>
            <h1>Welcome to Boot.dev</h1>
            <p>Learn to code by building real projects.</p>
            <main>
              <p>This is the second paragraph.</p>
            </main>
          </body>
        </html>
        """
        actual = get_first_paragraph_from_html(input_html)
        expected = "This is the second paragraph."
        self.assertEqual(actual, expected)


    def test_get_fallback_paragraph_from_html(self):
        input_html = """
        <html>
          <body>
            <h1>Welcome to Boot.dev</h1>
            <p>Learn to code by building real projects.</p>
            <main>
              <p></p>
            </main>
          </body>
        </html>
        """
        actual = get_first_paragraph_from_html(input_html)
        expected = "Learn to code by building real projects."
        self.assertEqual(actual, expected)

    def test_get_single_url_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a><main><a href="/blog">another link</a></main></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com", "https://crawler-test.com/blog"]
        self.assertEqual(actual, expected)

    def test_get_empty_url_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    def test_get_images_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html_relative(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_empty_image_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body></body></html>'
        actual = get_images_from_html_relative(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    def test_get_multiple_images_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/pic.png" /><img src="https://crawler-test.com/cover.webp" alt="cover photo"></body></html>'
        actual = get_images_from_html_relative(input_body, input_url)
        expected = ["https://crawler-test.com/pic.png", "https://crawler-test.com/cover.webp"]
        self.assertEqual(actual, expected)

    def test_extract_page_data_basic(self):
        input_url = "https://crawler-test.com"
        input_body = '''<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"]
        }
        self.assertEqual(actual, expected)
   

if __name__ == '__main__':
    unittest.main()
