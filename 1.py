import asyncio
import base64
import os
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode

FACULTY_URLS = [
    "https://dsu.edu.in/girisha-g-s",
    "https://dsu.edu.in/rajesh-t-m",
    "https://dsu.edu.in/dr-praveen",
    "https://dsu.edu.in/dr-arunkumar",
    "https://dsu.edu.in/dr-savitha"
]

async def main():
    browser_conf = BrowserConfig(headless=True)

    async with AsyncWebCrawler(config=browser_conf) as crawler:
        results = await crawler.arun_many(
            urls=FACULTY_URLS,
            config=CrawlerRunConfig(stream=False,pdf=True,screenshot=True)  # Default behavior
        )
        i=0
        for res in results:
            name = res.url.split("/")[-1]
            #print(f"Markdown for {name}:\n", result.markdown)
                    
            if res.screenshot:
                os.makedirs("screenshots", exist_ok=True)
                with open(f"screenshots/{name}.png", "wb") as f:
                    f.write(base64.b64decode(res.screenshot))

if __name__ == "__main__":
    asyncio.run(main())
