import unittest # 導入 Python 的單元測試框架
from selenium import webdriver # 導入 Selenium WebDriver，用於模擬瀏覽器操作
from selenium.webdriver.chrome.service import Service # 導入 Service 類，用於指定
from selenium.webdriver.chrome.options import Options # 導入 Options 類，用於設置
from selenium.webdriver.support.ui import WebDriverWait
from config.config import Config  # 導入自定義的 Config 模組，用於管理測試配置
import logging # 導入 logging 模組，用於記錄測試過程中的訊息


logger = logging.getLogger(__name__) # 設置日誌記錄器，名稱為當前模組名稱 (__name__)
config = Config.get_current_config()   # 動態獲取當前環境的配置實例，確保每次運行都使用最新的配置


class BaseTest(unittest.TestCase): # 定義基礎測試類別，繼承自 unittest.TestCase，提供測試的基本結構
    # setUp 方法在每個測試用例開始前運行，用於初始化測試環境
    def setUp(self):
        self.delay_seconds = Config.DELAY_SECONDS # 從配置中獲取延遲時間（單位：秒），用於控制測試步驟間的等待
        chrome_options = Options() # 創建 Chrome 瀏覽器選項對象，用於設置瀏覽器行為
        chrome_options.add_argument("--log-level=3") # 設置 Chrome 日誌級別為 3（僅顯示嚴重錯誤），減少不必要的輸出
        chrome_options.set_capability("goog:loggingPrefs", {"browser": "OFF"}) # 關閉瀏覽器控制台日誌，提升測試效率
        # chrome_options.add_argument("--headless") # 啟用無頭模式（不顯示瀏覽器窗口），適合在無圖形界面的環境運行
        chrome_options.add_argument("--no-sandbox") # 禁用沙盒模式，提升在某些系統上的相容性
        chrome_options.add_argument("--disable-dev-shm-usage") # 禁用 /dev/shm 使用，避免在容器化環境中出現記憶體問題

        # 初始化 Chrome WebDriver，使用指定的選項和 ChromeDriver 路徑
        self.driver = webdriver.Chrome(
            options=chrome_options,
            service=Service(Config.CHROMEDRIVER_PATH) # 指定 ChromeDriver 可執行文件的路
        )
        self.wait = WebDriverWait(self.driver, Config.WAIT_TIMEOUT)  # 初始化 WebDriverWait 對象，用於等待網頁元素載入完成，超時時間從配置中獲取
        self.driver.set_window_position(-1500, -500)  # 設置瀏覽器窗口位置

        # 檢查子類別是否定義了 self.url，如果有則載入該網址
        if hasattr(self, "url") and self.url:  # 只有在子類別有設定 `self.url` 才會載入
            self.driver.get(self.url) # 打開指定的網頁
            logger.info(f"設置測試環境: {self.url}") # 記錄載入的網址

    def tearDown(self):
        logger.info("測試結束，關閉瀏覽器") # 記錄測試結束的訊息
        self.driver.quit() # 關閉瀏覽器並釋放資源
