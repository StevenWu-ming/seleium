import os
import sys
# 添加項目根目錄到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import time
import logging
import unittest
from config.config import Config,config
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from config.BaseTest import BaseTest
from selenium.common.exceptions import StaleElementReferenceException  # 確保導入
from config.selenium_helpers import close_popup, perform_login, wait_for_success_message
from utils.test_utils import CleanTextTestResult, CustomTextTestRunner, log_and_fail_on_exception
from config.selenium_helpers import close_popup, perform_login, wait_for_success_message, wait_for_err_message, input_text, click_element



CustomTextTestRunner(unittest.TextTestRunner)


# 設置日誌文件路徑
log_dir = os.path.dirname(__file__)
log_file = os.path.join(log_dir, 'test_log.log')
# 配置日誌，調整級別為 INFO
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
        self.url = config.LOGIN_URL  # 指定註冊頁面
        print(f"設定的測試 URL: {self.url}")
        super().setUp()  # 調用 BaseTest 的 setUp()
        
    @log_and_fail_on_exception
    def test_01_01_deposit(self):
        """充值"""
        # 輸入使用者名稱到指定輸入框（最大長度為18個字元）
        input_text(self.driver, self.wait, "//input[@maxlength='18']", (config.VALID_USERNAME))
        # 輸入密碼到密碼輸入框
        input_text(self.driver, self.wait, "//input[@type='password']", (config.VALID_PASSWORD))
        # 點擊包含“登录”文字的按鈕來提交登入表單
        click_element(self.driver, self.wait, "//button[contains(text(), '登录')]")

        #關閉公告彈窗
        close_popup(self.driver, self.wait)

        # 等待遮罩層消失
        WebDriverWait(self.driver, 5).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "cdk-overlay-backdrop")))
    
        # 點擊充值按鈕
        # WebDriverWait(self.driver, 1).until(EC.element_to_be_clickable((
        #     By.XPATH, "//div[contains(@class, 'toggle') and .//span[contains(@class, 'toggle-wallet') and contains(text(), '充值')]]"))).click()

        # 點擊“网银转账”
        # WebDriverWait(self.driver, 5).until(
        #     EC.element_to_be_clickable((
        #         By.XPATH, "//div[contains(@class, 'method-item') and .//span[contains(@class, 'color-20') and contains(text(), '网银转账')]]"
        #     ))
        # ).click()

        element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.toggle")))
        self.driver.execute_script("arguments[0].click();", element)

        # 等待遮罩層消失
        WebDriverWait(self.driver, 5).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "cdk-overlay-backdrop")))
        
        element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.method-item")))
        self.driver.execute_script("arguments[0].click();", element)


        # 輸入金額
        amount_input = self.wait.until(EC.presence_of_element_located((
            By.XPATH, "//input[@type='number' and contains(@class, 'ng-untouched') and contains(@class, 'ng-pristine') and contains(@class, 'ng-valid')]")))
        self.driver.execute_script("arguments[0].value = arguments[1];", amount_input, config.DP_Amount)
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", amount_input)


        # 點擊銀行下拉框
        
        bank_dropdown = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((
                By.XPATH, "(//div[contains(@class, 'select-container')]//div[contains(@class, 'row-line') and .//i[contains(@class, 'icon-drop-down')]])[2]"
            )))
        
        #快速滾動
        # self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", bank_dropdown)
        #緩慢滾動
        self.driver.execute_script("""
            arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});
        """, bank_dropdown)
        # bank_dropdown.click()
        self.driver.execute_script("arguments[0].click();", bank_dropdown)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", bank_dropdown)
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
            print("找到目标按钮:", target_button.text)
            # ActionChains(self.driver).move_to_element(target_button).perform()
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'end'});", target_button)
            print("成功移动到按钮")
        except TimeoutException:
            print("TimeoutException: Failed to locate the button")
            print("页面源代码:", self.driver.page_source)
            self.fail("无法找到确认按钮")

        # # 定位優惠券下拉選單
        # WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((
        #     By.XPATH, "//div[contains(@class, 'select-container')]//div[contains(@class, 'input-container')]//div[contains(@class, 'selected-row')]")))

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
    runner = CustomTextTestRunner(resultclass=CleanTextTestResult, verbosity=2)
    result = runner.run(suite)
    logger.info("測試運行完成")