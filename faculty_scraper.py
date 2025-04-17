import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
from datetime import datetime
import json
import sys

# List of faculty profile URLs to scrape
FACULTY_URLS = [
    "https://dsu.edu.in/girisha-g-s",
    "https://dsu.edu.in/rajesh-t-m",
    "https://dsu.edu.in/dr-praveen",
    "https://dsu.edu.in/dr-arunkumar",
    "https://dsu.edu.in/dr-savitha"
]

async def scrape_faculty_profiles():
    """Scrape faculty profile pages and store the markdown content."""
    config = CrawlerRunConfig(
        deep_crawl_strategy=BFSDeepCrawlStrategy(
            max_depth=0,
            include_external=False
        ),
        scraping_strategy=LXMLWebScrapingStrategy(),
        verbose=True
    )
    
    all_faculty_data = []
    
    async with AsyncWebCrawler() as crawler:
        for url in FACULTY_URLS:
            print(f"\nScraping {url}...")
            results = await crawler.arun(url, config=config)
            
            if results and len(results) > 0:
                faculty_data = {
                    "url": url,
                    "markdown_content": results[0].markdown,
                    "timestamp": datetime.now().isoformat()
                }
                all_faculty_data.append(faculty_data)
                print(f"Successfully scraped {url}")
            else:
                print(f"Failed to scrape {url}")
    
    # Save the combined data to a JSON file
    output_file = "faculty_data.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_faculty_data, f, indent=4, ensure_ascii=False)
    
    print(f"\nScraping completed. Data saved to {output_file}")
    print(f"Total faculty profiles scraped: {len(all_faculty_data)}")

def run_scraper():
    """Run the scraper, handling different environments."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    if 'ipykernel' in sys.modules:
        return loop.run_until_complete(scrape_faculty_profiles())
    else:
        return asyncio.run(scrape_faculty_profiles())

if __name__ == "__main__":
    run_scraper() 