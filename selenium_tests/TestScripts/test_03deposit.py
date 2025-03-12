# selenium_tests/deposit.py
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

class DepositTest(unittest.TestCase):
    def setUp(self):
        self.delay_seconds = Config.DELAY_SECONDS  # 使用 Config.DELAY_SECONDS
        self.wait_timeout = Config.WAIT_TIMEOUT
        chrome_options = Options()
        chrome_options.add_argument("--log-level=3")
        chrome_options.set_capability("goog:loggingPrefs", {"browser": "OFF"})
        #chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(
            options=chrome_options,
            service=Service(Config.CHROMEDRIVER_PATH)  # 使用 Config.CHROMEDRIVER_PATH
        )
        self.driver.get(config.LOGIN_URL)  # 使用 config.BASE_URL
        self.wait = WebDriverWait(self.driver, Config.WAIT_TIMEOUT)  # 使用 Config.WAIT_TIMEOUT
        logger.info(f"設置測試環境: {config.LOGIN_URL}")

    def test_01_01_deposit(self):
        try:
            logger.info("開始測試：充值")
            
            username = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@maxlength='18']")))
            password = self.driver.find_element(By.XPATH, "//input[@type='password']")
            login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), '登录')]")            

            username.send_keys(config.VALID_USERNAME)
            password.send_keys(config.VALID_PASSWORD)
            login_button.click()
            
            while True:
                    try:
                        close_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//i[contains(@class, 'close-btn')]")))
                        if close_button:
                            close_button.click()
                            print("彈出窗口已關閉")
                            time.sleep(self.delay_seconds)  # 等待一秒，確保下一個彈窗加載出來
                        else:
                            print("未找到關閉按鈕")
                            break
                    except Exception as TimeoutException:
                        print("沒有更多的彈出窗口")
                        break
                
        # 使用 WebDriverWait 等待充值按钮可点击
            deposit_button = WebDriverWait(self.driver,3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'toggle') and .//span[contains(@class, 'toggle-wallet') and contains(text(), '充值')]]")))
            deposit_button.click()

            bank_button = WebDriverWait(self.driver,5).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'method-item') and .//span[contains(@class, 'color-20') and contains(text(), '网银转账')]]")))
            bank_button.click()

            target_button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'customize-button') and contains(@class, 'large') and contains(@class, 'primary') and contains(@class, 'disabled') and contains(text(), '确认')]")))
            self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'end' });", target_button)
            time.sleep(self.delay_seconds)

            # 定位輸入框並確保其可交互
            amount_input = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//input[@type='number' and contains(@class, 'ng-untouched') and contains(@class, 'ng-pristine') and contains(@class, 'ng-valid')]")
                )
            )
            # 檢查輸入框狀態並記錄
            logger.info(f"輸入框可見: {amount_input.is_displayed()}, 輸入框禁用: {amount_input.get_attribute('disabled')}")
            # 檢查輸入框是否可見且可編輯
            if not amount_input.is_displayed():
                logger.error("輸入框不可見，無法操作")
                self.fail("輸入框不可見")
            if amount_input.get_attribute("disabled") == "true":
                logger.error("輸入框被禁用，無法輸入值")
                self.fail("輸入框處於禁用狀態")

            # 定位銀行下拉選單
            bank_dropdown = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "(//div[contains(@class, 'select-container')]//div[contains(@class, 'row-line') and .//i[contains(@class, 'icon-drop-down')]])[2]")
                )
            )
            bank_dropdown.click()

            bank_option = WebDriverWait(self.driver,3).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//li[contains(text(), '中国民生银行')]")
                )
            )
            bank_option.click()
            amount_input.send_keys(config.DP_Amount)
            time.sleep(self.wait_timeout)
            self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'end' });", target_button)
            target_button.click()
            time.sleep(self.wait_timeout)

            # 等待頁面轉跳並加載完成
            self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//span[contains(text(), '请在有效期内完成存款')]")
                )
            )
            logger.info("頁面已完全加載完成")

            success_message = self.wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), '请在有效期内完成存款')]")))
            self.assertIn("请在有效期内完成存款", success_message.text)
            logger.info("測試用例通過：充值成功提交")
        except Exception as e:
            logger.error(f"測試用例失敗：充值 - 錯誤: {str(e)}")
            self.fail()


    def tearDown(self):
        logger.info("測試結束，關閉瀏覽器")
        self.driver.quit()

if __name__ == "__main__":
    unittest.main(verbosity=2)


