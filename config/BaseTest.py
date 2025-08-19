import os
import unittest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from config.config import Config

logger = logging.getLogger(__name__)
config = Config.get_current_config()

class BaseTest(unittest.TestCase):
    def setUp(self):
        # 延遲設定
        self.delay_seconds = Config.DELAY_SECONDS

        # 1. 配置 ChromeOptions
        chrome_options = Options()
        # 明確指定本機 Chrome.app 二進制（138 版）
        chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        # 窗口大小 & headless 引擎
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--log-level=3")
        # 隱藏 automation 特徵
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        # 覆蓋 User-Agent：去掉 HeadlessChrome 標識
        normal_ua = (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "Chrome/138.0.7204.94 Safari/537.36"
        )
        chrome_options.add_argument(f"--user-agent={normal_ua}")
        # 強制 browserName 為 chrome，避免部分工具識別為 headless
        chrome_options.set_capability("browserName", "chrome")

        # 2. 使用 config.py 中指定的 ChromeDriver 路徑
        logger.info(f"🚀 使用固定 ChromeDriver 路徑: {Config.get_chromedriver_path()}")
        service = Service(Config.get_chromedriver_path())

        # 3. 啟動 WebDriver
        try:
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            logger.info("✅ WebDriver 成功初始化")
        except Exception as e:
            logger.error(f"❌ WebDriver 初始化失敗: {e}")
            raise
        self.wait = WebDriverWait(self.driver, Config.WAIT_TIMEOUT)

        # 4. （可選）上報版本到後端
        try:
            caps = self.driver.capabilities
            payload = {
                "browserVersion": caps.get("browserVersion"),
                "chromedriverVersion": caps.get("chrome", {}).get("chromedriverVersion", "").split(" ", 1)[0],
                "testSuite": self.__class__.__name__
            }
            # 替換成你們後端版本上報接口
            logger.info(f"上報版本: {payload}")
            # requests.post("https://your-backend/api/test/version", json=payload, timeout=5)
        except Exception as e:
            logger.warning(f"版本上報失敗: {e}")

        # 5. 導航至測試頁面 (子類可設 self.url)
        if hasattr(self, "url") and self.url:
            self.driver.get(self.url)
            logger.info(f"導航至: {self.url}")

    def tearDown(self):
        logger.info("🧹 測試結束，關閉瀏覽器")
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)