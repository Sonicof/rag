from shutil import which
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

BOT_NAME = "college_scraper"

SPIDER_MODULES = ["college_scraper.spiders"]
NEWSPIDER_MODULE = "college_scraper.spiders"

ROBOTSTXT_OBEY = True

# Enable Selenium Middleware
DOWNLOADER_MIDDLEWARES = {
    "scrapy_selenium.SeleniumMiddleware": 800
}

# Set up Chrome WebDriver using WebDriver Manager
SELENIUM_DRIVER_NAME = "chrome"

# Chrome Options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--remote-debugging-port=9222")

# Fix for `NoneType` error
SELENIUM_DRIVER_ARGUMENTS = ["--headless", "--no-sandbox", "--disable-dev-shm-usage"]

# Set Selenium WebDriver options
SELENIUM_DRIVER_KWARGS = {
    "service": Service(ChromeDriverManager().install()),
    "options": chrome_options
}

# Set encoding
FEED_EXPORT_ENCODING = "utf-8"
