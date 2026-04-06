from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

def get_heading_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    for index in range(6):
        result = soup.find(name=f"h{index+1}")
        if result is None:
            continue
        return result.text
    return ""

def get_first_paragraph_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    primary = soup.find(name="main")
    primary_attempt = primary.find(name="p") if primary is not None else None
    fallback_attempt = soup.find(name="p")
    for attempt in [primary_attempt, fallback_attempt]:
        if attempt is None or len(attempt.text) == 0:
            continue
        return attempt.text
    return ""

def get_urls_from_html(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    urls = soup.find_all(name="a")
    processed_urls = []
    for link in urls:
        processed_urls.append(urljoin(base_url, link.get("href")))
    return processed_urls

def get_images_from_html_relative(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    processed_images = []
    for image in soup.find_all(name="img"):
        processed_images.append(urljoin(base_url, image.get("src")))
    return processed_images

def extract_page_data(html, page_url):
    page_data = dict()
    page_data["url"] = page_url
    page_data["heading"] = get_heading_from_html(html)
    page_data["first_paragraph"] = get_first_paragraph_from_html(html)
    page_data["outgoing_links"] = get_urls_from_html(html, page_url)
    page_data["image_urls"] = get_images_from_html_relative(html, page_url)
    return page_data

def normalize_url(url):
    parsed = urlparse(url)
    return parsed.netloc + parsed.path
