###設置Selenium自動化測試環境，初始化Chrome瀏覽器，支援平行測試，包含無頭模式與日誌管理
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from config.config import Config
import logging

logger = logging.getLogger(__name__)
config = Config.get_current_config()

class BaseTest(unittest.TestCase):
    def setUp(self):
        self.delay_seconds = Config.DELAY_SECONDS

        chrome_options = Options()
        chrome_options.add_argument("--log-level=3")
        chrome_options.set_capability("goog:loggingPrefs", {"browser": "OFF"})
        chrome_options.add_argument("--headless")  # ✅ Headless 模式
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")  # 避免某些系統 GPU 問題

        self.driver = webdriver.Chrome(
            options=chrome_options,
            service=Service(Config.CHROMEDRIVER_PATH)
        )
        self.wait = WebDriverWait(self.driver, Config.WAIT_TIMEOUT)

        # ✅ 每個 test case 自己開自己的 driver，所以可平行
        if hasattr(self, "url") and self.url:
            self.driver.get(self.url)
            logger.info(f"設置測試環境: {self.url}")

    def tearDown(self):
        logger.info("測試結束，關閉瀏覽器")
        self.driver.quit()
