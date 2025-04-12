# selenium_tests/main.py
import os
import unittest
import logging
from tests.test_01_registration import registrationPageTest,CleanTextTestResult, CustomTextTestRunner
from tests.test_02_login import LoginPageTest,CleanTextTestResult, CustomTextTestRunner
from tests.test_03deposit import DepositTest,CleanTextTestResult, CustomTextTestRunner
from config.config import Config
    
# 設置日誌文件路徑為 selenium_tests/test_log.log
log_dir = '/Users/steven/deepseek/seleium/tests'
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
    config = Config.get_current_config() 
    logger.info(f"開始運行測試，當前環境: {config.BASE_URL}")
    suite = unittest.TestLoader().loadTestsFromTestCase(LoginPageTest)
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(registrationPageTest))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(DepositTest))
    runner = CustomTextTestRunner(resultclass=CleanTextTestResult, verbosity=2)
    result = runner.run(suite)
    logger.info("測試運行完成")