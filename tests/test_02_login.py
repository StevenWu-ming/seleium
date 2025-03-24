# selenium_tests/test_login.py
import os
import sys
# 添加項目根目錄到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time
from config.config import config  
from utils.test_utils import CleanTextTestResult, CustomTextTestRunner
from selenium.common.exceptions import TimeoutException
from BaseTest import BaseTest


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

class LoginPageTest(BaseTest):
    def setUp(self):
        self.url = config.LOGIN_URL  # 指定註冊頁面
        print(f"設定的測試 URL: {self.url}")
        super().setUp()  # 調用 BaseTest 的 setUp()


    def test_01_01_phonenumber_login(self):
        """手機號碼登入"""
        try:
            logger.info("開始測試：手機號碼登入")
            
            phone_tab = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'tab') and contains(text(), '手机')]")))
            logger.debug("Found phone tab, clicking...")
            phone_tab.click()

            phone_dropdown = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'phone-box')]//button[contains(@class, 'select-btn')]")))
            logger.debug("Found phone dropdown, clicking...")
            phone_dropdown.click()

            search_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='搜索' or contains(@class, 'search')]")))
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
            phone_tab = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'tab') and contains(text(), '手机')]")))
            phone_tab.click()

            phonenumber = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='number']")))
            password = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='password']")))
            login_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '登录')]")))

            # 使用無效的手機號碼
            phonenumber.send_keys(config.generate_japanese_phone_number())  
            password.send_keys(config.VALID_PASSWORD)
            login_button.click()

            # 等待錯誤訊息出現
            try:
                error_message = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
                    (By.XPATH, "//div[contains(@class, 'error-info') and contains(text(), '您输入的密码不正确')]")
                ))
                logger.debug(f"錯誤訊息內容: {error_message.text}")
                self.assertIn("您输入的密码不正确", error_message.text)  # 根據實際的錯誤訊息文字調整
            except TimeoutException as e:
                # Take screenshot on error
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                screenshot_path = f"error_screenshot_{timestamp}.png"
                self.driver.save_screenshot(screenshot_path)
                logger.error(f"錯誤訊息未能找到: {str(e)}")
                logger.debug(f"Page source: {self.driver.page_source}")
                logger.info(f"Screenshot saved at {screenshot_path}")
                self.fail(f"錯誤訊息未能在預定時間內出現")
            
            logger.info("測試用例通過：錯誤手機號碼登入測試")

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
            username.send_keys(config.generate_random_username())
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
        """錯誤郵箱登入"""
        try:
            logger.info("開始測試：郵箱登入")
            phone_tab = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'tab') and contains(text(), ' 邮箱 ')]")))
            phone_tab.click()

            email = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='text']")))
            password = self.driver.find_element(By.XPATH, "//input[@type='password']")
            login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), '登录')]")
            email.send_keys(config.generate_random_email())
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
    


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(LoginPageTest)
    runner = CustomTextTestRunner(resultclass=CleanTextTestResult, verbosity=2)
    result = runner.run(suite)
    logger.info("測試運行完成")
