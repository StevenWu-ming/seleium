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
from unittest.runner import TextTestResult
from config import Config, config  # 導入 Config 和 config
from test_utils import CleanTextTestResult, CustomTextTestRunner
from selenium.webdriver.common.action_chains import ActionChains

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
        # 呼叫父類別（unittest.TextTestRunner）的初始化方法
        super().__init__(*args, **kwargs)
        # 設定 verbosity 為 0，表示不輸出詳細的測試資訊
        self.verbosity = 0

    def run(self, test):
        # 呼叫父類別的 run 方法來執行測試，並獲取測試結果
        result = super().run(test)
        
        # 檢查測試結果物件是否有 printSummary 方法
        if hasattr(result, 'printSummary'):
            # 如果有，則呼叫 printSummary 方法來輸出測試摘要
            result.printSummary()
        
        # 返回測試結果
        return result

# 主測試程式
class DepositTest(unittest.TestCase):
    def setUp(self):
        # 從 Config 中讀取延遲時間（DELAY_SECONDS）並存儲到實例變數 self.delay_seconds
        self.delay_seconds = Config.DELAY_SECONDS  # 使用 Config.DELAY_SECONDS
        
        # 從 Config 中讀取等待超時時間（WAIT_TIMEOUT）並存儲到實例變數 self.wait_timeout
        self.wait_timeout = Config.WAIT_TIMEOUT
        
        # 創建 Chrome 瀏覽器的選項物件
        chrome_options = Options()
        
        # 設置 Chrome 的日誌級別為 3（只顯示錯誤訊息），減少不必要的日誌輸出
        chrome_options.add_argument("--log-level=3")
        
        # 禁用瀏覽器的日誌記錄功能
        chrome_options.set_capability("goog:loggingPrefs", {"browser": "OFF"})
        
        # 如果需要以無頭模式運行 Chrome，可以取消註解以下行
        # chrome_options.add_argument("--headless")
        
        # Selenium 只會等待 DOM 加載完成，而不會等待所有資源（如圖片）加載完成。
        chrome_options.page_load_strategy = "eager"

        # 初始化 Chrome WebDriver，傳入瀏覽器選項和 ChromeDriver 的路徑
        self.driver = webdriver.Chrome(
            options=chrome_options,
            service=Service(Config.CHROMEDRIVER_PATH)  # 使用 Config.CHROMEDRIVER_PATH
        )
        
        # 打開登錄頁面（URL 從 config.LOGIN_URL 中讀取）
        self.driver.get(config.LOGIN_URL)  # 使用 config.LOGIN_URL
        
        # 初始化 WebDriverWait 物件，用於在測試中等待特定條件成立
        self.wait = WebDriverWait(self.driver, Config.WAIT_TIMEOUT)  # 使用 Config.WAIT_TIMEOUT
        
        # 使用 logger 記錄測試環境設置的日誌訊息
        logger.info(f"設置測試環境: {config.LOGIN_URL}")

    def test_01_01_deposit(self):
        """充值"""
        try:
            logger.info("開始測試：充值")
            #登入
            # 等待使用者名稱輸入框出現，並輸入有效的使用者名稱
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@maxlength='18']"))).send_keys(config.VALID_DP_USERNAME)

            # 等待密碼輸入框出現，並輸入有效的密碼
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))).send_keys(config.VALID_PASSWORD)

            # 等待登錄按鈕出現，並點擊它
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), '登录')]"))).click()

            #關閉公告
            # 進入一個無限循環，持續嘗試關閉彈出窗口
            while True:
                try:
                    # 使用 WebDriverWait 等待關閉按鈕出現並可點擊
                    # EC.element_to_be_clickable 確保按鈕不僅存在於 DOM 中，而且是可以點擊的
                    # By.XPATH 指定使用 XPATH 定位元素
                    # "//i[contains(@class, 'close-btn')]" 是 XPATH 表達式，用於找到 class 包含 'close-btn' 的 <i> 元素
                    close_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//i[contains(@class, 'close-btn')]")))

                    # 檢查是否成功找到關閉按鈕
                    if close_button:
                        # 如果找到關閉按鈕，則點擊它
                        close_button.click()
                    else:
                        # 如果未找到關閉按鈕，則跳出循環
                        break
                except Exception as TimeoutException:
                    # 如果在等待過程中發生超時（即未找到關閉按鈕），則跳出循環
                    break
            # 等待遮罩層消失
            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "cdk-overlay-backdrop"))
            )                
            # 等待充值按鈕出現並可點擊，然後點擊它
            WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((
                By.XPATH, "//div[contains(@class, 'toggle') and .//span[contains(@class, 'toggle-wallet') and contains(text(), '充值')]]"))).click()


            # 等待并点击“网银转账”按钮
            WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((
                By.XPATH, "//div[contains(@class, 'method-item') and .//span[contains(@class, 'color-20') and contains(text(), '网银转账'"")]]"))).click()


            # 等待“网银转账”按钮可点击并执行点击操作
            WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((
                By.XPATH, "//div[contains(@class, 'method-item') and .//span[contains(@class, 'color-20') and contains(text(), '网银转账')]]"))).click()

            # 等待并移動到“确认”按钮
            target_button = self.wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//button[contains(@class, 'customize-button') and contains(@class, 'large') and contains(@class, 'primary') and contains(@class, 'disabled') and contains(., '确认')]")
            ))            
            ActionChains(self.driver).move_to_element(target_button).perform()
            
            # 等待金额输入框可点击
            amount_input = self.wait.until(EC.element_to_be_clickable((
                    By.XPATH, "//input[@type='number' and contains(@class, 'ng-untouched') and contains(@class, 'ng-pristine') "
                    "and contains(@class, 'ng-valid')]")))

            # 使用 JavaScript 设置金额输入框的值
            self.driver.execute_script("arguments[0].value = arguments[1];", amount_input, config.DP_Amount)

            # 触发输入事件，确保输入框的值被更新
            self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", amount_input)


            # 等待并点击银行下拉框
            bank_dropdown = WebDriverWait(self.driver, 5) .until(EC.presence_of_element_located((
                By.XPATH, "(//div[contains(@class, 'select-container')]//div[contains(@class, 'row-line') and .//i[contains(@class, 'icon-drop-down')]])[2]"
            )))

            # 確保元素可見並滾動到可點擊範圍
            self.driver.execute_script("arguments[0].scrollIntoView(true);", bank_dropdown)

            # 使用 ActionChains 避免點擊失敗
            ActionChains(self.driver).move_to_element(bank_dropdown).click().perform()
            # 等待并选择“中国民生银行”选项
            bank_option = WebDriverWait(self.driver,2).until(
                EC.element_to_be_clickable((
                By.XPATH, "//li[contains(text(), '中国民生银行')]")))
            bank_option.click() 

            # 定位優惠卷下拉選單 主要輸入金額後要判斷他已經出現才可以點確認 所以他會定位但不會用到他
            selected_row = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((
                By.XPATH, "//div[contains(@class, 'select-container')]//div[contains(@class, 'input-container')]//div[contains(@class, 'selected-row')]")))
    
            # 點擊確認
            target_button.click()

            #有多筆訂單未確認 會跳入這判斷 一樣判斷存款成功     
            try:
                success_message = WebDriverWait(self.driver, 15).until(
                    EC.visibility_of_element_located((By.XPATH, "//pre[contains(@class, 'description') and contains(normalize-space(text()), '您有多笔订单未支付')]"))
                )
                self.assertIn("您有多笔订单未支付", success_message.text)
                logger.info("測試用例通過：存款速度頻繁")
                self.assertIsNotNone(success_message)
                return

            except Exception as e:
                logger.warning(f"檢測沒有多筆訂單可繼續存款")

            # 等待頁面轉跳並加載完成
            self.wait.until(
                EC.presence_of_element_located((
                By.XPATH, "//span[contains(text(), '请在有效期内完成')]")))

            #  判斷成功訊息
            success_message = self.wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), '请在有效期内完成')]")))
            self.assertIn("请在有效期内完成", success_message.text)
            logger.info("測試用例通過：充值成功提交")
        except Exception as e:
            logger.error(f"測試用例失敗：充值 - 錯誤: {str(e)}")
            self.fail()

    def tearDown(self):
        logger.info("測試結束，關閉瀏覽器")
        self.driver.quit()

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(DepositTest)
    runner = CustomTextTestRunner(resultclass=CleanTextTestResult, verbosity=2)
    result = runner.run(suite)
    logger.info("測試運行完成")


