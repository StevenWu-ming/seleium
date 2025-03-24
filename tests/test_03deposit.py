import os
import sys
# 添加項目根目錄到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import logging
import time  # 添加時間模塊導入
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import unittest
from utils.test_utils import CleanTextTestResult, CustomTextTestRunner
from selenium.common.exceptions import StaleElementReferenceException  # 確保導入
from BaseTest import BaseTest
from config.config import config


# 設置日誌文件路徑
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

class CustomTextTestRunner(unittest.TextTestRunner):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.verbosity = 0

    def run(self, test):
        result = super().run(test)
        if hasattr(result, 'printSummary'):
            result.printSummary()
        return result

class DepositTest(BaseTest):
    def setUp(self):
        self.url = config.LOGIN_URL  # 指定註冊頁面
        print(f"設定的測試 URL: {self.url}")
        super().setUp()  # 調用 BaseTest 的 setUp()
    
    def test_01_01_deposit(self):
        """充值"""
        
        try:
            logger.info("開始測試：充值")
            # 登入
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@maxlength='18']"))).send_keys(config.VALID_DP_USERNAME)
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))).send_keys(config.VALID_PASSWORD)
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), '登录')]"))).click()

            # 關閉公告
            # 關閉公告
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

            # 等待遮罩層消失
            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "cdk-overlay-backdrop"))
            )
            
            # 點擊充值按鈕
            # WebDriverWait(self.driver, 1).until(EC.element_to_be_clickable((
            #     By.XPATH, "//div[contains(@class, 'toggle') and .//span[contains(@class, 'toggle-wallet') and contains(text(), '充值')]]"))).click()

            element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.toggle")))
            self.driver.execute_script("arguments[0].click();", element)

            # 點擊“网银转账”
            # WebDriverWait(self.driver, 5).until(
            #     EC.element_to_be_clickable((
            #         By.XPATH, "//div[contains(@class, 'method-item') and .//span[contains(@class, 'color-20') and contains(text(), '网银转账')]]"
            #     ))
            # ).click()

            # 等待遮罩層消失
            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "cdk-overlay-backdrop"))
            )
            
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
                ))
            )
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

            # 選擇“中国民生银行”（添加截圖功能）
            try:
                bank_option = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, "//li[contains(text(), '中国民生银行')]"))
                )
                self.driver.execute_script("arguments[0].scrollIntoView(true);", bank_option)
                self.driver.execute_script("arguments[0].click();", bank_option)
                logger.info("已選擇 '中国民生银行'")
            except TimeoutException as e:
                screenshot_path = os.path.join(log_dir, f"screenshot_bank_option_failure_{int(time.time())}.png")
                self.driver.save_screenshot(screenshot_path)
                logger.error(f"无法找到银行选项: {str(e)}，截圖已保存至: {screenshot_path}")
                self.fail(f"充值测试失败: 无法找到 '中国民生银行' 选项")

            # 移動到“确认”按鈕
            try:
                target_button = WebDriverWait(self.driver, 15).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[contains(@class, 'customize-button') and contains(@class, 'large') and contains(@class, 'primary') and contains(., '确认')]")
                    )
                )
                print("找到目标按钮:", target_button.text)
                # ActionChains(self.driver).move_to_element(target_button).perform()
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'end'});", target_button)
                print("成功移动到按钮")
            except TimeoutException:
                print("TimeoutException: Failed to locate the button")
                print("页面源代码:", self.driver.page_source)
                self.fail("无法找到确认按钮")

            

            # 定位優惠券下拉選單
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((
                By.XPATH, "//div[contains(@class, 'select-container')]//div[contains(@class, 'input-container')]//div[contains(@class, 'selected-row')]")))

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
            
        except TimeoutException as e:
            logger.error(f"測試超時: {str(e)}")
            self.fail()
        except Exception as e:
            logger.error(f"測試失敗: {str(e)}")
            self.fail()



if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(DepositTest)
    runner = CustomTextTestRunner(resultclass=CleanTextTestResult, verbosity=2)
    result = runner.run(suite)
    logger.info("測試運行完成")