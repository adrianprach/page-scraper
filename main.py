import sys
import asyncio
import time

from async_crawler import AsyncCrawler


async def crawl_site_async(url):
    async with AsyncCrawler(url, 20, 2) as site:
        return await site.crawl()

async def main():
    argv_len = len(sys.argv)
    if argv_len < 2:
        print("no website provided")
        return sys.exit(1)
    if argv_len > 2:
        print("too many arguments provided")
        return sys.exit(1)
    base_url = sys.argv[1]
    print(f"starting crawl of {base_url}")
    start = time.perf_counter()
    crawled = await crawl_site_async(base_url)
    elapsed = time.perf_counter() - start
    print(crawled)
    print(f"Elapsed: {elapsed:6f}ms")
    return sys.exit(0)


if __name__ == "__main__":
    asyncio.run(main())
    
