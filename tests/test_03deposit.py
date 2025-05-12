# 測試充值功能，支援不同環境（TestEnv 和 ProdEnv）的充值方式，包含登入、金額輸入及訂單狀態檢查
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import time
import logging
import unittest
from config.config import Config
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from config.BaseTest import BaseTest
from selenium.common.exceptions import StaleElementReferenceException
from config.selenium_helpers import close_popup, perform_login, wait_for_success_message, wait_for_err_message, input_text, click_element
from utils.test_utils import CleanTextTestResult, CustomTextTestRunner, log_and_fail_on_exception
from testbackend.sc_otp import DepositRiskProcessor
from testbackend.sc_login_aeskey_api import run_admin_login_workflow

CustomTextTestRunner(unittest.TextTestRunner)

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

class DepositTest(BaseTest):
    def setUp(self):
        self.config = Config.get_current_config()
        self.url = self.config.LOGIN_URL
        print(f"設定的測試 URL: {self.url}")
        super().setUp()

    @log_and_fail_on_exception
    def test_01_01_deposit(self):
        """充值"""
        # # 輸入使用者名稱到指定輸入框（最大長度為18個字元）
        # input_text(self.driver, self.wait, "//input[@maxlength='18']", self.config.VALID_DP_USERNAME)
        # # 輸入密碼到密碼輸入框
        # input_text(self.driver, self.wait, "//input[@type='password']", self.config.VALID_PASSWORD)
        # # 點擊包含“登录”文字的按鈕來提交登入表單
        # click_element(self.driver, self.wait, "//button[contains(text(), '登录')]")

        perform_login(self.driver, self.wait, self.config.VALID_DP_USERNAME, self.config.VALID_PASSWORD)
        
        # 調用 wait_for_success_message 函數，等待並獲取包含 "我的钱包" 的成功提示信息
        try:
            success_message = wait_for_success_message(self.wait, "我的钱包")
            # 斷言檢查成功提示信息中是否包含 "我的钱包" 這個關鍵字，
            # 以驗證界面上顯示的信息符合預期     
            self.assertIn("我的钱包", success_message)
            # 記錄成功信息到日誌，表示手機號碼直接登入測試用例通過
            logger.info("測試用例通過：手機號碼直接登入成功")
            
        except Exception as direct_login_error:
            # 當上述任一操作失敗時，捕獲異常並記錄警告，
            # 提示直接登入失敗，可能需要驗證碼處理，並顯示錯誤信息
            logger.warning(f"直接登入失敗，可能需要驗證碼: {str(direct_login_error)}")

            # 點擊發送驗證碼的按鈕或連結
            # 此元素必須同時包含 'input-group-txt' 和 'get-code' 兩個 CSS 類名，用以定位發送驗證碼的按鈕
            click_element(self.driver, self.wait, "//div[contains(@class, 'input-group-txt') and contains(@class, 'get-code')]")
            phone_number = self.config.PHONE_NUMBER
            last_six_digits = phone_number[-6:]
            input_elements = self.driver.find_elements(By.XPATH, "//code-input//input[@type='number']")
            
            if len(input_elements) != 6:
                raise Exception("未找到六個驗證碼輸入框")

            # 逐一輸入六位數字
            for i in range(6):
                input_elements[i].clear()
                input_elements[i].send_keys(last_six_digits[i])
            click_element(self.driver, self.wait, "//div[@class='btn-container']//button[contains(text(), '确定')]")

            success_toast = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'toast-text')]//p[contains(text(), '成功')]")))
            print(f"驗證碼發送成功{success_toast}")

            run_admin_login_workflow()
            processor = DepositRiskProcessor()
            
            # 在輸入框中填入驗證碼
            # 此輸入框為數字類型並限制最大長度為6位，通常用於輸入驗證碼
            # 使用 config.VERIFY_CODE 中的測試驗證碼進行填入
            verify_codes = processor.otp()
            if verify_codes:
                verify_code = verify_codes[0]  # 取第一個驗證碼
            else:
                raise Exception("無法獲取驗證碼")

            input_text(self.driver, self.wait, "//div[contains(@class, 'input-group')]//input[@type='number' and @maxlength='6']", verify_code)
            time.sleep(self.delay_seconds)

            # 關閉公告彈窗
            close_popup(self.driver, self.wait)

            # 等待遮罩層消失
            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "cdk-overlay-backdrop")))
            

        if Config.ENV == "ProdEnv":
            self.deposit_method_b()
        else:  # TestEnv
            self.deposit_method_a()

    def deposit_method_a(self):
        """充值方式 A (TestEnv)"""
        #點擊充值
        element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.toggle")))
        self.driver.execute_script("arguments[0].click();", element)

        # 等待遮罩層消失
        WebDriverWait(self.driver, 5).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "cdk-overlay-backdrop")))
   
        # 選擇“网银转账”
        element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.method-item")))
        self.driver.execute_script("arguments[0].click();", element)

        # 輸入金額
        amount_input = self.wait.until(EC.presence_of_element_located((
            By.XPATH, "//input[@type='number' and contains(@class, 'ng-untouched') and contains(@class, 'ng-pristine') and contains(@class, 'ng-valid')]")))
        self.driver.execute_script("arguments[0].value = arguments[1];", amount_input, self.config.DP_Amount)
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", amount_input)

        # 點擊銀行下拉框
        bank_dropdown = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((
                By.XPATH, "(//div[contains(@class, 'select-container')]//div[contains(@class, 'row-line') and .//i[contains(@class, 'icon-drop-down')]])[2]"
            )))
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", bank_dropdown)
        self.driver.execute_script("arguments[0].click();", bank_dropdown)
        logger.info("已點擊銀行下拉框")

        # 選擇“中国民生银行”
        try:
            bank_option = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//li[contains(text(), '中国民生银行')]")))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", bank_option)
            self.driver.execute_script("arguments[0].click();", bank_option)
            logger.info("已選擇 '中国民生银行'")
        except TimeoutException as e:
            self.fail(f"充值测试失败: 无法找到 '中国民生银行' 选项")

        # 移動到“确认”按鈕
        try:
            target_button = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(@class, 'customize-button') and contains(@class, 'large') and contains(@class, 'primary') and contains(., '确认')]")
                ))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'end'});", target_button)
        except TimeoutException:
            self.fail("无法找到确认按钮")

        # 檢查優惠券下拉選單
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((
                    By.XPATH, "//div[contains(@class, 'select-container')]//div[contains(@class, 'input-container')]//div[contains(@class, 'selected-row')]"
                ))
            )
            logger.info("優惠券下拉選單已出現")
        except TimeoutException:
            logger.warning("優惠券下拉選單未出現，繼續流程")

        # 點擊確認
        WebDriverWait(self.driver, 10).until(
            lambda d: 'disabled' not in target_button.get_attribute('class')
        )
        logger.info("✅ 確認按鈕現在可以點擊")
        ActionChains(self.driver).move_to_element(target_button).click().perform()

        # 檢查是否有未支付訂單
        try:
            success_message = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//pre[contains(@class, 'description') and contains(normalize-space(text()), '您有多笔订单未支付')]"))
            )
            self.assertIn("您有多笔订单未支付", success_message.text)
            logger.info("測試用例通過：存款速度頻繁")
            return
        except TimeoutException:
            logger.warning("檢測沒有多筆訂單可繼續存款")

        # 等待頁面跳轉並檢查成功訊息
        success_message = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(text(), '请在有效期内完成')]")))
        self.assertIn("请在有效期内完成", success_message.text)
        logger.info("測試用例通過：充值成功提交")

    def deposit_method_b(self):
        """充值方式 B (ProdEnv)"""
        #點擊充值
        element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.toggle")))
        self.driver.execute_script("arguments[0].click();", element)

        # 等待遮罩層消失
        WebDriverWait(self.driver, 5).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "cdk-overlay-backdrop")))

        # 選擇“EBPay錢包”
        element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.method-item")))
        self.driver.execute_script("arguments[0].click();", element)

        # 輸入金額
        logger.info("開始定位金額輸入框")
        amount_input = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((
                By.XPATH, "//input[@type='number' and contains(@class, 'ng-untouched') and contains(@class, 'ng-pristine') and contains(@class, 'ng-valid')]")))
        logger.info("金額輸入框定位成功")
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", amount_input)
        time.sleep(0.5)  # 等待滾動和動畫完成
        logger.info("已滾動到金額輸入框")
        logger.info(f"設置金額: {self.config.DP_Amount}")
        try:
            if amount_input.get_attribute("disabled") or amount_input.get_attribute("readonly"):
                logger.error("金額輸入框被禁用或唯讀，無法輸入")
                self.fail("金額輸入框不可用")
            amount_input.click()  # 激活輸入框焦點
            amount_input.clear()
            amount_input.send_keys(str(self.config.DP_Amount))
            self.driver.execute_script("""
                arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
                arguments[0].dispatchEvent(new Event('blur', { bubbles: true }));
            """, amount_input)
            logger.info("金額使用 send_keys 設置成功")
        except Exception as e:
            logger.error(f"send_keys 失敗: {e}, 嘗試 JavaScript 輸入")
            self.driver.execute_script("arguments[0].value = arguments[1];", amount_input, str(self.config.DP_Amount))
            self.driver.execute_script("""
                arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
                arguments[0].dispatchEvent(new Event('blur', { bubbles: true }));
            """, amount_input)
            logger.info("金額使用 JavaScript 設置成功")
        logger.info("金額設置完成")

        # 檢查優惠券下拉選單
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((
                    By.XPATH, "//div[contains(@class, 'select-container')]//div[contains(@class, 'input-container')]//div[contains(@class, 'selected-row')]"
                ))
            )
            logger.info("優惠券下拉選單已出現")
        except TimeoutException:
            logger.warning("優惠券下拉選單未出現，繼續流程")

        # # 移動到“确认”按鈕
        # try:
        #     target_button = WebDriverWait(self.driver, 15).until(
        #         EC.element_to_be_clickable(
        #             (By.XPATH, "//button[contains(@class, 'customize-button') and contains(@class, 'large') and contains(@class, 'primary') and contains(., '确认')]")
        #         ))
        #     self.driver.execute_script("arguments[0].split({block: 'end'});", target_button)
        # except TimeoutException:
        #     self.fail("无法找到确认按钮")

        target_button = WebDriverWait(self.driver, 15).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "//button[contains(@class, 'customize-button') and contains(@class, 'large') and contains(@class, 'primary') and contains(., '确认')]")
                        ))
        # 點擊確認
        WebDriverWait(self.driver, 10).until(
            lambda d: 'disabled' not in target_button.get_attribute('class')
        )
        logger.info("✅ 確認按鈕現在可以點擊")
        ActionChains(self.driver).move_to_element(target_button).click().perform()

        # 檢查是否有未支付訂單
        try:
            success_message = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//pre[contains(@class, 'description') and contains(normalize-space(text()), '您有多笔订单未支付')]"))
            )
            self.assertIn("您有多笔订单未支付", success_message.text)
            logger.info("測試用例通過：存款速度頻繁")
            return
        except TimeoutException:
            logger.warning("檢測沒有多筆訂單可繼續存款")

        # 等待頁面跳轉並檢查成功訊息
        success_message = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(text(), '请在有效期内完成')]")))
        self.assertIn("请在有效期内完成", success_message.text)
        logger.info("測試用例通過：充值成功提交")

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(DepositTest)
    runner = CustomTextTestRunner(resultclass=CleanTextTestResult,  verbosity=2)
    result = runner.run(suite)
    logger.info("測試運行完成")