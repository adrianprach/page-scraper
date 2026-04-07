import os
import sys
import asyncio
import time
import json

from async_crawler import AsyncCrawler


async def crawl_site_async(url, max_concurrency, max_pages):
    async with AsyncCrawler(url, max_concurrency, max_pages) as site:
        return await site.crawl()

def write_json_report(page_data, filename="report.json"):
    if not isinstance(page_data, dict):
        raise Exception("Not a valid dict!")
    crawled_page_data = page_data.values()
    result = sorted(crawled_page_data, key=lambda x: x.get('url'))
    with open(filename, "w") as file:
        file.write(json.dumps(obj=result, indent=2))

async def main():
    max_concurrency = 5
    max_pages = 5
    argv_len = len(sys.argv)
    if argv_len < 2:
        print("no website provided")
        return sys.exit(1)
    if argv_len > 4:
        print("too many arguments provided")
        return sys.exit(1)
    if argv_len == 4:
        max_concurrency = sys.argv[2]
        max_pages = sys.argv[3]

    base_url = sys.argv[1]
    print(f"starting crawl of {base_url}, max_concurrency: {max_concurrency}, max_pages: {max_pages}")
    start = time.perf_counter()
    crawled = await crawl_site_async(base_url, int(max_concurrency), int(max_pages))
    elapsed = time.perf_counter() - start
    print(crawled)
    print(json.dumps(obj=crawled, indent=2), f"Page crawled: {crawled.keys()}")
    write_json_report(crawled)
    print(f"\n\nPage crawled: {crawled.keys()}")
    print(f"Elapsed: {elapsed:6f}ms")
    return sys.exit(0)


if __name__ == "__main__":
    asyncio.run(main())
    
