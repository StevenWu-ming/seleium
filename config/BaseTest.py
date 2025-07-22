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
        # 延迟设定
        self.delay_seconds = Config.DELAY_SECONDS

        # 1. 配置 ChromeOptions
        chrome_options = Options()
        # 明确指定本机 Chrome.app 二进制（138 版）
        chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        # 窗口大小 & headless 引擎
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--log-level=3")
        # 隐藏 automation 特征
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        # 覆盖 User-Agent：去掉 HeadlessChrome 标识
        normal_ua = (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/138.0.7204.94 Safari/537.36"
        )
        chrome_options.add_argument(f"--user-agent={normal_ua}")
        # 强制 browserName 为 chrome，避免部分工具识别为 headless
        chrome_options.set_capability("browserName", "chrome")

        # 2. 下载并安装对应的 ChromeDriver (138)
        logger.info("🚀 使用 webdriver_manager 获取 ChromeDriver")
        driver_path = ChromeDriverManager().install()
        service = Service(driver_path)

        # 3. 启动 WebDriver
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, Config.WAIT_TIMEOUT)

        # 4. （可选）上报版本到后端
        try:
            caps = self.driver.capabilities
            payload = {
                "browserVersion": caps.get("browserVersion"),
                "chromedriverVersion": caps.get("chrome", {}).get("chromedriverVersion", "").split(" ", 1)[0],
                "testSuite": self.__class__.__name__
            }
            # 替换成你们后端版本上报接口
            logging.info(f"上报版本: {payload}")
            # requests.post("https://your-backend/api/test/version", json=payload, timeout=5)
        except Exception as e:
            logger.warning(f"版本上报失败: {e}")

        # 5. 导航至测试页面 (子类可设 self.url)
        if hasattr(self, "url") and self.url:
            self.driver.get(self.url)
            logger.info(f"导航至: {self.url}")

    def tearDown(self):
        logger.info("🧹 测试结束，关闭浏览器")
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)
