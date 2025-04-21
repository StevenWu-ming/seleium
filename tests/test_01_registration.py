# seleium/tests/test_01_registration.py
import os
import sys
# 添加項目根目錄到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import time
import logging
import unittest
from config.BaseTest import BaseTest
from config.config import Config 
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException  # 確保導入
from config.selenium_helpers import close_popup, perform_login, wait_for_success_message, wait_for_err_message, input_text, click_element
from utils.test_utils import CleanTextTestResult, CustomTextTestRunner, log_and_fail_on_exception


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

# config = Config.get_current_config()  # 每次動態取得當前環境設定


class registrationPageTest(BaseTest):
    def setUp(self):
        self.config = Config.get_current_config() 
        self.url = self.config.REGISTER_URL  # 指定註冊頁面
        print(f"設定的測試 URL: {self.url}")
        super().setUp()  # 調用 BaseTest 的 setUp()

    @log_and_fail_on_exception
    def test_01_01check_registration_button_enabled_after_username_and_password(self):
        """檢查註冊按鈕是否在輸入帳號密碼後啟用"""
        #關閉公告彈窗
        close_popup(self.driver, self.wait)

        # 可以優化email_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '邮箱')]//following-sibling::div//input[@type='text']")))            

        #定位註冊按鈕 
        registration_button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), ' 注册 ')]")))
        #檢查註冊按鈕狀態 獲取按鈕的 class 屬性值"disabled" 這個詞是否出現在 並把布林值True，儲存在 initial_disabled 變數中
        initial_disabled = "disabled" in registration_button.get_attribute("class")
        logger.debug(f"未輸入任何資料: {'disabled' if initial_disabled else 'enabled'}")
        #這是一個測試斷言，通常用於單元測試框架（如 unittest）assertTrue() 檢查 initial_disabled 是否為 True
        self.assertTrue(initial_disabled, "註冊按鈕初始狀態應為 disabled")

        #定位帳號輸入欄位 並且輸入
        input_text(self.driver, self.wait, "//div[contains(text(), '用户名')]//following-sibling::div//input[@type='text']", "cooper001")
        time.sleep(self.delay_seconds)

        #檢查註冊按鈕狀態 獲取按鈕的 class 屬性值"disabled" 這個詞是否出現在 並把布林值True，儲存在 mid_disabled 變數中
        mid_disabled = "disabled" in registration_button.get_attribute("class")
        logger.debug(f"僅輸入帳號: {'disabled' if mid_disabled else 'enabled'}")
        #這是一個測試斷言，通常用於單元測試框架（如 unittest）assertTrue() 檢查 mid_disabled 是否為 True
        self.assertTrue(mid_disabled, "僅輸入用戶名後，註冊按鈕應仍為 disabled")

        #定位密碼輸入欄位 並且輸入
        input_text(self.driver, self.wait, "//input[@type='password']", "1234Qwer")
        time.sleep(self.delay_seconds)
        
        #檢查註冊按鈕狀態 獲取按鈕的 class 屬性值"disabled" 這個詞是否出現在 並把布林值False，儲存在 final_disabled 變數中
        final_disabled = "disabled" in registration_button.get_attribute("class")
        logger.debug(f"全部輸入: {'disabled' if final_disabled else 'enabled'}")
        #這是一個測試斷言，通常用於單元測試框架（如 unittest）assertTrue() 檢查 final_disabled 是否為 False
        self.assertFalse(final_disabled, "輸入用戶名和密碼並同意條款後，註冊按鈕應為 enabled")

        logger.info("測試用例通過：註冊按鈕檢查成功")

    @log_and_fail_on_exception
    def test_01_02_registration(self):
        """帳號密碼正確註冊，並且進行 KYC 驗證"""
# Step 1: 註冊
        #關閉公告彈窗
        close_popup(self.driver, self.wait)
        #定位帳號輸入欄位 並且輸入 隨機帳號
        input_text(self.driver, self.wait, "//div[contains(text(), '用户名')]//following-sibling::div//input[@type='text']", (Config.generate_random_username()))
        #定位密碼輸入欄位 並且輸入 
        input_text(self.driver, self.wait, "//input[@type='password']", (self.config.VALID_PASSWORD))
        click_element(self.driver, self.wait, "//button[contains(text(), '注册')]")
        #判斷是否登入成功 拿到我的錢包字串
        success_message = wait_for_success_message(self.wait, "我的钱包")
        self.assertIn("我的钱包", success_message)
        logger.info("測試用例通過：帳號密碼正確註冊成功")

 # Step 2: 進行 KYC 驗證
        kyc_url = "https://uat-newplatform.mxsyl.com/zh-cn/userCenter/kyc"
        self.driver.get(kyc_url)

        click_element(self.driver, self.wait, "//button[contains(text(), ' 立即开始 ')]")
        #定位手機區碼 並且點擊
        click_element(self.driver, self.wait, "//button[.//p[text()='+81']]")
        #手機區碼輸入+86
        input_text(self.driver, self.wait, "//input[@placeholder='搜索' or contains(@class, 'search')]", "+86")
        time.sleep(self.delay_seconds)
        click_element(self.driver, self.wait, "//div[contains(text(), '+86')]")

        #定位手機號碼欄位 輸入手機號碼
        input_text(self.driver, self.wait,  "//div[contains(@class, 'phone-select')]//input[@type='number']", (Config.generate_chinese_phone_number()))
        # 點擊發送驗證碼的按鈕或連結
        # 此元素必須同時包含 'input-group-txt' 和 'get-code' 兩個 CSS 類名，用以定位發送驗證碼的按鈕
        click_element(self.driver, self.wait, "//div[contains(@class, 'input-group-txt') and contains(@class, 'get-code')]")
        
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), '验证码已发送')]")))
        print("✅ 檢測到驗證碼已發送字樣")

        #輸入驗證碼（目前預設123456）
        input_text(self.driver, self.wait, "//div[contains(text(), '验证码')]/following::input[@type='number'][1]", (self.config.VERIFY_CODE))

        input_text(self.driver, self.wait, "//div[contains(text(), '姓名')]/following::input[@type='text'][1]", "测试")

        click_element(self.driver, self.wait, "//button[contains(text(), '继续')]")

        success_message = wait_for_success_message(self.wait, "账户已验证")
        self.assertIn("账户已验证", success_message)
        logger.info("測試用例通過：KYC 驗證成功）")

    @log_and_fail_on_exception
    def test_01_03_registration_duplicate(self):
        """帳號重複無法註冊""" 
        #關閉公告彈窗
        close_popup(self.driver, self.wait)
        #定位帳號輸入欄位 並且輸入 
        input_text(self.driver, self.wait, "//div[contains(text(), '用户名')]//following-sibling::div//input[@type='text']", (self.config.VALID_USERNAME))
        #定位密碼輸入欄位 並且輸入
        input_text(self.driver, self.wait, "//input[@type='password']", (self.config.VALID_PASSWORD))
        click_element(self.driver, self.wait, "//button[contains(text(), '注册')]")
        #判斷是否登入失敗 拿到该用户名已存在字串
        error_message = wait_for_err_message(self.wait, "该用户名已存在")
    
        self.assertIn("该用户名已存在", error_message)
        logger.info("測試用例通過：重複帳號無法註冊")


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(registrationPageTest)
    runner = CustomTextTestRunner(resultclass=CleanTextTestResult, verbosity=2)
    result = runner.run(suite)
    logger.info("測試運行完成")

