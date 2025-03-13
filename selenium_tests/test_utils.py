import logging
import traceback
from unittest.runner import TextTestResult
import unittest

logger = logging.getLogger(__name__)

class CleanTextTestResult(TextTestResult):
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.pass_count = 0
        self.fail_count = 0
        self.passed_tests = []  # 用於儲存成功的測試用例訊息
        self.failed_tests = []  # 用於儲存失敗用例的詳細資訊

    def addSuccess(self, test):
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
            # 使用 docstring（如果有）或測試方法名稱來生成失敗訊息
            failure_msg = f"測試用例失敗：{test._testMethodDoc or test._testMethodName} - 錯誤: {str(err[1])}"
            failure_info = {
                "test_name": failure_msg,
                "error_type": str(err[0].__name__),
                "error_message": str(err[1]),
                "stack_trace": ''.join(traceback.format_tb(err[2]))
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
            # 使用 docstring（如果有）或測試方法名稱來生成錯誤訊息
            error_msg = f"測試用例錯誤：{test._testMethodDoc or test._testMethodName} - 錯誤: {str(err[1])}"
            error_info = {
                "test_name": error_msg,
                "error_type": str(err[0].__name__),
                "error_message": str(err[1]),
                "stack_trace": ''.join(traceback.format_tb(err[2]))
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
        total = self.pass_count + self.fail_count
        logger.info(f"\n📌測試結果摘要:")
        logger.info(f"✅通過測試數: {self.pass_count}")
        logger.info(f"❌失敗測試數: {self.fail_count}")
        logger.info(f"📊總測試數: {total}")

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
            "failed_tests": [test["test_name"] for test in self.failed_tests]  # 返回失敗訊息
        }

class CustomTextTestRunner(unittest.TextTestRunner):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.verbosity = 0

    def run(self, test):
        result = super().run(test)
        if hasattr(result, 'printSummary'):
            result.printSummary()
        return result