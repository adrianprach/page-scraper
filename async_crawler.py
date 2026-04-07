import asyncio
import aiohttp

from crawl import extract_page_data, normalize_url


class AsyncCrawler:
    def __init__(self, base_url, max_concurrency, max_pages):
        self.base_url = base_url
        self.base_domain = normalize_url(base_url)
        self.page_data = dict()
        self.lock = asyncio.Lock()
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.max_pages = max_pages
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(base_url=self.base_url)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
        return self

    async def add_page_visit(self, normalized_url):
        async with self.lock:
            if normalized_url in self.page_data:
                return False
            return True

    async def get_html(self, url):
        try:
            async with self.session.get(
                url, headers={"User-Agent": "BootCrawler/1.0"}
            ) as attempt:
                if attempt.status >= 400:
                    raise Exception(
                        f"fail to fetch {url}, receiving status_code: {attempt.status_code} {attempt.reason}"
                    )
                content_type = attempt.headers.get("content-type")
                if content_type is not None and "html" in content_type:
                    return await attempt.text()
                raise Exception(f"not valid content type: {content_type}")
        except Exception as e:
            raise Exception(f"Got issue fetching {url}: {e}")

    async def get_html_or_empty(self, url):
        try:
            return await self.get_html(url)
        except Exception as e:
            print(e)
            return ""

    async def crawl_page(self, current_url=None):
        base_url = self.base_url
        page_data = self.page_data

        if current_url is None:
            return self.crawl_page(base_url, base_url, page_data)
        if page_data is None:
            page_data = dict()

        url_normalized = normalize_url(current_url)
        same_domain = normalize_url(base_url) in url_normalized

        first_time = await self.add_page_visit(url_normalized)
        if not first_time or (not same_domain):
            return page_data

        tasks = []
        async with self.semaphore:
            page_html = await self.get_html_or_empty(current_url)
            result = extract_page_data(page_html, current_url)
            async with self.lock:
                self.page_data[url_normalized] = result
            for link in result["outgoing_links"]:
                tasks.append(asyncio.create_task(self.crawl_page(link)))
        await asyncio.gather(*tasks)

    async def crawl(self):
        await self.crawl_page(self.base_url)
        return self.page_data

