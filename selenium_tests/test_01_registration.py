# selenium_tests/test_registration.py
import os
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import unittest
import traceback
import time
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
        logging.FileHandler(log_file, mode='w'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CleanTextTestResult(TextTestResult):
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.pass_count = 0
        self.fail_count = 0
        self.failed_tests = []  # 用於儲存失敗用例的詳細資訊

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
            # 收集失敗用例的詳細資訊
            failure_info = {
                "test_name": test._testMethodName,
                "error_type": str(err[0].__name__),
                "error_message": str(err[1]),
                "stack_trace": ''.join(traceback.format_tb(err[2]))
            }
            self.failed_tests.append(failure_info)
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
            # 收集錯誤用例的詳細資訊
            error_info = {
                "test_name": test._testMethodName,
                "error_type": str(err[0].__name__),
                "error_message": str(err[1]),
                "stack_trace": ''.join(traceback.format_tb(err[2]))
            }
            self.failed_tests.append(error_info)
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
        logger.info(f"\n📌測試結果摘要:")
        logger.info(f"✅通過測試數: {self.pass_count}")
        logger.info(f"❌失敗測試數: {self.fail_count}")
        logger.info(f"📊總測試數: {total}")

    def get_results(self):
        """返回結構化的測試結果，包括失敗用例"""
        total = self.pass_count + self.fail_count
        return {
            "summary": {
                "pass_count": self.pass_count,
                "fail_count": self.fail_count,
                "total_count": total
            },
            "failed_tests": self.failed_tests
        }

class CustomTextTestRunner(unittest.TextTestRunner):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.verbosity = 0

    def run(self, test):
        result = super().run(test)
        if hasattr(result, 'printSummary'):
            result.printSummary()
        return result

class registrationPageTest(unittest.TestCase):
    def setUp(self):
        self.delay_seconds = Config.DELAY_SECONDS  # 使用 Config.DELAY_SECONDS
        chrome_options = Options()
        chrome_options.add_argument("--log-level=3")
        chrome_options.set_capability("goog:loggingPrefs", {"browser": "OFF"})
        #chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(
            options=chrome_options,
            service=Service(Config.CHROMEDRIVER_PATH)  # 使用 Config.CHROMEDRIVER_PATH
        )
        self.driver.get(config.REGISTER_URL)  # 使用 config.BASE_URL
        self.wait = WebDriverWait(self.driver, Config.WAIT_TIMEOUT)  # 使用 Config.WAIT_TIMEOUT
        logger.info(f"設置測試環境: {config.REGISTER_URL}")

    def test_01_01check_registration_button_enabled_after_username_and_password(self):
        try:
            logger.info("開始測試：檢查註冊按鈕是否在輸入帳號密碼後啟用")

            close_button = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//i[contains(@class, 'close-btn')]")
            ))
            if close_button:
                close_button.click()
                print("彈出窗口已關閉")
            else:
                print("未找到關閉按鈕")

            username_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '用户名')]//following-sibling::div//input[@type='text']")))            
            password_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']")))
            email_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '邮箱')]//following-sibling::div//input[@type='text']")))            
            registration_button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), ' 注册 ')]")))

            initial_disabled = "disabled" in registration_button.get_attribute("class")
            logger.debug(f"未輸入任何資料: {'disabled' if initial_disabled else 'enabled'}")
            self.assertTrue(initial_disabled, "註冊按鈕初始狀態應為 disabled")

            username = "cooper001"
            username_input.send_keys(username)
            time.sleep(self.delay_seconds)

            mid_disabled = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), '注册')]")))
            mid_disabled = "disabled" in registration_button.get_attribute("class")
            logger.debug(f"僅輸入帳號: {'disabled' if mid_disabled else 'enabled'}")
            self.assertTrue(mid_disabled, "僅輸入用戶名後，註冊按鈕應仍為 disabled")

            password = "1234Qwer"
            password_input.send_keys(password)
            time.sleep(self.delay_seconds)

            final_disabled = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), '注册')]")))
            final_disabled = "disabled" in registration_button.get_attribute("class")
            logger.debug(f"全部輸入: {'disabled' if final_disabled else 'enabled'}")
            self.assertFalse(final_disabled, "輸入用戶名和密碼並同意條款後，註冊按鈕應為 enabled")

            logger.info("測試用例通過：登入按鈕檢查成功")
        except Exception as e:
            logger.error(f"測試用例失敗：登入按鈕檢查 - 錯誤: {str(e)}")
            self.fail()

    def test_01_02_registration(self):
        try:
            logger.info("開始測試：帳號密碼正確註冊")

            close_button = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//i[contains(@class, 'close-btn')]")
            ))
            if close_button:
                close_button.click()
                print("彈出窗口已關閉")
            else:
                print("未找到關閉按鈕")

            username_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '用户名')]//following-sibling::div//input[@type='text']")))            
            password = self.driver.find_element(By.XPATH, "//input[@type='password']")
            registration_button = self.driver.find_element(By.XPATH, "//button[contains(text(), '注册')]")
            username_input.send_keys(config.INVALID_USERNAME_PREFIX)
            password.send_keys(config.VALID_PASSWORD)
            registration_button.click()

            success_message = self.wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), '我的钱包')]")))
            self.assertIn("我的钱包", success_message.text)
            logger.info("測試用例通過：帳號密碼正確登入成功")
        except Exception as e:
            logger.error(f"測試用例失敗：帳號密碼正確登入 - 錯誤: {str(e)}")
            self.fail()

    def test_01_03_registration_duplicate(self):
        try:
            logger.info("開始測試：帳號重複無法註冊")

            close_button = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//i[contains(@class, 'close-btn')]")
            ))
            if close_button:
                close_button.click()
                print("彈出窗口已關閉")
            else:
                print("未找到關閉按鈕")

            username_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '用户名')]//following-sibling::div//input[@type='text']")))            
            password = self.driver.find_element(By.XPATH, "//input[@type='password']")
            registration_button = self.driver.find_element(By.XPATH, "//button[contains(text(), '注册')]")
            username_input.send_keys(config.VALID_USERNAME)
            password.send_keys(config.VALID_PASSWORD)
            registration_button.click()

            error_message = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[contains(text(), '该用户名已存在')]")
            ))            
            self.assertIn("该用户名已存在", error_message.text)
            logger.info("測試用例通過：重複帳號無法註冊")
        except Exception as e:
            logger.error(f"測試用例失敗：重複帳號註冊 - 錯誤: {str(e)}")
            self.fail()



    def tearDown(self):
        logger.info("測試結束，關閉瀏覽器")
        self.driver.quit()

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(registrationPageTest)
    runner = CustomTextTestRunner(resultclass=CleanTextTestResult, verbosity=2)
    result = runner.run(suite)
    logger.info("測試運行完成")