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

    def test_04_phonenumber_login(self):
        try:
            # 打印頁面標題以確認加載
            print(f"Page title: {self.driver.title}")

            # 定位並點擊「手机」標籤
            phone_tab = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'tab') and contains(text(), '手机')]")))
            print("Found phone tab, clicking...")
            phone_tab.click()

            # 定位並點擊手機號碼下拉選單
            phone_dropdown = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'phone-box')]//button[contains(@class, 'select-btn')]")))
            print("Found phone dropdown, clicking...")
            phone_dropdown.click()

            # 等待並選擇「+86」相關的選項
            search_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='搜索' or contains(@class, 'search')]")))
            search_input.send_keys("+86")
            china_option = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '+86')] | //li[contains(text(), '+86')]")))
            print("Found '+86' option, clicking...")
            china_option.click()

            # 輸入手機號和密碼
            phonenumber = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='number']")))
            password = self.driver.find_element(By.XPATH, "//input[@type='password']")
            login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), '登录')]")
            phonenumber.send_keys("13100000001")
            password.send_keys("1234Qwer")
            login_button.click()

            # 檢查是否直接登入成功（跳過驗證碼）
            try:
                '''# 嘗試關閉所有可能的 Pop-up
                popup_closed = False
                while not popup_closed:
                    try:
                        popup_close_buttons = self.wait.until(
                            EC.presence_of_all_elements_located((By.XPATH, "//i[contains(@class, 'close-btn') and contains(@class, 'icon-close-simple')]"))
                        )
                        if popup_close_buttons:
                            for button in popup_close_buttons:
                                print("Found pop-up close button, clicking...")
                                button.click()
                                time.sleep(1)  # 等待 Pop-up 關閉
                        else:
                            popup_closed = True
                    except Exception as popup_error:
                        print(f"No more pop-ups found or failed to close: {str(popup_error)}")
                        popup_closed = True'''

                # 嘗試等待登入成功的標誌（優化後的 XPath）
                success_message = self.wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), '我的钱包')]")))
                self.assertIn("我的钱包", success_message.text)
                print("Test Case 2 - 手機號碼登入成功: PASSED (直接登入成功)")
                self.assertIsNotNone(success_message)
                return  # 直接退出函數，跳過驗證碼流程

            except Exception as direct_login_error:
                print(f"直接登入失敗，可能需要驗證碼: {str(direct_login_error)}")


            # 定位並點擊「獲取驗證碼」按鈕
            get_code_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'input-group-txt') and contains(@class, 'get-code')]")))
            get_code_button.click()

            # 等待成功提示框出現（例如包含「成功」的提示）
            success_toast = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'toast-text')]//p[contains(text(), '成功')]")))

            # 等待驗證碼輸入框出現
            verify_code_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'input-group')]//input[@type='number' and @maxlength='6']")))
            verify_code_input.send_keys("123456")

            '''popup_closed = False
            while not popup_closed:
                    try:
                        popup_close_buttons = self.wait.until(
                            EC.presence_of_all_elements_located((By.XPATH, "//i[contains(@class, 'close-btn') and contains(@class, 'icon-close-simple')]"))
                        )
                        if popup_close_buttons:
                            for button in popup_close_buttons:
                                print("Found pop-up close button, clicking...")
                                button.click()
                                time.sleep(1)  # 等待 Pop-up 關閉
                        else:
                            popup_closed = True
                    except Exception as popup_error:
                        print(f"No more pop-ups found or failed to close: {str(popup_error)}")
                        popup_closed = True'''


            # 等待登入成功的標誌（優化後的 XPath）
            success_message = self.wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), '我的钱包')]")))
            self.assertIn("我的钱包", success_message.text)
            print("Test Case 2 - 手機號碼登入成功: PASSED (經由驗證碼登入成功)")
            self.assertIsNotNone(success_message)

        except Exception as e:
            print(f"Test Case 2 - 手機號碼登入失敗: FAILED - {str(e)}")
            self.fail()

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main(verbosity=2)