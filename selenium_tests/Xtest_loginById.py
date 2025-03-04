from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import unittest
import time
import sys
from unittest.runner import TextTestResult

class CleanTextTestResult(TextTestResult):
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.pass_count = 0
        self.fail_count = 0

    def addSuccess(self, test):
        super().addSuccess(test)
        self.pass_count += 1
        if self.showAll:
            self.stream.writeln("PASS")
        elif self.dots:
            self.stream.write('.')
            self.stream.flush()

    def addFailure(self, test, err):
        if test not in self.failures:
            super().addFailure(test, err)
            self.fail_count += 1
        if self.showAll:
            self.stream.writeln("FAIL")
        elif self.dots:
            self.stream.write('F')
            self.stream.flush()

    def addError(self, test, err):
        if test not in self.errors:
            super().addError(test, err)
            self.fail_count += 1
        if self.showAll:
            self.stream.writeln("ERROR")
        elif self.dots:
            self.stream.write('E')
            self.stream.flush()

    def printSummary(self):
        total = self.pass_count + self.fail_count
        self.stream.writeln(f"\n測試結果摘要:")
        self.stream.writeln(f"通過測試數: {self.pass_count}")
        self.stream.writeln(f"失敗測試數: {self.fail_count}")
        self.stream.writeln(f"總測試數: {total}")

class CustomTextTestRunner(unittest.TextTestRunner):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, test):
        result = super().run(test)
        if hasattr(result, 'printSummary'):
            result.printSummary()
        return result

class LoginPageTest(unittest.TestCase):
    def setUp(self):
        self.delay_seconds = 2
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get("https://the-internet.herokuapp.com/login")
        self.wait = WebDriverWait(self.driver, 10)
        
    def test_01_successful_login(self):
        username = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
        password = self.driver.find_element(By.ID, "password")
        login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        
        username.send_keys("tomsmith")
        password.send_keys("SuperSecretPassword!")
        login_button.click()
        
        success_message = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//div[contains(@class, 'flash') and contains(@class, 'success')]")
        ))
        self.assertIsNotNone(success_message)

    def test_02_invalid_credentials(self):
        username = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
        password = self.driver.find_element(By.ID, "password")
        login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        
        username.send_keys("wronguser")
        password.send_keys("wrongpassword")
        login_button.click()
        
        error_message = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//div[contains(@class, 'flash') and contains(@class, 'error')]")
        ))
        self.assertIsNotNone(error_message)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(LoginPageTest)
    runner = CustomTextTestRunner(resultclass=CleanTextTestResult, verbosity=2)
    runner.run(suite)
