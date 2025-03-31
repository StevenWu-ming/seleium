# selenium_tests/test_login.py
import os
import sys
# 添加項目根目錄到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import time
import logging
import unittest
from config.config import Config,config  
from config.BaseTest import BaseTest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from utils.test_utils import CleanTextTestResult, CustomTextTestRunner, log_and_fail_on_exception
from config.selenium_helpers import close_popup, perform_login, wait_for_success_message, wait_for_err_message, input_text, click_element


CustomTextTestRunner(unittest.TextTestRunner)


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

    
class LoginPageTest(BaseTest):
    def setUp(self):
        self.url = config.LOGIN_URL  # 指定註冊頁面
        print(f"設定的測試 URL: {self.url}")
        super().setUp()  # 調用 BaseTest 的 setUp()

    @log_and_fail_on_exception
    def test_01_01_phonenumber_login(self):
        """手機號碼登入"""
        #定位手機tab 並且點擊
        click_element(self.driver, self.wait, "//div[contains(@class, 'tab') and contains(text(), '手机')]") 
        #定位手機區碼 並且點擊
        click_element(self.driver, self.wait, "//div[contains(@class, 'phone-box')]//button[contains(@class, 'select-btn')]")
        #手機區碼輸入+86
        input_text(self.driver, self.wait, "//input[@placeholder='搜索' or contains(@class, 'search')]", "+86")
        time.sleep(self.delay_seconds)
        #定位+86位置 並且點擊
        click_element(self.driver, self.wait, "//div[contains(text(), '+86')]")
        # 下面這段先不要移除
        # china_option = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '+86')] | //li[contains(text(), '+86')]")))
        # logger.debug("Found '+86' option, clicking...")
        # china_option.click()

        #定位手機號碼欄位 輸入手機號碼
        input_text(self.driver, self.wait, "//input[@type='number']", (config.PHONE_NUMBER))
        #定位密碼欄位 輸入密碼
        input_text(self.driver, self.wait, "//input[@type='password']", (config.VALID_PASSWORD))
        #定位登入按鈕 並且點擊
        click_element(self.driver, self.wait, "//button[contains(text(), '登录')]")


   
        # 調用 wait_for_success_message 函數，等待並獲取包含 "我的钱包" 的成功提示信息
        try:
            success_message = wait_for_success_message(self.wait, "我的钱包")
            # 斷言檢查成功提示信息中是否包含 "我的钱包" 這個關鍵字，
            # 以驗證界面上顯示的信息符合預期     
            self.assertIn("我的钱包", success_message)
            # 記錄成功信息到日誌，表示手機號碼直接登入測試用例通過
            logger.info("測試用例通過：手機號碼直接登入成功")
            # 斷言確認 success_message 不為 None，以進一步保證獲取到的提示信息有效
            self.assertIsNotNone(success_message)
            return
        except Exception as direct_login_error:
            # 當上述任一操作失敗時，捕獲異常並記錄警告，
            # 提示直接登入失敗，可能需要驗證碼處理，並顯示錯誤信息
            logger.warning(f"直接登入失敗，可能需要驗證碼: {str(direct_login_error)}")

        # 點擊發送驗證碼的按鈕或連結
        # 此元素必須同時包含 'input-group-txt' 和 'get-code' 兩個 CSS 類名，用以定位發送驗證碼的按鈕
        click_element(self.driver, self.wait, "//div[contains(@class, 'input-group-txt') and contains(@class, 'get-code')]")

        # 使用顯式等待，直到出現包含「成功」文字的提示訊息（toast）
        # 這裡等待的元素為一個 <p> 標籤，其父容器帶有 'toast-text' 類名
        success_toast = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'toast-text')]//p[contains(text(), '成功')]")))
        # 記錄除錯日誌，標示驗證碼發送成功
        logger.debug("Verification code sent successfully")
        # 在輸入框中填入驗證碼
        # 此輸入框為數字類型並限制最大長度為6位，通常用於輸入驗證碼
        # 使用 config.VERIFY_CODE 中的測試驗證碼進行填入
        input_text(self.driver, self.wait, "//div[contains(@class, 'input-group')]//input[@type='number' and @maxlength='6']", (config.VERIFY_CODE))
        # 等待並獲取包含「我的钱包」字樣的成功訊息，表示登入流程成功
        success_message = wait_for_success_message(self.wait, "我的钱包")
        # 斷言：檢查返回的成功訊息中是否包含「我的钱包」這個關鍵字
        self.assertIn("我的钱包", success_message)
        # 記錄日誌：測試用例通過，表示使用手機號碼加驗證碼的登入流程成功
        logger.info("測試用例通過：手機號碼經由驗證碼登入成功")
        # 斷言：確認 success_message 不為 None，進一步驗證成功訊息是有效的
        self.assertIsNotNone(success_message)

    @log_and_fail_on_exception
    def test_01_02_phonenumber__wronglogin(self):
        """輸入錯誤手機號碼登入"""
        # 點擊選項卡，切換到「手机」頁面
        # 利用 XPath 定位 class 包含 "tab" 且文本包含 "手机" 的元素
        click_element(self.driver, self.wait, "//div[contains(@class, 'tab') and contains(text(), '手机')]")
        # 在數字類型的輸入框中輸入生成的日本手機號碼，用於測試手機號碼格式
        input_text(self.driver, self.wait, "//input[@type='number']", (Config.generate_japanese_phone_number()))
        # 在密碼輸入框中輸入有效的密碼，這裡使用從配置文件中獲取的有效密碼
        input_text(self.driver, self.wait, "//input[@type='password']", (config.VALID_PASSWORD))
        # 點擊包含 "登录" 文字的按鈕，提交登入表單
        click_element(self.driver, self.wait, "//button[contains(text(), '登录')]")        

        # 等待錯誤訊息出現
        try:
            # 等待錯誤提示訊息出現，預期訊息中包含 "您输入的密码不正确"
            error_message = wait_for_err_message(self.wait, "您输入的密码不正确")
            # 下面這段先不要移除
            # error_message = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
            #     (By.XPATH, "//div[contains(@class, 'error-info') and contains(text(), '您输入的密码不正确')]")
            # ))
            #將捕獲的錯誤訊息內容記錄到調試日誌中，方便後續檢查
            logger.debug(f"錯誤訊息內容: {error_message}")
            # 驗證捕獲到的錯誤訊息中是否包含預期的文字 "您输入的密码不正确"
            self.assertIn("您输入的密码不正确", error_message)  # 根據實際的錯誤訊息文字調整
        except TimeoutException as e:
            # 如果等待錯誤訊息超時，捕獲 TimeoutException 異常
            logger.error(f"錯誤訊息未能找到: {str(e)}")
            # 異常處理：報告測試失敗，提示錯誤訊息未能在預定時間內出現
            self.fail(f"錯誤訊息未能在預定時間內出現")
        # 記錄最終測試結果：表示錯誤手機號碼登入測試成功
        logger.info("測試用例通過：錯誤手機號碼登入測試")

    @log_and_fail_on_exception
    def test_02_01check_login_button_enabled_after_username_and_password(self):
        """檢查登入按鈕是否在輸入帳號密碼後啟用"""
        # 使用顯式等待，直到頁面上包含「登录」文字的按鈕元素出現，並將其賦值給 login_button
        login_button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), '登录')]")))
        # 判斷按鈕的 class 屬性中是否包含 "disabled"，以檢查按鈕初始狀態是否為禁用
        initial_disabled = "disabled" in login_button.get_attribute("class")
        # 記錄初始狀態到日誌，顯示未輸入任何資料時按鈕的狀態
        logger.debug(f"未輸入任何資料: {'disabled' if initial_disabled else 'enabled'}")
        # 斷言檢查：確保初始狀態下按鈕應該是禁用的，若不符合則顯示錯誤信息
        self.assertTrue(initial_disabled, "登入按鈕初始狀態應為 disabled")

        # 在用戶名輸入框中輸入 "cooper001"，該輸入框通過 maxlength='18' 來限制輸入長度
        input_text(self.driver, self.wait, "//input[@maxlength='18']", "cooper001")
        # 再次檢查按鈕的狀態，判斷輸入用戶名後是否仍保持禁用狀態
        mid_disabled = "disabled" in login_button.get_attribute("class")
        # 記錄當前狀態到日誌，顯示僅輸入帳號後按鈕的狀態
        logger.debug(f"僅輸入帳號: {'disabled' if mid_disabled else 'enabled'}")
        # 斷言：確認僅輸入用戶名後按鈕仍為禁用狀態，否則測試失敗
        self.assertTrue(mid_disabled, "僅輸入用戶名後，登入按鈕應仍為 disabled")
        
        # 在密碼輸入框中輸入 "1234Qwer"，模擬用戶輸入密碼
        input_text(self.driver, self.wait, "//input[@type='password']", "1234Qwer")
        # 最後檢查按鈕狀態，判斷輸入用戶名和密碼後按鈕是否從禁用變為啟用
        final_disabled = "disabled" in login_button.get_attribute("class")
        # 記錄最終狀態到日誌，顯示全部資料輸入後按鈕的狀態
        logger.debug(f"全部輸入: {'disabled' if final_disabled else 'enabled'}")
        # 斷言：確認輸入用戶名和密碼後按鈕應該變為啟用（即不包含 "disabled"）
        self.assertFalse(final_disabled, "輸入用戶名和密碼，登入按鈕應為 enabled")

        # 重複斷言確認按鈕啟用狀態，並提供英文錯誤信息
        self.assertFalse(final_disabled, "Login button should be enabled after username and password input")
        
        logger.info("測試用例通過：登入按鈕檢查成功")

    @log_and_fail_on_exception
    def test_02_02_successful_login(self):
        """帳號密碼正確登入"""
        # 輸入使用者名稱到指定輸入框（最大長度為18個字元）
        input_text(self.driver, self.wait, "//input[@maxlength='18']", (config.VALID_USERNAME))
        # 輸入密碼到密碼輸入框
        input_text(self.driver, self.wait, "//input[@type='password']", (config.VALID_PASSWORD))
        # 點擊包含“登录”文字的按鈕來提交登入表單
        click_element(self.driver, self.wait, "//button[contains(text(), '登录')]")
        # 等待成功訊息出現，並檢查是否包含“我的ㄓ钱包”文字
        success_message = wait_for_success_message(self.wait, "我的钱包")
        # 斷言檢查成功訊息中包含“我的钱包”，驗證登入成功
        self.assertIn("我的钱包", success_message)
        # 記錄測試用例通過的日誌訊息
        logger.info("測試用例通過：帳號密碼正確登入成功")

    @log_and_fail_on_exception
    def test_02_03_invalid_credentials(self):
        """帳號密碼錯誤登入"""
        # 輸入隨機生成的使用者名稱到指定輸入框（最大長度為18個字元）
        input_text(self.driver, self.wait, "//input[@maxlength='18']", (Config.generate_random_username()))
        # 輸入有效的密碼到密碼輸入框
        input_text(self.driver, self.wait, "//input[@type='password']", (config.VALID_PASSWORD))
        # 點擊包含“登录”文字的按鈕來提交登入表單
        click_element(self.driver, self.wait, "//button[contains(text(), '登录')]")

        # 等待錯誤訊息出現，並檢查是否包含“您输入的密码不正确”文字
        error_message = wait_for_err_message(self.wait, "您输入的密码不正确")

        # 斷言檢查錯誤訊息中包含“您输入的密码不正确”，驗證登入失敗
        self.assertIn("您输入的密码不正确", error_message)
        # 記錄測試用例通過的日誌訊息，表示帳號密碼錯誤無法登入
        logger.info("測試用例通過：帳號密碼錯誤無法登入成功")

    @log_and_fail_on_exception
    def test_03_01_mail_login(self):
        """郵箱登入"""  
        # 點擊選項卡，切換到「 邮箱 」登入方式
        # 利用 XPath 定位 class 包含 "tab" 且文本包含 " 邮箱 " 的元素
        click_element(self.driver, self.wait, "//div[contains(@class, 'tab') and contains(text(), ' 邮箱 ')]")

        # 在文本輸入框中輸入郵箱地址，郵箱地址從配置文件中取得
        input_text(self.driver, self.wait, "//input[@type='text']", (config.EMAIL))
        # 在密碼輸入框中輸入密碼，密碼從配置文件中取得
        input_text(self.driver, self.wait, "//input[@type='password']", (config.VALID_PASSWORD))
        # 點擊包含「登录」文字的按鈕，提交登入請求
        click_element(self.driver, self.wait, "//button[contains(text(), '登录')]")

        # 等待並捕獲登入成功後返回的提示訊息，預期訊息中包含「我的钱包」
        success_message = wait_for_success_message(self.wait, "我的钱包")
        # 斷言檢查：確保成功訊息不為 None，以進一步確認提示信息有效
        self.assertIn("我的钱包", success_message)
        logger.info("測試用例通過：郵箱登入成功")
        self.assertIsNotNone(success_message)

    @log_and_fail_on_exception
    def test_03_02_mail_wronglogin(self):
        """錯誤郵箱登入"""
        click_element(self.driver, self.wait, "//div[contains(@class, 'tab') and contains(text(), ' 邮箱 ')]")

        input_text(self.driver, self.wait, "//input[@type='text']", (Config.generate_random_email()))
        input_text(self.driver, self.wait, "//input[@type='password']", (config.VALID_PASSWORD))
        click_element(self.driver, self.wait, "//button[contains(text(), '登录')]")

        error_message = wait_for_err_message(self.wait, "邮箱与密码不匹")
        logger.debug("Found error message for invalid email ")
        
        # 驗證錯誤訊息
        self.assertIn("邮箱与密码不匹配", error_message)  # 根據實際的錯誤訊息文字調整
        logger.info("測試用例通過：錯誤郵箱登入測試")
        self.assertIsNotNone(error_message)
    


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(LoginPageTest)
    runner = CustomTextTestRunner(resultclass=CleanTextTestResult, verbosity=2)
    result = runner.run(suite)
    logger.info("測試運行完成")
