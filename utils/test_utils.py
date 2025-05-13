# 提供單元測試輔助功能，包括日誌裝飾器、截圖保存、自定義測試結果處理及清空截圖目錄
import os # 導入 os 模組，用於處理檔案路徑和目錄操作
import time # 導入 time 模組，用於生成時間戳記
import logging # 導入 logging 模組，用於記錄測試過程中的訊息
import unittest # 導入 unittest 模組，提供測試框架
import traceback # 導入 traceback 模組，用於格式化異常堆疊追蹤
import shutil # 導入 shutil 模組，用於清空目錄
from functools import wraps # 導入 wraps，用於保留被裝飾函數的元數據
from unittest.runner import TextTestResult # 導入 TextTestResult，作為自定義結果類的基類
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 設置日誌記錄器，名稱為當前模組名稱 (__name__)
logger = logging.getLogger(__name__)

def log_and_fail_on_exception(test_func):
    """
    裝飾器：為測試方法添加日誌記錄和異常處理
    Args:
        test_func: 要裝飾的測試方法
    Returns:
        wrapper: 包裝後的函數，記錄測試開始並捕獲異常
    """
    @wraps(test_func)
    def wrapper(self, *args, **kwargs):
        display_name = test_func.__doc__ or test_func.__name__ # 使用測試方法的 docstring 或名稱作為顯示名稱
        try:
            logger.info(f"開始測試：{display_name}") # 記錄測試開始
            return test_func(self, *args, **kwargs) # 執行原始測試方法
        except Exception as e:
            logger.error(f"測試失敗：{display_name} - 錯誤: {str(e)}") # 記錄測試失敗和錯誤訊息
            self.fail() # 標記測試為失敗
    return wrapper

def wait_for_loading_to_disappear(driver, timeout=15):
    """等待畫面中的 loading 遮罩消失（支援多種常見 class 名稱）"""

    possible_loading_classes = [
        "app-local-loading",  # 你目前使用的
        "loading",            # 常見
        "spinner",            # 常見
        "overlay",            # 遮罩類型
        "loading-container",  # 元件外框
        "lds-spinner",        # 第三方 UI 套件常用
    ]

    found = False
    for class_name in possible_loading_classes:
        try:
            loading_element = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, class_name))
            )
            logger.info(f"🔄 偵測到 loading: class='{class_name}', outerHTML: {loading_element.get_attribute('outerHTML')}")
            found = True
            break
        except:
            continue

    if not found:
        logger.info("✅ 沒有偵測到 loading 畫面，繼續執行")
        return

    # 等待該 loading 元素消失
    WebDriverWait(driver, timeout).until(
        EC.invisibility_of_element_located((By.CLASS_NAME, class_name))
    )
    logger.info(f"✅ loading 已消失: class='{class_name}'")

def clear_screenshots_directory():
    """
    清空 screenshots 目錄並重新創建
    """
    screenshot_dir = "screenshots"
    if os.path.exists(screenshot_dir):
        shutil.rmtree(screenshot_dir) # 刪除目錄及其內容
    os.makedirs(screenshot_dir, exist_ok=True) # 重新創建空目錄
    logger.info("已清空 screenshots 目錄")


def clear_log_file(log_file_path="test.log"):
    """清空指定的日誌文件"""
    if os.path.exists(log_file_path):
        open(log_file_path, 'w').close()
    logger.info("已清空日誌文件")


class CleanTextTestResult(TextTestResult):
    """
    自定義測試結果類，增強 unittest 的結果處理功能
    記錄成功/失敗次數、詳細失敗資訊，並在失敗時保存截圖
    """
    def __init__(self, stream, descriptions, verbosity):
        """
        初始化自定義測試結果
        Args:
            stream: 輸出流（通常為 sys.stderr）
            descriptions: 是否顯示測試描述
            verbosity: 詳細程度（控制輸出格式）
        """
        super().__init__(stream, descriptions, verbosity)
        self.pass_count = 0 # 成功測試用例計數
        self.fail_count = 0 # 失敗/錯誤測試用例計數
        self.passed_tests = []  # 用於儲存成功的測試用例訊息
        self.failed_tests = []  # 用於儲存失敗用例的詳細資訊

    def addSuccess(self, test):
        """
        處理成功測試用例
        Args:
            test: 當前測試用例對象
        """
        super().addSuccess(test)
        self.pass_count += 1
        # 使用 docstring（如果有）或測試方法名稱來生成成功訊息
        success_msg = f"測試用例通過：{test._testMethodDoc or test._testMethodName}"
        self.passed_tests.append(success_msg)
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
            
            # 截圖處理
            if hasattr(test, 'driver'):
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                screenshot_name = f"screenshot_{test._testMethodName}_{timestamp}.png"
                screenshot_dir = "screenshots"
                os.makedirs(screenshot_dir, exist_ok=True)
                screenshot_path = os.path.join(screenshot_dir, screenshot_name)
                test.driver.save_screenshot(screenshot_path)
            else:
                screenshot_path = "無法取得 driver 截圖"

            # 使用 docstring（如果有）或測試方法名稱來生成失敗訊息
            failure_msg = f"測試用例失敗：{test._testMethodDoc or test._testMethodName} - 錯誤: {str(err[1])}"
            failure_info = {
                "test_name": failure_msg,
                "error_type": str(err[0].__name__),
                "error_message": str(err[1]),
                "stack_trace": ''.join(traceback.format_tb(err[2])),
                "screenshot": screenshot_path
            }
            self.failed_tests.append(failure_info)
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

            # 截圖處理
            if hasattr(test, 'driver'):
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                screenshot_name = f"screenshot_{test._testMethodName}_{timestamp}.png"
                screenshot_dir = "screenshots"
                os.makedirs(screenshot_dir, exist_ok=True)
                screenshot_path = os.path.join(screenshot_dir, screenshot_name)
                test.driver.save_screenshot(screenshot_path)
            else:
                screenshot_path = "無法取得 driver 截圖"

            # 使用 docstring（如果有）或測試方法名稱來生成錯誤訊息
            error_msg = f"測試用例錯誤：{test._testMethodDoc or test._testMethodName} - 錯誤: {str(err[1])}"
            error_info = {
                "test_name": error_msg,
                "error_type": str(err[0].__name__),
                "error_message": str(err[1]),
                "stack_trace": ''.join(traceback.format_tb(err[2])),
                "screenshot": screenshot_path
            }
            self.failed_tests.append(error_info)
        logger.error(f"測試用例錯誤: {test._testMethodName} - 錯誤: {str(err[1])}")
        if self.showAll:
            self.stream.write('')
        elif self.dots:
            self.stream.write('')
            self.stream.flush()

    def printErrors(self):
        pass

    def printSummary(self):
        # 不再直接打印，而是由主進程負責打印
        pass

    def get_results(self):
        """返回結構化的測試結果，包括成功和失敗用例"""
        total = self.pass_count + self.fail_count
        return {
            "summary": {
                "pass_count": self.pass_count,
                "fail_count": self.fail_count,
                "total_count": total
            },
            "passed_tests": self.passed_tests,  # 返回成功的測試用例訊息
            "failed_tests": self.failed_tests,  # 返回成功的測試用例訊息
            # "failed_tests": [test["test_name"] for test in self.failed_tests]  # 返回失敗訊息
        }

class CustomTextTestRunner(unittest.TextTestRunner):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.verbosity = 0

    def run(self, test):
        clear_screenshots_directory() # 在測試運行前清空截圖目錄
        clear_log_file()  # 清空日誌文件
        result = super().run(test)
        # 不再調用 printSummary，由主進程負責打印總結
        return result