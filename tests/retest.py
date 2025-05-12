# 執行指定的單元測試用例並捕獲輸出，檢查結果並重複運行直到失敗
import unittest
import sys
from io import StringIO
from test_01_registration import registrationPageTest,CleanTextTestResult, CustomTextTestRunner
from test_02_login import LoginPageTest,CleanTextTestResult, CustomTextTestRunner
from test_03deposit import DepositTest,CleanTextTestResult, CustomTextTestRunner

def run_tests():
    while True:
        # 重定向 stdout 以捕獲測試輸出
        buffer = StringIO()
        sys.stdout = buffer
        
        # 指定特定的測試用例
        loader = unittest.TestLoader()
        # 格式為 "module_name.ClassName.test_method_name"
        suite = loader.loadTestsFromName('test_01_registration.registrationPageTest.test_01_02_registration')
        
        # 執行測試
        # runner = unittest.TextTestRunner(stream=buffer, verbosity=2)
        runner = CustomTextTestRunner(stream=buffer, resultclass=CleanTextTestResult, verbosity=2)

        result = runner.run(suite)
        
        # 恢復 stdout 並印出結果
        sys.stdout = sys.__stdout__
        print(buffer.getvalue())
        
        # 檢查是否有錯誤或失敗
        if not result.wasSuccessful():
            print("錯誤或失敗發生，停止執行！")
            break
        
        print("測試成功，繼續重複執行...")

if __name__ == "__main__":
    run_tests()