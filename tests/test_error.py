'''
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import time
import logging
import unittest
import requests  # 添加 requests 依賴
from config.config import Config  
from config.BaseTest import BaseTest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from utils.test_utils import CleanTextTestResult, CustomTextTestRunner, log_and_fail_on_exception
from config.selenium_helpers import close_popup, perform_login, wait_for_success_message, wait_for_err_message, input_text, click_element
from testbackend.sc_otp import DepositRiskProcessor
from testbackend.sc_login_aeskey_api import run_admin_login_workflow
import json

CustomTextTestRunner(unittest.TextTestRunner)

# 日誌設置（保持原樣）
log_dir = os.path.dirname(__file__)
log_file = os.path.join(log_dir, 'test_log.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(name)s] %(message)s',
    handlers=[
        logging.FileHandler(log_file, mode='w'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class LoginPageTest(BaseTest):
    def setUp(self):
        self.config = Config.get_current_config() 
        self.url = self.config.LOGIN_URL
        print(f"設定的測試 URL: {self.url}")
        super().setUp()  # 調用 BaseTest 的 setUp，使用標準 selenium.webdriver

    def log_error_details(self):
        """記錄 API 回應和前端錯誤訊息（使用 requests）"""
        # 模擬 API 請求
        random_username = Config.generate_random_username()
        try:
            response = requests.post(
                "https://example.com/api/login",  # 替換為實際 API 端點
                json={"username": random_username, "password": self.config.VALID_PASSWORD},
                timeout=5
            )
            api_response = {
                "url": response.url,
                "status_code": response.status_code,
                "body": response.text
            }
        except requests.RequestException as e:
            api_response = {
                "url": "https://example.com/api/login",
                "status_code": None,
                "body": f"Request failed: {str(e)}"
            }
        logger.error(f"API Response on error: {json.dumps(api_response, indent=2, ensure_ascii=False)}")

        # 捕獲前端錯誤訊息
        error_message = wait_for_err_message(self.wait, "您输入的密码不正确")
        if error_message:
            logger.error(f"Frontend error message: {error_message}")
        else:
            logger.error("No frontend error message found")

    @log_and_fail_on_exception
    def test_02_05_invalid_credentials(self):
        """帳號密碼錯誤登入"""
        # 輸入隨機生成的使用者名稱
        random_username = Config.generate_random_username()
        input_text(self.driver, self.wait, "//input[@maxlength='18']", random_username)
        # 輸入有效的密碼
        input_text(self.driver, self.wait, "//input[@type='password']", self.config.VALID_PASSWORD)
        # 點擊登入按鈕
        click_element(self.driver, self.wait, "//button[contains(text(), '登录')]")

        # 等待錯誤訊息
        try:
            error_message = wait_for_err_message(self.wait, "您输入的密码不正确")
            # 驗證錯誤訊息
            self.assertIn("您输入的密码不正确", error_message, f"Expected error message not found. Actual: {error_message}")
            logger.info("測試用例通過：帳號密碼錯誤無法登入成功")
        except (AssertionError, TimeoutException) as e:
            # 斷言失敗或超時時記錄 API 回應和前端錯誤
            logger.error(f"Test failed: {str(e)}")
            self.log_error_details()
            raise

    # 其他測試用例（保持不變）
    @log_and_fail_on_exception
    def test_02_01_phonenumber_login(self):
        """手機號碼登入"""
        processor = DepositRiskProcessor()
        click_element(self.driver, self.wait, "//div[contains(@class, 'tab') and contains(text(), '手机')]") 
        click_element(self.driver, self.wait, "//div[contains(@class, 'phone-box')]//button[contains(@class, 'select-btn')]")
        input_text(self.driver, self.wait, "//input[@placeholder='搜索' or contains(@class, 'search')]", "+86")
        time.sleep(self.delay_seconds)
        click_element(self.driver, self.wait, "//div[contains(text(), '+86')]")
        input_text(self.driver, self.wait, "//input[@type='number']", (self.config.PHONE_NUMBER))
        input_text(self.driver, self.wait, "//input[@type='password']", (self.config.VALID_PASSWORD))
        click_element(self.driver, self.wait, "//button[contains(text(), '登录')]")
        try:
            success_message = wait_for_success_message(self.wait, "我的钱包")
            self.assertIn("我的钱包", success_message)
            logger.info("測試用例通過：手機號碼直接登入成功")
            self.assertIsNotNone(success_message)
            return
        except Exception as direct_login_error:
            logger.warning(f"直接登入失敗，可能需要驗證碼: {str(direct_login_error)}")
        click_element(self.driver, self.wait, "//div[contains(@class, 'input-group-txt') and contains(@class, 'get-code')]")
        success_toast = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'toast-text')]//p[contains(text(), '成功')]")))
        logger.debug("Verification code sent successfully")
        verify_codes = processor.otp()
        if verify_codes:
            verify_code = verify_codes[0]
        else:
            raise Exception("無法獲取驗證碼")
        input_text(self.driver, self.wait, "//div[contains(@class, 'input-group')]//input[@type='number' and @maxlength='6']", verify_code)
        success_message = wait_for_success_message(self.wait, "我的钱包")
        self.assertIn("我的钱包", success_message)
        logger.info("測試用例通過：手機號碼經由驗證碼登入成功")
        self.assertIsNotNone(success_message)

    @log_and_fail_on_exception
    def test_02_02_phonenumber__wronglogin(self):
        """輸入錯誤手機號碼登入"""
        click_element(self.driver, self.wait, "//div[contains(@class, 'tab') and contains(text(), '手机')]")
        input_text(self.driver, self.wait, "//input[@type='number']", (Config.generate_japanese_phone_number()))
        input_text(self.driver, self.wait, "//input[@type='password']", (self.config.VALID_PASSWORD))
        click_element(self.driver, self.wait, "//button[contains(text(), '登录')]")        
        try:
            error_message = wait_for_err_message(self.wait, "您输入的密码不正确")
            logger.debug(f"錯誤訊息內容: {error_message}")
            self.assertIn("您输入的密码不正确", error_message)
        except TimeoutException as e:
            logger.error(f"錯誤訊息未能找到: {str(e)}")
            self.fail(f"錯誤訊息未能在預定時間內出現")
        logger.info("測試用例通過：錯誤手機號碼登入測試")

    @log_and_fail_on_exception
    def test_02_03check_login_button_enabled_after_username_and_password(self):
        """檢查登入按鈕是否在輸入帳號密碼後啟用"""
        login_button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), '登录')]")))
        initial_disabled = "disabled" in login_button.get_attribute("class")
        logger.debug(f"未輸入任何資料: {'disabled' if initial_disabled else 'enabled'}")
        self.assertTrue(initial_disabled, "登入按鈕初始狀態應為 disabled")
        input_text(self.driver, self.wait, "//input[@maxlength='18']", "cooper001")
        mid_disabled = "disabled" in login_button.get_attribute("class")
        logger.debug(f"僅輸入帳號: {'disabled' if mid_disabled else 'enabled'}")
        self.assertTrue(mid_disabled, "僅輸入用戶名後，登入按鈕應仍為 disabled")
        input_text(self.driver, self.wait, "//input[@type='password']", "1234Qwer")
        final_disabled = "disabled" in login_button.get_attribute("class")
        logger.debug(f"全部輸入: {'disabled' if final_disabled else 'enabled'}")
        self.assertFalse(final_disabled, "輸入用戶名和密碼，登入按鈕應為 enabled")
        self.assertFalse(final_disabled, "Login button should be enabled after username and password input")
        logger.info("測試用例通過：登入按鈕檢查成功")

    @log_and_fail_on_exception
    def test_02_04_successful_login(self):
        """帳號密碼正確登入"""
        perform_login(self.driver, self.wait, self.config.VALID_USERNAME, self.config.VALID_PASSWORD)
        try:
            success_message = wait_for_success_message(self.wait, "我的钱包")
            self.assertIn("我的钱包", success_message)
            logger.info("測試用例通過：手機號碼直接登入成功")
            self.assertIsNotNone(success_message)
            return
        except Exception as direct_login_error:
            logger.warning(f"直接登入失敗，可能需要驗證碼: {str(direct_login_error)}")
        click_element(self.driver, self.wait, "//div[contains(@class, 'input-group-txt') and contains(@class, 'get-code')]")
        phone_number = self.config.PHONE_NUMBER
        last_six_digits = phone_number[-6:]
        input_elements = self.driver.find_elements(By.XPATH, "//code-input//input[@type='number']")
        if len(input_elements) != 6:
            raise Exception("未找到六個驗證碼輸入框")
        for i in range(6):
            input_elements[i].clear()
            input_elements[i].send_keys(last_six_digits[i])
        click_element(self.driver, self.wait, "//div[@class='btn-container']//button[contains(text(), '确定')]")
        success_toast = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'toast-text')]//p[contains(text(), '成功')]")))
        print(f"驗證碼發送成功{success_toast}")
        run_admin_login_workflow()
        processor = DepositRiskProcessor()
        verify_codes = processor.otp()
        if verify_codes:
            verify_code = verify_codes[0]
        else:
            raise Exception("無法獲取驗證碼")
        input_text(self.driver, self.wait, "//div[contains(@class, 'input-group')]//input[@type='number' and @maxlength='6']", verify_code)
        time.sleep(self.delay_seconds)
        logger.debug("Verification code sent successfully")
        success_message = wait_for_success_message(self.wait, "我的钱包")
        self.assertIn("我的钱包", success_message)
        logger.info("測試用例通過：手機號碼經由驗證碼登入成功")
        self.assertIsNotNone(success_message)

    @log_and_fail_on_exception
    def test_02_06_mail_login(self):
        """郵箱登入"""  
        click_element(self.driver, self.wait, "//div[contains(@class, 'tab') and contains(text(), ' 邮箱 ')]")
        input_text(self.driver, self.wait, "//input[@type='text']", (self.config.EMAIL))
        input_text(self.driver, self.wait, "//input[@type='password']", (self.config.VALID_PASSWORD))
        click_element(self.driver, self.wait, "//button[contains(text(), '登录')]")
        success_message = wait_for_success_message(self.wait, "我的钱包")
        self.assertIn("我的钱包", success_message)
        logger.info("測試用例通過：郵箱登入成功")
        self.assertIsNotNone(success_message)

    @log_and_fail_on_exception
    def test_02_07_mail_wronglogin(self):
        """錯誤郵箱登入"""
        click_element(self.driver, self.wait, "//div[contains(@class, 'tab') and contains(text(), ' 邮箱 ')]")
        input_text(self.driver, self.wait, "//input[@type='text']", (Config.generate_random_email()))
        input_text(self.driver, self.wait, "//input[@type='password']", (self.config.VALID_PASSWORD))
        click_element(self.driver, self.wait, "//button[contains(text(), '登录')]")
        error_message = wait_for_err_message(self.wait, "邮箱与密码不匹")
        logger.debug("Found error message for invalid email ")
        self.assertIn("邮箱与密码不匹配", error_message)
        logger.info("測試用例通過：錯誤郵箱登入測試")
        self.assertIsNotNone(error_message)

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(LoginPageTest)
    runner = CustomTextTestRunner(resultclass=CleanTextTestResult, verbosity=2)
    result = runner.run(suite)
    logger.info("測試運行完成")
    '''