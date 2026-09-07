from urllib.parse import urlsplit, urljoin
from bs4 import BeautifulSoup, Tag
from typing import TypedDict
import requests


class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]


def normalize_url(url: str) -> str:
    parsed_url = urlsplit(url)
    full_path = f"{parsed_url.netloc}{parsed_url.path}"
    full_path = full_path.rstrip("/")
    return full_path.lower()

def get_heading_from_html(html: str) -> str:

    soup = BeautifulSoup(html, 'html.parser')
    heading = soup.find('h1')

    if not heading:
        heading = soup.find('h2')

    if not heading:
        return ""

    return heading.get_text(strip=True) if isinstance(heading, Tag) else ""

def get_first_paragraph_from_html(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    first_paragraph = soup.find('p')
    main_paragraph = soup.find('main')

    if main_paragraph != None:
        main_paragraph = main_paragraph.find('p')
        if main_paragraph != None:
            if isinstance(main_paragraph, Tag):
                return main_paragraph.get_text(strip=True)

    return first_paragraph.get_text(strip=True) if isinstance(first_paragraph, Tag) else ""


def get_urls_from_html(html, base_url):

    soup = BeautifulSoup(html, 'html.parser')
    hrefs = []
    links = soup.find_all('a')

    for link in links:
        hrefs.append(urljoin(base_url, link.get('href')))

    return hrefs

def get_images_from_html(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    srcs = []
    imgs = soup.find_all('img')
    
    for img in imgs:
        srcs.append(urljoin(base_url, img.get('src')))
    
    return srcs

def extract_page_data(html: str, page_url: str):
    heading = get_heading_from_html(html)
    first_paragraph = get_first_paragraph_from_html(html)
    outgoing_links = get_urls_from_html(html, page_url)
    image_urls = get_images_from_html(html, page_url)

    return {
        "url": page_url,
        "heading": heading,
        "first_paragraph": first_paragraph,
        "outgoing_links": outgoing_links,
        "image_urls": image_urls,

    }



    
def get_html(url):
   
    try:
        response =  requests.get(url, headers={"User-Agent": "BootCrawler/1.0"})
    except Exception as e:
        raise Exception(f"Network error: {e}")

    
    if response.status_code >= 400:
        raise Exception(f"Error Status Code Returned: {response.status_code}")
    
    if response.headers['content-type'] != 'text/html':
        raise Exception(f"Content-type returned not 'text/html': {r.headers['content-type']}")

    print(response.text)




  

