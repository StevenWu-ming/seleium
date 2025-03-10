# selenium_tests/test_login.py
import os
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import unittest
import time
import random
import string
from unittest.runner import TextTestResult
from config import Config, config  # 導入 Config 和 config

# 設置日誌文件路徑為 selenium_tests/test_log.log
log_dir = os.path.dirname(__file__)  # 獲取當前腳本所在目錄 (selenium_tests)
log_file = os.path.join(log_dir, 'test_log.log')  # 直接放在 selenium_tests 根目錄

# 配置日誌，調整級別為 INFO
logging.basicConfig(
    level=logging.INFO,  # 改為 INFO 級別
    format='%(asctime)s - %(levelname)s - [%(name)s] %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CleanTextTestResult(TextTestResult):
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.pass_count = 0
        self.fail_count = 0

    def addSuccess(self, test):
        super().addSuccess(test)
        self.pass_count += 1
        logger.info(f"測試用例通過: {test._testMethodName}")
        if self.showAll:
            self.stream.write('')
        elif self.dots:
            self.stream.write('')
            self.stream.flush()

    def addFailure(self, test, err):
        if test not in self.failures:
            super().addFailure(test, err)
            self.fail_count += 1
        logger.error(f"測試用例失敗: {test._testMethodName} - 錯誤: {str(err[1])}")
        if self.showAll:
            self.stream.write('')
        elif self.dots:
            self.stream.write('')
            self.stream.flush()

    def addError(self, test, err):
        if test not in self.errors:
            super().addError(test, err)
            self.fail_count += 1
        logger.error(f"測試用例錯誤: {test._testMethodName} - 錯誤: {str(err[1])}")
        if self.showAll:
            self.stream.write('')
        elif self.dots:
            self.stream.write('')
            self.stream.flush()

    def printErrors(self):
        pass

    def printSummary(self):
        total = self.pass_count + self.fail_count
        logger.info(f"\n測試結果摘要:")
        logger.info(f"通過測試數: {self.pass_count}")
        logger.info(f"失敗測試數: {self.fail_count}")
        logger.info(f"總測試數: {total}")

class CustomTextTestRunner(unittest.TextTestRunner):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.verbosity = 0

    def run(self, test):
        result = super().run(test)
        if hasattr(result, 'printSummary'):
            result.printSummary()
        return result

class LoginPageTest(unittest.TestCase):
    def setUp(self):
        self.delay_seconds = Config.DELAY_SECONDS  # 使用 Config.DELAY_SECONDS
        chrome_options = Options()
        chrome_options.add_argument("--log-level=3")
        chrome_options.set_capability("goog:loggingPrefs", {"browser": "OFF"})
        # chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(
            options=chrome_options,
            service=Service(Config.CHROMEDRIVER_PATH)  # 使用 Config.CHROMEDRIVER_PATH
        )
        self.driver.get(config.BASE_URL)  # 使用 config.BASE_URL
        self.wait = WebDriverWait(self.driver, Config.WAIT_TIMEOUT)  # 使用 Config.WAIT_TIMEOUT
        logger.info(f"設置測試環境: {config.BASE_URL}")

    
    def test_03_01_mail_wronglogin(self):
        try:
            logger.info("開始測試：郵箱登入")
            phone_tab = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'tab') and contains(text(), ' 邮箱 ')]")))
            phone_tab.click()

            email = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='text']")))
            password = self.driver.find_element(By.XPATH, "//input[@type='password']")
            login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), '登录')]")
            email.send_keys(config.INVALID_EMAIL)
            password.send_keys(config.VALID_PASSWORD)
            login_button.click()

            error_message = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[contains(text(), '邮箱与密码不匹配')]")
            ))
            logger.debug("Found error message for invalid email ")
            
            # 驗證錯誤訊息
            self.assertIn("邮箱与密码不匹配", error_message.text)  # 根據實際的錯誤訊息文字調整
            logger.info("測試用例通過：錯誤郵箱登入測試")
            self.assertIsNotNone(error_message)

        except Exception as e:
            logger.error(f"測試用例失敗：錯誤郵箱登入測試 - 錯誤: {str(e)}")
            self.fail()
    
    def tearDown(self):
        logger.info("測試結束，關閉瀏覽器")
        self.driver.quit()

if __name__ == "__main__":
    logger.info(f"開始運行測試，當前環境: {config.BASE_URL}")
    suite = unittest.TestLoader().loadTestsFromTestCase(LoginPageTest)
    runner = CustomTextTestRunner(resultclass=CleanTextTestResult, verbosity=0)
    result = runner.run(suite)
    logger.info("測試運行完成")