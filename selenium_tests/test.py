from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import unittest
import time

class LoginPageTest(unittest.TestCase):
    def setUp(self):
        self.delay_seconds = 2
        chrome_options = Options()
        chrome_options.add_argument("--log-level=3")
        chrome_options.set_capability("goog:loggingPrefs", {"browser": "OFF"})
        # chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get("https://uat-newplatform.mxsyl.com/zh-cn/login")
        self.wait = WebDriverWait(self.driver, 5)  # 增加等待時間至 15 秒

    def test_05_mail_login(self):
        try:
            # 定位並點擊「郵箱」標籤
            phone_tab = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'tab') and contains(text(), ' 邮箱 ')]")))
            phone_tab.click()

            # 輸入郵箱和密碼
            email = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='text']")))
            password = self.driver.find_element(By.XPATH, "//input[@type='password']")
            login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), '登录')]")
            email.send_keys("hrtqdwmk@sharklasers.com")
            password.send_keys("1234Qwer")
            login_button.click()

            # 等待登入成功的標誌（優化後的 XPath）
            success_message = self.wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), '我的钱包')]")))
            self.assertIn("我的钱包", success_message.text)
            print("Test Case 2 - 郵箱登入成功: PASSED ")
            self.assertIsNotNone(success_message)

        except Exception as e:
            print(f"Test Case 2 - 郵箱登入失敗: FAILED - {str(e)}")
            self.fail()

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main(verbosity=2)