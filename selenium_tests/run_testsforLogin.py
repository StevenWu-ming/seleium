# selenium_tests/run_testsforLogin.py
import os
import unittest
import logging
from test_02_login import LoginPageTest, CleanTextTestResult, CustomTextTestRunner
from config import config

# 設置日誌文件路徑為 selenium_tests/test_log.log
log_dir = os.path.dirname(__file__)  # 獲取當前腳本所在目錄 (selenium_tests)
log_file = os.path.join(log_dir, 'test_log.log')  # 直接放在 selenium_tests 根目錄

# 配置日誌，調整級別為 INFO
logging.basicConfig(
    level=logging.INFO,  # 改為 INFO 級別
    format='%(asctime)s - %(levelname)s - [%(name)s] %(message)s',
    handlers=[
        logging.FileHandler(log_file, mode='w'),
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info(f"開始運行測試，當前環境: {config.BASE_URL}")
    suite = unittest.TestLoader().loadTestsFromTestCase(LoginPageTest)
    runner = CustomTextTestRunner(resultclass=CleanTextTestResult, verbosity=0)
    result = runner.run(suite)
    logger.info("測試運行完成")