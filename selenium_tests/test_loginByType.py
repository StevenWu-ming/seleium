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
        # chrome_options.add_argument("--headless")  # 註解掉以便觀察
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get("https://the-internet.herokuapp.com/login")
        self.wait = WebDriverWait(self.driver, 10)

    def test_successful_login(self):
        try:
            username = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='text']")))
            time.sleep(self.delay_seconds)
            password = self.driver.find_element(By.XPATH, "//input[@type='password']")
            time.sleep(self.delay_seconds)
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")

            username.send_keys("tomsmith")
            time.sleep(self.delay_seconds)
            password.send_keys("SuperSecretPassword!")
            time.sleep(self.delay_seconds)
            login_button.click()

            success_message = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'flash') and contains(@class, 'success')]")))
            self.assertIn("you logged into a secure area", success_message.text.lower())
            print("Test Case 1 - Successful Login: PASSED")
        except Exception as e:
            print(f"Test Case 1 - Successful Login: FAILED - {str(e)}")
            self.fail()

    def test_invalid_credentials(self):
        try:
            username = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='text']")))
            time.sleep(self.delay_seconds)
            password = self.driver.find_element(By.XPATH, "//input[@type='password']")
            time.sleep(self.delay_seconds)
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")

            username.send_keys("wronguser")
            time.sleep(self.delay_seconds)
            password.send_keys("wrongpassword")
            time.sleep(self.delay_seconds)
            login_button.click()

            error_message = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'flash') and contains(@class, 'error')]")))
            self.assertIn("your username is invalid", error_message.text.lower())
            print("Test Case 2 - Invalid Credentials: PASSED")
        except Exception as e:
            print(f"Test Case 2 - Invalid Credentials: FAILED - {str(e)}")
            self.fail()

    def tearDown(self):
        time.sleep(self.delay_seconds)
        self.driver.quit()

if __name__ == "__main__":
    unittest.main(verbosity=2)
    