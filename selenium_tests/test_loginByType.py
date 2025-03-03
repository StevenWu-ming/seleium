from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import unittest
import time
import sys
import random
import string
from unittest.runner import TextTestResult

class CleanTextTestResult(TextTestResult):
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.pass_count = 0
        self.fail_count = 0

    def addSuccess(self, test):
        super().addSuccess(test)
        self.pass_count += 1
        # 移除 "PASS" 輸出，僅保留您自定義的 print 訊息
        if self.showAll:
            self.stream.write('')  # 空輸出，避免多餘的行
        elif self.dots:
            self.stream.write('')  # 移除點號
            self.stream.flush()

    def addFailure(self, test, err):
        if test not in self.failures:
            super().addFailure(test, err)
            self.fail_count += 1
        if self.showAll:
            self.stream.write('')  # 移除 "FAIL" 輸出
        elif self.dots:
            self.stream.write('')  # 移除 'F'
            self.stream.flush()

    def addError(self, test, err):
        if test not in self.errors:
            super().addError(test, err)
            self.fail_count += 1
        if self.showAll:
            self.stream.write('')  # 移除 "ERROR" 輸出
        elif self.dots:
            self.stream.write('')  # 移除 'E'
            self.stream.flush()

    def printErrors(self):
        # 覆蓋 printErrors 方法，移除默認的 "ok" 和測試名稱輸出
        pass

    def printSummary(self):
        total = self.pass_count + self.fail_count
        self.stream.writeln(f"\n測試結果摘要:")
        self.stream.writeln(f"通過測試數: {self.pass_count}")
        self.stream.writeln(f"失敗測試數: {self.fail_count}")
        self.stream.writeln(f"總測試數: {total}")

class CustomTextTestRunner(unittest.TextTestRunner):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.verbosity = 0  # 設置 verbosity 為 0，防止輸出測試名稱和 "ok"

    def run(self, test):
        result = super().run(test)
        if hasattr(result, 'printSummary'):
            result.printSummary()
        return result

class LoginPageTest(unittest.TestCase):
    def setUp(self):
        self.delay_seconds = 2
        chrome_options = Options()
        chrome_options.add_argument("--log-level=3")
        chrome_options.set_capability("goog:loggingPrefs", {"browser": "OFF"})
        #chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get("https://uat-newplatform.mxsyl.com/zh-cn/login")
        self.wait = WebDriverWait(self.driver, 10)
    
    def generate_random_username(self, length=8):
        # 定義可能的字元集（字母和數字，適合用於帳號）
        letters_and_digits = string.ascii_lowercase + string.digits  # 小寫字母和數字
        # 確保帳號只包含小寫字母和數字（根據網站需求調整）
        random_username = ''.join(random.choice(letters_and_digits) for _ in range(length))
        return random_username
    

    def test_01_check_login_button_enabled_after_username_and_password(self):
        try:
            # 等待用戶名輸入欄位、密碼輸入欄位和登入按鈕加載
            username_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@maxlength='18']")))
            password_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']")))
            login_button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), '登录')]")))

            # 初始檢查：按鈕是否為 disabled（未輸入任何內容時）
            initial_disabled = "disabled" in login_button.get_attribute("class")
            print(f"未輸入任何資料 {'disabled' if initial_disabled else 'enabled'}")

            # 輸入用戶名
            username = "cooper001"
            username_input.send_keys(username)
            time.sleep(1)  # 等待頁面更新（根據需要調整）

            # 中間檢查：輸入用戶名後，按鈕是否仍為 disabled（密碼未輸入）
            mid_login_button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), '登录')]")))
            mid_disabled = "disabled" in mid_login_button.get_attribute("class")
            print(f"僅輸入帳號: {'disabled' if mid_disabled else 'enabled'}")

            # 輸入密碼
            password = "1234Qwer"
            password_input.send_keys(password)
            time.sleep(1)  # 等待頁面更新（根據需要調整）

            # 最終檢查：輸入用戶名和密碼後，按鈕是否變為 enabled（移除 disabled）
            final_login_button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), '登录')]")))
            final_disabled = "disabled" in final_login_button.get_attribute("class")
            print(f"全部輸入: {'disabled' if final_disabled else 'enabled'}")

            # 斷言：確認輸入用戶名和密碼後按鈕應為 enabled（不包含 disabled 類名）
            self.assertFalse(final_disabled, "Login button should be enabled after username and password input")

            print(f"Test Case 1 - 登入按鈕檢查: PASSED")
        except Exception as e:
            print(f"Test Case 1 - 登入按鈕檢查: FAILED - {str(e)}")
            self.fail()

    def test_02_successful_login(self):
        try:   
            username = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@maxlength='18']")))
            password = self.driver.find_element(By.XPATH, "//input[@type='password']")
            login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), '登录')]")
            username.send_keys("cooper001")
            password.send_keys("1234Qwer")
            login_button.click()
            

            success_message = self.wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), '充值')]")))
            self.assertIn("充值", success_message.text)
            print("Test Case 2 - 帳號密碼正確: PASSED")
            #self.assertIsNotNone(success_message)
        except Exception as e:
            print(f"Test Case 2 - 帳號密碼正確: FAILED - {str(e)}")
            self.fail()

    def test_04_invalid_credentials(self):
        try:    
            username = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@maxlength='18']")))
            password = self.driver.find_element(By.XPATH, "//input[@type='password']")
            login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), '登录')]")
            random_username = self.generate_random_username(length=8)  # 您可以調整帳號長度
            username.send_keys(random_username)
            password.send_keys("1234Qwer")
            login_button.click()
            
            error_message = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[contains(text(), '您输入的密码不正确')]")
            ))
            self.assertIn("您输入的密码不正确", error_message.text)
            print("Test Case 3 - 帳號密碼錯誤: PASSED")
            #self.assertIsNotNone(error_message)
        except Exception as e:
            print(f"Test Case 3 - 帳號密碼錯誤: FAILED - {str(e)}")
            self.fail()

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(LoginPageTest)
    runner = CustomTextTestRunner(resultclass=CleanTextTestResult, verbosity=0)  # 將 verbosity 設置為 0
    runner.run(suite)