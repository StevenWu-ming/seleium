import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from config.config import Config, config  # 導入 Config 和 config
import logging

logger = logging.getLogger(__name__)

class BaseTest(unittest.TestCase):
    def setUp(self):
        self.delay_seconds = Config.DELAY_SECONDS
        chrome_options = Options()
        chrome_options.add_argument("--log-level=3")
        chrome_options.set_capability("goog:loggingPrefs", {"browser": "OFF"})
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(
            options=chrome_options,
            service=Service(Config.CHROMEDRIVER_PATH)
        )
        self.wait = WebDriverWait(self.driver, Config.WAIT_TIMEOUT)
        # self.driver.set_window_position(2000, 100)

        if hasattr(self, "url") and self.url:  # 只有在子類別有設定 `self.url` 才會載入
            self.driver.get(self.url)
            logger.info(f"設置測試環境: {self.url}")

    def tearDown(self):
        logger.info("測試結束，關閉瀏覽器")
        self.driver.quit()
