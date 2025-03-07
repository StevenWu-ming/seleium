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

    def generate_random_username(self, length=8):
        letters_and_digits = string.ascii_lowercase + string.digits
        random_username = ''.join(random.choice(letters_and_digits) for _ in range(length))
        return f"{config.INVALID_USERNAME_PREFIX}{random_username}"

    def test_01_check_login_button_enabled_after_username_and_password(self):
        try:
            logger.info("開始測試：檢查登入按鈕是否在輸入帳號密碼後啟用")
            username_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@maxlength='18']")))
            password_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']")))
            login_button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), '登录')]")))

            initial_disabled = "disabled" in login_button.get_attribute("class")
            logger.debug(f"未輸入任何資料: {'disabled' if initial_disabled else 'enabled'}")

            username = "cooper001"
            username_input.send_keys(username)
            time.sleep(self.delay_seconds)

            mid_login_button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), '登录')]")))
            mid_disabled = "disabled" in mid_login_button.get_attribute("class")
            logger.debug(f"僅輸入帳號: {'disabled' if mid_disabled else 'enabled'}")

            password = "1234Qwer"
            password_input.send_keys(password)
            time.sleep(self.delay_seconds)

            final_login_button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), '登录')]")))
            final_disabled = "disabled" in final_login_button.get_attribute("class")
            logger.debug(f"全部輸入: {'disabled' if final_disabled else 'enabled'}")

            self.assertFalse(final_disabled, "Login button should be enabled after username and password input")
            logger.info("測試用例通過：登入按鈕檢查成功")
        except Exception as e:
            logger.error(f"測試用例失敗：登入按鈕檢查 - 錯誤: {str(e)}")
            self.fail()

    def test_02_successful_login(self):
        try:
            logger.info("開始測試：帳號密碼正確登入")
            username = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@maxlength='18']")))
            password = self.driver.find_element(By.XPATH, "//input[@type='password']")
            login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), '登录')]")
            username.send_keys(config.VALID_USERNAME)
            password.send_keys(config.VALID_PASSWORD)
            login_button.click()

            success_message = self.wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), '我的钱包')]")))
            self.assertIn("我的钱包", success_message.text)
            logger.info("測試用例通過：帳號密碼正確登入成功")
        except Exception as e:
            logger.error(f"測試用例失敗：帳號密碼正確登入 - 錯誤: {str(e)}")
            self.fail()

    def test_03_invalid_credentials(self):
        try:
            logger.info("開始測試：帳號密碼錯誤登入")
            username = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@maxlength='18']")))
            password = self.driver.find_element(By.XPATH, "//input[@type='password']")
            login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), '登录')]")
            random_username = self.generate_random_username()
            username.send_keys(random_username)
            password.send_keys(config.VALID_PASSWORD)
            login_button.click()

            error_message = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[contains(text(), '您输入的密码不正确')]")
            ))
            self.assertIn("您输入的密码不正确", error_message.text)
            logger.info("測試用例通過：帳號密碼錯誤無法登入成功")
        except Exception as e:
            logger.error(f"測試用例失敗：帳號密碼錯誤登入 - 錯誤: {str(e)}")
            self.fail()

    def test_04_phonenumber_login(self):
        try:
            logger.info("開始測試：手機號碼登入")
            print(f"Page title: {self.driver.title}")

            phone_tab = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'tab') and contains(text(), '手机')]")))
            logger.debug("Found phone tab, clicking...")
            phone_tab.click()

            phone_dropdown = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'phone-box')]//button[contains(@class, 'select-btn')]")))
            logger.debug("Found phone dropdown, clicking...")
            phone_dropdown.click()

            search_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='搜索' or contains(@class, 'search')]")))
            search_input.send_keys("+86")
            china_option = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '+86')] | //li[contains(text(), '+86')]")))
            logger.debug("Found '+86' option, clicking...")
            china_option.click()

            phonenumber = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='number']")))
            password = self.driver.find_element(By.XPATH, "//input[@type='password']")
            login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), '登录')]")
            phonenumber.send_keys(config.PHONE_NUMBER)
            password.send_keys(config.VALID_PASSWORD)
            login_button.click()

            try:
                success_message = self.wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), '我的钱包')]")))
                self.assertIn("我的钱包", success_message.text)
                logger.info("測試用例通過：手機號碼直接登入成功")
                self.assertIsNotNone(success_message)
                return

            except Exception as direct_login_error:
                logger.warning(f"直接登入失敗，可能需要驗證碼: {str(direct_login_error)}")

            get_code_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'input-group-txt') and contains(@class, 'get-code')]")))
            logger.debug("Clicking get code button...")
            get_code_button.click()

            success_toast = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'toast-text')]//p[contains(text(), '成功')]")))
            logger.debug("Verification code sent successfully")

            verify_code_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'input-group')]//input[@type='number' and @maxlength='6']")))
            verify_code_input.send_keys(config.VERIFY_CODE)

            success_message = self.wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), '我的钱包')]")))
            self.assertIn("我的钱包", success_message.text)
            logger.info("測試用例通過：手機號碼經由驗證碼登入成功")
            self.assertIsNotNone(success_message)

        except Exception as e:
            logger.error(f"測試用例失敗：手機號碼登入 - 錯誤: {str(e)}")
            self.fail()

    def test_05_mail_login(self):
        try:
            logger.info("開始測試：郵箱登入")
            phone_tab = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'tab') and contains(text(), ' 邮箱 ')]")))
            phone_tab.click()

            email = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='text']")))
            password = self.driver.find_element(By.XPATH, "//input[@type='password']")
            login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), '登录')]")
            email.send_keys(config.EMAIL)
            password.send_keys(config.VALID_PASSWORD)
            login_button.click()

            success_message = self.wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), '我的钱包')]")))
            self.assertIn("我的钱包", success_message.text)
            logger.info("測試用例通過：郵箱登入成功")
            self.assertIsNotNone(success_message)

        except Exception as e:
            logger.error(f"測試用例失敗：郵箱登入 - 錯誤: {str(e)}")
            self.fail()

    def tearDown(self):
        logger.info("測試結束，關閉瀏覽器")
        self.driver.quit()

if __name__ == "__main__":
    unittest.main(verbosity=2)