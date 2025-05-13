import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import time
import logging
import unittest
import traceback  # 導入 traceback 模塊
from config.config import Config
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from config.BaseTest import BaseTest
from selenium.common.exceptions import TimeoutException, WebDriverException
from config.selenium_helpers import close_popup, perform_login, wait_for_success_message, wait_for_err_message, input_text, click_element
from utils.test_utils import CleanTextTestResult, CustomTextTestRunner, log_and_fail_on_exception , wait_for_loading_to_disappear
from testbackend.sc_otp import DepositRiskProcessor
from testbackend.sc_login_aeskey_api import run_admin_login_workflow

CustomTextTestRunner(unittest.TextTestRunner)

# 日誌配置
log_dir = os.path.dirname(__file__)
log_file = os.path.join(log_dir, 'test_log.log')
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(name)s] %(message)s',
    handlers=[
        logging.FileHandler(log_file, mode='a', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class withdrawal(BaseTest):
    def setUp(self):
        self.config = Config.get_current_config()
        self.url = self.config.LOGIN_URL
        print(f"設定的測試 URL: {self.url}")
        super().setUp()

    @log_and_fail_on_exception
    def test_04_01_withdrawal(self):
        """提款"""
        # 登入
        perform_login(self.driver, self.wait, self.config.VALID_WD_USERNAME, self.config.VALID_PASSWORD)
        
        try:
            success_message = wait_for_success_message(self.wait, "我的钱包")
            self.assertIn("我的钱包", success_message)
            logger.info("測試用例通過：手機號碼直接登入成功")

        except Exception as direct_login_error:
            logger.warning(f"直接登入失敗，可能需要驗證碼: {str(direct_login_error)}")
            click_element(
                self.driver, self.wait, "//div[contains(@class, 'input-group-txt') and contains(@class, 'get-code')]")
            
            phone_number = self.config.PHONE_NUMBER
            last_six_digits = phone_number[-6:]
            input_elements = self.driver.find_elements(By.XPATH, "//code-input//input[@type='number']")
            if len(input_elements) != 6:
                raise Exception("未找到六個驗證碼輸入框")
            for i in range(6):
                input_elements[i].clear()
                input_elements[i].send_keys(last_six_digits[i])
            click_element(self.driver, self.wait, "//div[@class='btn-container']//button[contains(text(), '确定')]")
            success_toast = self.wait.until(EC.presence_of_element_located((
                By.XPATH, "//div[contains(@class, 'toast-text')]//p[contains(text(), '成功')]")))
            print(f"驗證碼發送成功{success_toast}")

            run_admin_login_workflow()
            processor = DepositRiskProcessor()
            
            verify_codes = processor.otp()
            if verify_codes:
                verify_code = verify_codes[0]
            else:
                raise Exception("無法獲取驗證碼")

            input_text(
                self.driver, self.wait, "//div[contains(@class, 'input-group')]//input[@type='number' and @maxlength='6']", verify_code)
            time.sleep(self.delay_seconds)

            close_popup(self.driver, self.wait)

            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "cdk-overlay-backdrop")))

        if Config.ENV == "ProdEnv":
            self.deposit_method_b()
        else:  # TestEnv
            self.deposit_method_a()

    def deposit_method_a(self):
        """提款方式 A (TestEnv)"""
        # 轉跳提款介面
        self.WD_URL = self.config.WD_URL
        self.driver.get(self.WD_URL)
        logger.info(f"轉跳提款介面: {self.WD_URL}")
        
        # 定位幣種選單
        coin_dropdown = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='select' and .//i[@class='icon-drop-down']]")))
        self.driver.execute_script("arguments[0].click();", coin_dropdown)

        # 選擇“幣種”
        coin_option = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'select-row')]//span[text()='CNY']")))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", coin_option)
        self.driver.execute_script("arguments[0].click();", coin_option)
        logger.info("已選擇 'CNY'")

        WebDriverWait(self.driver, 10).until(lambda d: d.execute_script("return document.readyState === 'complete'"))
        logger.info("頁面加載完成")

        # 選擇“网银转账”
        # 定位“網銀轉帳”元素
        label_option = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((
            By.XPATH, "//mat-radio-button[.//div[contains(@class, 'row') and contains(., '网银转账')]]//label")))
        
        # 使用 ActionChains 模擬用戶點擊
        # ActionChains(self.driver).move_to_element(label_option).click().perform()
        # logger.info("使用 ActionChains 點擊 label")

        # 備用方式：使用 JavaScript 點擊
        self.driver.execute_script("arguments[0].click();", label_option)
        logger.info("改用 JavaScript 點擊 label")
        
        # 第一次"繼續"按鈕
        go_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((
            By.XPATH, "//button[contains(@class, 'customize-button') and contains(@class, 'medium') and contains(@class, 'primary') and contains(., ' 继续 ')]")))
        
        WebDriverWait(self.driver, 15).until(
            lambda d: 'disabled' not in go_button.get_attribute('class'))
        
        logger.info("✅ 確認按鈕現在可以點擊")
        ActionChains(self.driver).move_to_element(go_button).click().perform()
        
        # 輸入金額
        amount_input = self.wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, "div.input-container.large input[type='number']")))
        self.driver.execute_script("arguments[0].value = arguments[1];", amount_input, self.config.WD_Amount)
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", amount_input)


        # 等待並定位「第一個銀行選項」的 radio 按鈕 input 元素
        radio_input = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((
            By.XPATH, "(//div[contains(@class, 'card-box') and contains(@class, 'added')]//input[@type='radio'])[1]"
        )))
        logger.info(f"成功定位 radio input: {radio_input.get_attribute('outerHTML')}")

        # 檢查狀態
        logger.info(f"元素可見: {radio_input.is_displayed()}")
        logger.info(f"元素可點擊: {radio_input.is_enabled()}")


        # 使用 JavaScript 點擊 radio
        self.driver.execute_script("arguments[0].click();", radio_input)
        logger.info("已透過 JavaScript 點擊第一個銀行 radio 按鈕")


        # 滾動到父層
        try:
            mall_next_div = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'small-next')]")))            
            # 滾動到父層元素
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", mall_next_div)
        except Exception as e:
            logger.error(f"無法找到父層 div.small-next: {str(e)}")
            raise

        # 第二次"繼續"按鈕檢查父層內的所有按鈕
        try:
            buttons = mall_next_div.find_elements(By.XPATH, ".//button")
            logger.info(f"在 div.small-next 中找到 {len(buttons)} 個按鈕")
        except Exception as e:
            logger.error(f"無法在 div.small-next 中找到按鈕: {str(e)}")
            raise

        # 確保至少有一個按鈕
        if buttons:
            go_button_2 = buttons[0]  # 選擇第一個按鈕（因為 div.small-next 中只有一個按鈕）
            self.driver.execute_script("arguments[0].click();", go_button_2)
        else:
            logger.error("divsmall-next 中沒有按鈕")
            raise Exception("無法找到按鈕")
        

        # 定位並點擊目標 第三次"繼續" 按鈕
        try:
            # 直接定位符合條件的 customize-button
            target_customize_button = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//customize-button[@class='n-m' and @size='large']")))
            logger.info("成功找到符合條件的 customize-button")

            # 定位內層的按鈕
            continue_button = target_customize_button.find_element(By.XPATH, ".//button[contains(@class, 'customize-button')]")
            logger.info(f"成功定位繼續按鈕: {continue_button.get_attribute('outerHTML')}")

            # 確保按鈕未被禁用
            WebDriverWait(self.driver, 15).until(
                lambda d: 'disabled' not in continue_button.get_attribute('class'))
            logger.info("按鈕未被禁用")

            # 點擊按鈕
            logger.info("✅ 正在點擊繼續按鈕")
            ActionChains(self.driver).move_to_element(continue_button).click().perform()

        except Exception as e:
            logger.error(f"無法定位或點擊繼續按鈕: {str(e)}")
            raise






    # 將 deposit_method_b 方法完整註解掉，這樣這段代碼不會被執行
    def deposit_method_b(self):
        """提款方式 B (ProdEnv)"""
        # 轉跳提款介面
        self.WD_URL = self.config.WD_URL
        self.driver.get(self.WD_URL)
        logger.info(f"轉跳提款介面: {self.WD_URL}")
        
        # 定位幣種選單
        coin_dropdown = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='select' and .//i[@class='icon-drop-down']]")))
        self.driver.execute_script("arguments[0].click();", coin_dropdown)

        # 選擇“幣種”
        coin_option = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'select-row')]//span[text()='CNY']")))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", coin_option)
        self.driver.execute_script("arguments[0].click();", coin_option)
        logger.info("已選擇 'CNY'")

        WebDriverWait(self.driver, 10).until(lambda d: d.execute_script("return document.readyState === 'complete'"))
        logger.info("頁面加載完成")

        # 選擇“网银转账”
        # 定位“網銀轉帳”元素
        label_option = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((
            By.XPATH, "//mat-radio-button[.//div[contains(@class, 'row') and contains(., '网银转账')]]//label")))
        
        # 使用 ActionChains 模擬用戶點擊
        # ActionChains(self.driver).move_to_element(label_option).click().perform()
        # logger.info("使用 ActionChains 點擊 label")

        # 備用方式：使用 JavaScript 點擊
        self.driver.execute_script("arguments[0].click();", label_option)
        logger.info("改用 JavaScript 點擊 label")
        
        # 第一次"繼續"按鈕
        go_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((
            By.XPATH, "//button[contains(@class, 'customize-button') and contains(@class, 'medium') and contains(@class, 'primary') and contains(., ' 继续 ')]")))
        
        WebDriverWait(self.driver, 15).until(
            lambda d: 'disabled' not in go_button.get_attribute('class'))
        
        logger.info("✅ 確認按鈕現在可以點擊")
        ActionChains(self.driver).move_to_element(go_button).click().perform()
        
        # 輸入金額
        amount_input = self.wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, "div.input-container.large input[type='number']")))
        self.driver.execute_script("arguments[0].value = arguments[1];", amount_input, self.config.WD_Amount)
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", amount_input)


        # 等待並定位「第一個銀行選項」的 radio 按鈕 input 元素
        radio_input = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((
            By.XPATH, "(//div[contains(@class, 'card-box') and contains(@class, 'added')]//input[@type='radio'])[1]"
        )))
        logger.info(f"成功定位 radio input: {radio_input.get_attribute('outerHTML')}")

        # 檢查狀態
        logger.info(f"元素可見: {radio_input.is_displayed()}")
        logger.info(f"元素可點擊: {radio_input.is_enabled()}")


        # 使用 JavaScript 點擊 radio
        self.driver.execute_script("arguments[0].click();", radio_input)
        logger.info("已透過 JavaScript 點擊第一個銀行 radio 按鈕")


        # 滾動到父層
        try:
            mall_next_div = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'small-next')]")))            
            # 滾動到父層元素
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", mall_next_div)
        except Exception as e:
            logger.error(f"無法找到父層 div.small-next: {str(e)}")
            raise

        # 第二次"繼續"按鈕檢查父層內的所有按鈕
        try:
            buttons = mall_next_div.find_elements(By.XPATH, ".//button")
            logger.info(f"在 div.small-next 中找到 {len(buttons)} 個按鈕")
        except Exception as e:
            logger.error(f"無法在 div.small-next 中找到按鈕: {str(e)}")
            raise

        # 確保至少有一個按鈕
        if buttons:
            go_button_2 = buttons[0]  # 選擇第一個按鈕（因為 div.small-next 中只有一個按鈕）
            self.driver.execute_script("arguments[0].click();", go_button_2)
        else:
            logger.error("divsmall-next 中沒有按鈕")
            raise Exception("無法找到按鈕")
        

        # 定位並點擊目標 第三次"繼續" 按鈕
        try:
            # 直接定位符合條件的 customize-button
            target_customize_button = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//customize-button[@class='n-m' and @size='large']")))
            logger.info("成功找到符合條件的 customize-button")

            # 定位內層的按鈕
            continue_button = target_customize_button.find_element(By.XPATH, ".//button[contains(@class, 'customize-button')]")
            logger.info(f"成功定位繼續按鈕: {continue_button.get_attribute('outerHTML')}")

            # 確保按鈕未被禁用
            WebDriverWait(self.driver, 15).until(
                lambda d: 'disabled' not in continue_button.get_attribute('class'))
            logger.info("按鈕未被禁用")

            # 點擊按鈕
            logger.info("✅ 正在點擊繼續按鈕")
            ActionChains(self.driver).move_to_element(continue_button).click().perform()

        except Exception as e:
            logger.error(f"無法定位或點擊繼續按鈕: {str(e)}")
            raise
    

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(withdrawal)
    runner = CustomTextTestRunner(resultclass=CleanTextTestResult, verbosity=2)
    result = runner.run(suite)
    logger.info("測試運行完成")