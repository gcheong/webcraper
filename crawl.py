from urllib.parse import urlsplit, urljoin
from bs4 import BeautifulSoup, Tag
from typing import TypedDict
import requests
import asyncio
import aiohttp
from types import TracebackType



class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]

class AsyncCrawler:
    base_url: str
    base_domain:str
    page_data:dict[str, PageData]
    lock:asyncio.Lock
    max_concurrency:int
    semaphore:asyncio.Semaphore
    session:aiohttp.ClientSession

    def __init__(self, base_url:str) -> None:
        self.base_url = base_url
        self.base_domain = urlsplit(base_url).netloc
        self.page_data: dict[str, PageData] = {}
        self.lock = asyncio.Lock()
        self.max_concurrency = 1
        self.semaphore = asyncio.Semaphore(self.max_concurrency)
        self.session: aiohttp.ClientSession | None = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self


    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if self.session is not None:
            await self.session.close()

    async def add_page_visit(self, normalized_url):
        async with self.lock:
            if normalize_url in self.page_data:
                return False
            else:
                return True

    async def get_html(self, url):  

        if self.session is None:
            return None
   
        try:

            response =  requests.get(url, headers={"User-Agent": "BootCrawler/1.0"})
        except Exception as e:
            raise Exception(f"Network error: {e}")

    
        if response.status_code >= 400:
            raise Exception(f"Error Status Code Returned: {response.status_code}")

        content_type = response.headers.get("content-type", "")

        if "text/html" not in content_type:
            raise Exception(f"got non-HTML response: {content_type}")

        return response.text


    


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

    content_type = response.headers.get("content-type", "")

    if "text/html" not in content_type:
        raise Exception(f"got non-HTML response: {content_type}")

    return response.text

def crawl_page(base_url, current_url=None, page_data=None):

    if page_data == None:
        page_data = {}
    
    if current_url == None:
        current_url = base_url


    parsed_current_url = urlsplit(current_url)
    parsed_base_url = urlsplit(base_url)

    if parsed_current_url.netloc != parsed_current_url.netloc:
        return

    normalized_current_url = normalize_url(current_url)

    if normalized_current_url in page_data:
        return

    this_page_html = ""
    try:
        this_page_html = get_html(current_url)

    except Exception as e:
        print(f"Received exception when trying to get html: {e}")

    print(f"Html Received from {current_url}:")
    print(this_page_html)

    this_page_data = extract_page_data(this_page_html,current_url)

    page_data[current_url] = this_page_data

    for url in this_page_data['outgoing_links']:
        crawl_page(base_url, url, page_data)
    
    
        



  

