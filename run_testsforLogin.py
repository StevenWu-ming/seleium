# run_testsforLogin.py
import unittest
from selenium_tests.test_login import LoginPageTest, CleanTextTestResult, CustomTextTestRunner

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(LoginPageTest)
    runner = CustomTextTestRunner(resultclass=CleanTextTestResult, verbosity=0)  # 將 verbosity 設置為 0
    runner.run(suite)


