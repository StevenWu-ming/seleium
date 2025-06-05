import os
import shutil
import unittest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from config.config import Config

logger = logging.getLogger(__name__)
config = Config.get_current_config()



class BaseTest(unittest.TestCase):
    def setUp(self):
        self.delay_seconds = Config.DELAY_SECONDS

        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # ✅ Headless 模式（若要看視覺效果可關掉這行）
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--log-level=3")
        chrome_options.set_capability("goog:loggingPrefs", {"browser": "OFF"})

        logger.info("🚀 啟動 webdriver_manager，檢查快取或下載 ChromeDriver")
        downloaded_driver_path = ChromeDriverManager().install()

        # ✅ 若自定路徑不存在，就複製一次
        if not os.path.exists(Config.CHROMEDRIVER_PATH):
            os.makedirs(os.path.dirname(Config.CHROMEDRIVER_PATH), exist_ok=True)
            shutil.copy(downloaded_driver_path, Config.CHROMEDRIVER_PATH)
            os.chmod(Config.CHROMEDRIVER_PATH, 0o755)
            logger.info(f"📥 複製 ChromeDriver 至指定路徑: {Config.CHROMEDRIVER_PATH}")
        else:
            logger.info(f"✅ 使用已存在的 ChromeDriver 路徑: {Config.CHROMEDRIVER_PATH}")

        # ✅ 初始化 driver
        self.driver = webdriver.Chrome(
            service=Service(Config.CHROMEDRIVER_PATH),
            options=chrome_options
        )

        self.wait = WebDriverWait(self.driver, Config.WAIT_TIMEOUT)

        if hasattr(self, "url") and self.url:
            self.driver.get(self.url)
            logger.info(f"🌐 導航至指定測試頁面: {self.url}")

    def tearDown(self):
        logger.info("🧹 測試結束，關閉瀏覽器")
        self.driver.quit()
