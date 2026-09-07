import unittest
from crawl import normalize_url, get_heading_from_html, get_first_paragraph_from_html, get_urls_from_html, get_images_from_html, extract_page_data


class TestCrawl(unittest.TestCase):
    def test_normalize_url_protocol(self) -> None:
        input_url = "https://crawler-test.com/path"
        actual = normalize_url(input_url)
        expected = "crawler-test.com/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_slash(self) -> None:
        input_url = "https://crawler-test.com/path/"
        actual = normalize_url(input_url)
        expected = "crawler-test.com/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_capitals(self) -> None:
        input_url = "https://CRAWLER-TEST.com/path"
        actual = normalize_url(input_url)
        expected = "crawler-test.com/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_http(self) -> None:
        input_url = "http://CRAWLER-TEST.com/path"
        actual = normalize_url(input_url)
        expected = "crawler-test.com/path"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_basic(self):
        input_body = "<html><body><h1>Test Title</h1></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_h2_no_h1(self):
            input_body = "<html><body><h2>Test Title</h2></body></html>"
            actual = get_heading_from_html(input_body)
            expected = "Test Title"
            self.assertEqual(actual, expected)


    def test_get_first_paragraph_from_html_main_priority(self):
        input_body = """<html><body>
        <p>Outside paragraph.</p>
        <main>
            <p>Main paragraph.</p>
        </main>
    </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_first_paragraph_fallback_no_main(self):
            input_body = """<html><body>
            <p>Outside paragraph.</p>
        </body></html>"""
            actual = get_first_paragraph_from_html(input_body)
            expected = "Outside paragraph."
            self.assertEqual(actual, expected)

    def test_get_urls_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="/some_link.html"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/some_link.html"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_multiple_relative(self):
        input_url = "https://crawler-test.com"
        input_body = """
                    <html>
                        <body>
                            <a href="/some_link.html">
                                <span>Boot.dev</span>
                            </a>
                                <a href="/another_link.html">
                                <span>Butt.dev</span>
                            </a>
                        </body>
                    </html>"""
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/some_link.html", "https://crawler-test.com/another_link.html"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="https://crawler-test.com/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

    def test_extract_page_data_basic(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"],
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_h2_no_h1(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h2>Test Title</h2>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"],
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_main_priority(self):
            input_url = "https://crawler-test.com"
            input_body = """<html><body>
                <h2>Test Title</h2>
                <main>
                    <p>This is the first paragraph.</p>
                </main>
                <a href="/link1">Link 1</a>
                <img src="/image1.jpg" alt="Image 1">
            </body></html>"""
            actual = extract_page_data(input_body, input_url)
            expected = {
                "url": "https://crawler-test.com",
                "heading": "Test Title",
                "first_paragraph": "This is the first paragraph.",
                "outgoing_links": ["https://crawler-test.com/link1"],
                "image_urls": ["https://crawler-test.com/image1.jpg"],
            }
            self.assertEqual(actual, expected)

    def test_extract_page_data_h2_no_h1(self):
            input_url = "https://crawler-test.com"
            input_body = """<html><body>
                <h2>Test Title</h2>
                <p>This is the first paragraph.</p>
                <a href="/link1">Link 1</a>
                <img src="/image1.jpg" alt="Image 1">
            </body></html>"""
            actual = extract_page_data(input_body, input_url)
            expected = {
                "url": "https://crawler-test.com",
                "heading": "Test Title",
                "first_paragraph": "This is the first paragraph.",
                "outgoing_links": ["https://crawler-test.com/link1"],
                "image_urls": ["https://crawler-test.com/image1.jpg"],
            }
            self.assertEqual(actual, expected)
    def test_extract_page_data_main_fallback(self):
            input_url = "https://crawler-test.com"
            input_body = """<html><body>
                <h2>Test Title</h2>
                <p>This is the first paragraph.</p>
                <main>
                    This is the main body.
                </main>
                <a href="/link1">Link 1</a>
                <img src="/image1.jpg" alt="Image 1">
            </body></html>"""
            actual = extract_page_data(input_body, input_url)
            expected = {
                "url": "https://crawler-test.com",
                "heading": "Test Title",
                "first_paragraph": "This is the first paragraph.",
                "outgoing_links": ["https://crawler-test.com/link1"],
                "image_urls": ["https://crawler-test.com/image1.jpg"],
            }
            self.assertEqual(actual, expected)

    def test_extract_page_data_links_absolute(self):
                input_url = "https://crawler-test.com"
                input_body = """<html><body>
                    <h2>Test Title</h2>
                    <p>This is the first paragraph.</p>
                    <main>
                        This is the main body.
                    </main>
                    <a href="https://crawler-test.com/link1">Link 1</a>
                    <img src="/image1.jpg" alt="Image 1">
                </body></html>"""
                actual = extract_page_data(input_body, input_url)
                expected = {
                    "url": "https://crawler-test.com",
                    "heading": "Test Title",
                    "first_paragraph": "This is the first paragraph.",
                    "outgoing_links": ["https://crawler-test.com/link1"],
                    "image_urls": ["https://crawler-test.com/image1.jpg"],
                }
                self.assertEqual(actual, expected)

    def test_extract_page_data_images_absolute(self):   
                input_url = "https://crawler-test.com"
                input_body = """<html><body>
                    <h2>Test Title</h2>
                    <p>This is the first paragraph.</p>
                    <main>
                        This is the main body.
                    </main>
                    <a href="https://crawler-test.com/link1">Link 1</a>
                    <img src="https://crawler-test.com/image1.jpg" alt="Image 1">
                </body></html>"""
                actual = extract_page_data(input_body, input_url)
                expected = {
                    "url": "https://crawler-test.com",
                    "heading": "Test Title",
                    "first_paragraph": "This is the first paragraph.",
                    "outgoing_links": ["https://crawler-test.com/link1"],
                    "image_urls": ["https://crawler-test.com/image1.jpg"],
                }
                self.assertEqual(actual, expected)

    
    def test_extract_page_data_multiple_links_relative(self):   
                input_url = "https://crawler-test.com"
                input_body = """<html><body>
                    <h2>Test Title</h2>
                    <p>This is the first paragraph.</p>
                    <main>
                        This is the main body.
                    </main>
                    <a href="/link1">Link 1</a>
                    <img src="https://crawler-test.com/image1.jpg" alt="Image 1">
                    <a href="/link2">Link 2</a>
                </body></html>"""
                actual = extract_page_data(input_body, input_url)
                expected = {
                    "url": "https://crawler-test.com",
                    "heading": "Test Title",
                    "first_paragraph": "This is the first paragraph.",
                    "outgoing_links": ["https://crawler-test.com/link1", "https://crawler-test.com/link2"],
                    "image_urls": ["https://crawler-test.com/image1.jpg"],
                }
                self.assertEqual(actual, expected)
if __name__ == "__main__":
    unittest.main()
