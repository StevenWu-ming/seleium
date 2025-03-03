# run_testsforLogin.py
import unittest
from selenium_tests.test_loginByType import LoginPageTest, CleanTextTestResult, CustomTextTestRunner

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(LoginPageTest)
    runner = CustomTextTestRunner(resultclass=CleanTextTestResult, verbosity=2)
    runner.run(suite)