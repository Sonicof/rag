import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class CollegeSpider(scrapy.Spider):
    name = "college"
    allowed_domains = ["dsu.edu.in"]
    start_urls = ["https://www.dsu.edu.in/"]

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                wait_time=10,  # Wait for JavaScript to load
                screenshot=True,  # Debugging: Capture screenshot
                wait_until=EC.presence_of_element_located((By.TAG_NAME, "body"))  # Ensure body is loaded
            )

    def parse(self, response):
        content_type = response.headers.get('Content-Type', b'').decode()
        print(f"[*] Content-Type: {content_type}")

        if "text/html" not in content_type:
            self.logger.warning(f"Skipping non-HTML page: {response.url}")
            return

        # Extract text content
        page_text = response.xpath("//body//text()").getall()
        page_text = " ".join(page_text).strip()

        yield {
            "url": response.url,
            "text": page_text
        }

        # Follow links
        for link in response.css("a::attr(href)").getall():
            absolute_url = response.urljoin(link)
            if absolute_url.startswith("https://www.dsu.edu.in"):
                yield SeleniumRequest(
                    url=absolute_url,
                    callback=self.parse,
                    wait_time=5  # Wait for JavaScript
                )
