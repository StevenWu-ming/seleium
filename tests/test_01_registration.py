# selenium_tests/test_registration.py
import os
import sys
# 添加項目根目錄到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time
from config.config import Config , config  # 導入 Config 和 config
from utils.test_utils import CleanTextTestResult, CustomTextTestRunner
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException  # 確保導入
from config.BaseTest import BaseTest


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

class registrationPageTest(BaseTest):
    def setUp(self):
        self.url = config.REGISTER_URL  # 指定註冊頁面
        print(f"設定的測試 URL: {self.url}")
        super().setUp()  # 調用 BaseTest 的 setUp()


    def test_01_01check_registration_button_enabled_after_username_and_password(self):
        """檢查註冊按鈕是否在輸入帳號密碼後啟用"""
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
            # time.sleep(self.delay_seconds)

            # mid_disabled = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), '注册')]")))
            mid_disabled = "disabled" in registration_button.get_attribute("class")
            logger.debug(f"僅輸入帳號: {'disabled' if mid_disabled else 'enabled'}")
            self.assertTrue(mid_disabled, "僅輸入用戶名後，註冊按鈕應仍為 disabled")

            password = "1234Qwer"
            password_input.send_keys(password)
            time.sleep(self.delay_seconds)

            # final_disabled = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), '注册')]")))
            final_disabled = "disabled" in registration_button.get_attribute("class")
            logger.debug(f"全部輸入: {'disabled' if final_disabled else 'enabled'}")
            self.assertFalse(final_disabled, "輸入用戶名和密碼並同意條款後，註冊按鈕應為 enabled")

            logger.info("測試用例通過：註冊按鈕檢查成功")
        except Exception as e:
            logger.error(f"測試用例失敗：註冊按鈕檢查 - 錯誤: {str(e)}")
            self.fail()

    def test_01_02_registration(self):
        """帳號密碼正確註冊"""
        try:
            logger.info("開始測試：帳號密碼正確註冊")

            while True:
                try:
                    close_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//i[contains(@class, 'close-btn')]")))
                    if close_button:
                        # 使用 JavaScript 點擊，避免 StaleElementReferenceException
                        self.driver.execute_script("arguments[0].click();", close_button)
                    else:
                        break
                except (TimeoutException, StaleElementReferenceException):
                    break  # 如果超時或元素過期，則退出循環

            username_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '用户名')]//following-sibling::div//input[@type='text']")))            
            password = self.driver.find_element(By.XPATH, "//input[@type='password']")
            registration_button = self.driver.find_element(By.XPATH, "//button[contains(text(), '注册')]")
            username_input.send_keys(Config.generate_random_username())
            password.send_keys(config.VALID_PASSWORD)
            registration_button.click()

            success_message = self.wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), '我的钱包')]")))
            self.assertIn("我的钱包", success_message.text)
            logger.info("測試用例通過：帳號密碼正確註冊成功")
        except Exception as e:
            screenshot_path = os.path.join(log_dir, f"screenshot_bank_option_failure_{int(time.time())}.png")
            self.driver.save_screenshot(screenshot_path)
            logger.error(f"測試用例失敗：帳號密碼正確註冊 - 錯誤: {str(e)}")
            self.fail()

    def test_01_03_registration_duplicate(self):
        """帳號重複無法註冊"""
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




if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(registrationPageTest)
    runner = CustomTextTestRunner(resultclass=CleanTextTestResult, verbosity=2)
    result = runner.run(suite)
    logger.info("測試運行完成")
