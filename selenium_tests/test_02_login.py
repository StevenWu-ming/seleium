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
from test_utils import CleanTextTestResult, CustomTextTestRunner
from concurrent.futures import ThreadPoolExecutor

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
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(
            options=chrome_options,
            service=Service(Config.CHROMEDRIVER_PATH)  # 使用 Config.CHROMEDRIVER_PATH
        )
        self.driver.get(config.LOGIN_URL)  # 使用 config.BASE_URL
        self.wait = WebDriverWait(self.driver, Config.WAIT_TIMEOUT)  # 使用 Config.WAIT_TIMEOUT
        logger.info(f"設置測試環境: {config.LOGIN_URL}")

    def test_01_01_phonenumber_login(self):
        """手機號碼登入"""
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


    def test_01_02_phonenumber__wronglogin(self):
        """輸入錯誤手機號碼登入"""
        try:
            logger.info("開始測試：輸入錯誤手機號碼登入")
            print(f"Page title: {self.driver.title}")

            phone_tab = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'tab') and contains(text(), '手机')]")))
            logger.debug("Found phone tab, clicking...")
            phone_tab.click()

            phonenumber = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='number']")))
            password = self.driver.find_element(By.XPATH, "//input[@type='password']")
            login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), '登录')]")
            # 使用無效的手機號碼
            # random_username = self.generate_japanese_phone_number()
            # phonenumber.send_keys(random_username)  
            phonenumber.send_keys(Config.generate_japanese_phone_number())
            password.send_keys(config.VALID_PASSWORD)
            login_button.click()


            # 等待錯誤訊息出現
            error_message = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[contains(text(), '您输入的密码不正确')]")
            ))
            logger.debug("Found error message for invalid phone number")
            
            # 驗證錯誤訊息
            self.assertIn("您输入的密码不正确", error_message.text)  # 根據實際的錯誤訊息文字調整
            logger.info("測試用例通過：錯誤手機號碼登入測試")
            self.assertIsNotNone(error_message)

        except Exception as e:
            logger.error(f"測試用例失敗：錯誤手機號碼登入測試 - 錯誤: {str(e)}")
            self.fail()

    def test_02_01check_login_button_enabled_after_username_and_password(self):
        """檢查登入按鈕是否在輸入帳號密碼後啟用"""
        try:
            logger.info("開始測試：檢查登入按鈕是否在輸入帳號密碼後啟用")
            username_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@maxlength='18']")))
            password_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']")))
            login_button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), '登录')]")))

            initial_disabled = "disabled" in login_button.get_attribute("class")
            logger.debug(f"未輸入任何資料: {'disabled' if initial_disabled else 'enabled'}")
            self.assertTrue(initial_disabled, "登入按鈕初始狀態應為 disabled")

            username = "cooper001"
            username_input.send_keys(username)
            time.sleep(self.delay_seconds)

            mid_disabled = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), '登录')]")))
            mid_disabled = "disabled" in login_button.get_attribute("class")
            logger.debug(f"僅輸入帳號: {'disabled' if mid_disabled else 'enabled'}")
            self.assertTrue(mid_disabled, "僅輸入用戶名後，登入按鈕應仍為 disabled")

            password = "1234Qwer"
            password_input.send_keys(password)
            time.sleep(self.delay_seconds)

            final_disabled = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), '登录')]")))
            final_disabled = "disabled" in login_button.get_attribute("class")
            logger.debug(f"全部輸入: {'disabled' if final_disabled else 'enabled'}")
            self.assertFalse(final_disabled, "輸入用戶名和密碼，登入按鈕應為 enabled")

            self.assertFalse(final_disabled, "Login button should be enabled after username and password input")
            logger.info("測試用例通過：登入按鈕檢查成功")
        except Exception as e:
            logger.error(f"測試用例失敗：登入按鈕檢查 - 錯誤: {str(e)}")
            self.fail()

    def test_02_02_successful_login(self):
        """帳號密碼正確登入"""
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

    def test_02_03_invalid_credentials(self):
        """帳號密碼錯誤登入"""
        try:
            logger.info("開始測試：帳號密碼錯誤登入")
            username = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@maxlength='18']")))
            password = self.driver.find_element(By.XPATH, "//input[@type='password']")
            login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), '登录')]")
            # random_username = self.generate_random_username()
            username.send_keys(Config.generate_random_username())
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

    def test_03_01_mail_login(self):
        """郵箱登入"""
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

    def test_03_02_mail_wronglogin(self):
        """郵箱登入"""
        try:
            logger.info("開始測試：郵箱登入")
            phone_tab = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'tab') and contains(text(), ' 邮箱 ')]")))
            phone_tab.click()

            email = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='text']")))
            password = self.driver.find_element(By.XPATH, "//input[@type='password']")
            login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), '登录')]")
            email.send_keys(Config.generate_random_email())
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
    
def run_test(test_method):
    suite = unittest.TestSuite()
    suite.addTest(LoginPageTest(test_method))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

if __name__ == "__main__":
    test_cases = ["test_01_01_phonenumber_login",
                     "test_01_02_phonenumber__wronglogin",
                     "test_02_01check_login_button_enabled_after_username_and_password",
                     "test_02_02_successful_login",
                     "test_02_03_invalid_credentials",
                     "test_03_01_mail_login",
                     "test_03_02_mail_wronglogin"]  # 测试方法名称
    with ThreadPoolExecutor(max_workers=16) as executor:
        executor.map(run_test, test_cases)
    logger.info("測試運行完成")


# if __name__ == "__main__":
#     suite = unittest.TestLoader().loadTestsFromTestCase(LoginPageTest)
#     runner = CustomTextTestRunner(resultclass=CleanTextTestResult, verbosity=2)
#     result = runner.run(suite)
#     logger.info("測試運行完成")