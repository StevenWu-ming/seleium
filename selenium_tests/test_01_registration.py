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
        logger.info(f"\n📌測試結果摘要:")
        logger.info(f"✅通過測試數: {self.pass_count}")
        logger.info(f"❌失敗測試數: {self.fail_count}")
        logger.info(f"📊總測試數: {total}")

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
        # chrome_options.add_argument("--headless")
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
            username_input.send_keys(f'A'+config.INVALID_USERNAME_PREFIX)
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


    # def test_02_01_phonenumber_login(self):
    #     try:
    #         logger.info("開始測試：手機號碼登入")
    #         print(f"Page title: {self.driver.title}")

    #         phone_tab = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'tab') and contains(text(), '手机')]")))
    #         logger.debug("Found phone tab, clicking...")
    #         phone_tab.click()

    #         phone_dropdown = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'phone-box')]//button[contains(@class, 'select-btn')]")))
    #         logger.debug("Found phone dropdown, clicking...")
    #         phone_dropdown.click()

    #         search_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='搜索' or contains(@class, 'search')]")))
    #         search_input.send_keys("+86")
    #         china_option = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '+86')] | //li[contains(text(), '+86')]")))
    #         logger.debug("Found '+86' option, clicking...")
    #         china_option.click()

    #         phonenumber = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='number']")))
    #         password = self.driver.find_element(By.XPATH, "//input[@type='password']")
    #         login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), '登录')]")
    #         phonenumber.send_keys(config.PHONE_NUMBER)
    #         password.send_keys(config.VALID_PASSWORD)
    #         login_button.click()

    #         try:
    #             success_message = self.wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), '我的钱包')]")))
    #             self.assertIn("我的钱包", success_message.text)
    #             logger.info("測試用例通過：手機號碼直接登入成功")
    #             self.assertIsNotNone(success_message)
    #             return

    #         except Exception as direct_login_error:
    #             logger.warning(f"直接登入失敗，可能需要驗證碼: {str(direct_login_error)}")

    #         get_code_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'input-group-txt') and contains(@class, 'get-code')]")))
    #         logger.debug("Clicking get code button...")
    #         get_code_button.click()

    #         success_toast = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'toast-text')]//p[contains(text(), '成功')]")))
    #         logger.debug("Verification code sent successfully")

    #         verify_code_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'input-group')]//input[@type='number' and @maxlength='6']")))
    #         verify_code_input.send_keys(config.VERIFY_CODE)

    #         success_message = self.wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), '我的钱包')]")))
    #         self.assertIn("我的钱包", success_message.text)
    #         logger.info("測試用例通過：手機號碼經由驗證碼登入成功")
    #         self.assertIsNotNone(success_message)

    #     except Exception as e:
    #         logger.error(f"測試用例失敗：手機號碼登入 - 錯誤: {str(e)}")
    #         self.fail()


    # def test_02_02_phonenumber__wronglogin(self):
    #     try:
    #         logger.info("開始測試：輸入錯誤手機號碼登入")
    #         print(f"Page title: {self.driver.title}")

    #         phone_tab = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'tab') and contains(text(), '手机')]")))
    #         logger.debug("Found phone tab, clicking...")
    #         phone_tab.click()

    #         phonenumber = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='number']")))
    #         password = self.driver.find_element(By.XPATH, "//input[@type='password']")
    #         login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), '登录')]")
    #         # 使用無效的手機號碼
    #         # random_username = self.generate_japanese_phone_number()
    #         # phonenumber.send_keys(random_username)  
    #         phonenumber.send_keys(config.INVALID_PHONE_NUMBER)
    #         password.send_keys(config.VALID_PASSWORD)
    #         login_button.click()


    #         # 等待錯誤訊息出現
    #         error_message = self.wait.until(EC.presence_of_element_located(
    #             (By.XPATH, "//div[contains(text(), '您输入的密码不正确')]")
    #         ))
    #         logger.debug("Found error message for invalid phone number")
            
    #         # 驗證錯誤訊息
    #         self.assertIn("您输入的密码不正确", error_message.text)  # 根據實際的錯誤訊息文字調整
    #         logger.info("測試用例通過：錯誤手機號碼登入測試")
    #         self.assertIsNotNone(error_message)

    #     except Exception as e:
    #         logger.error(f"測試用例失敗：錯誤手機號碼登入測試 - 錯誤: {str(e)}")
    #         self.fail()


    # def test_03_01_mail_login(self):
    #     try:
    #         logger.info("開始測試：郵箱登入")
    #         phone_tab = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'tab') and contains(text(), ' 邮箱 ')]")))
    #         phone_tab.click()

    #         email = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='text']")))
    #         password = self.driver.find_element(By.XPATH, "//input[@type='password']")
    #         login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), '登录')]")
    #         email.send_keys(config.EMAIL)
    #         password.send_keys(config.VALID_PASSWORD)
    #         login_button.click()

    #         success_message = self.wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), '我的钱包')]")))
    #         self.assertIn("我的钱包", success_message.text)
    #         logger.info("測試用例通過：郵箱登入成功")
    #         self.assertIsNotNone(success_message)

    #     except Exception as e:
    #         logger.error(f"測試用例失敗：郵箱登入 - 錯誤: {str(e)}")
    #         self.fail()

    # def test_03_02_mail_wronglogin(self):
    #     try:
    #         logger.info("開始測試：郵箱登入")
    #         phone_tab = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'tab') and contains(text(), ' 邮箱 ')]")))
    #         phone_tab.click()

    #         email = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='text']")))
    #         password = self.driver.find_element(By.XPATH, "//input[@type='password']")
    #         login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), '登录')]")
    #         email.send_keys(config.INVALID_EMAIL)
    #         password.send_keys(config.VALID_PASSWORD)
    #         login_button.click()

    #         error_message = self.wait.until(EC.presence_of_element_located(
    #             (By.XPATH, "//div[contains(text(), '邮箱与密码不匹配')]")
    #         ))
    #         logger.debug("Found error message for invalid email ")
            
    #         # 驗證錯誤訊息
    #         self.assertIn("邮箱与密码不匹配", error_message.text)  # 根據實際的錯誤訊息文字調整
    #         logger.info("測試用例通過：錯誤郵箱登入測試")
    #         self.assertIsNotNone(error_message)

    #     except Exception as e:
    #         logger.error(f"測試用例失敗：錯誤郵箱登入測試 - 錯誤: {str(e)}")
    #         self.fail()
    
    def tearDown(self):
        logger.info("測試結束，關閉瀏覽器")
        self.driver.quit()

if __name__ == "__main__":
    unittest.main(verbosity=2)