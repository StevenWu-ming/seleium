# selenium_helpers.py
import os # 導入 os 模組（此處未直接使用，可能為未來擴展保留）
import time # 導入 time 模組（此處未直接使用，可能為未來擴展保留）
from selenium.webdriver.common.by import By # 導入 By，用於指定定位元素的方式（如 XPath）
from selenium.webdriver.support import expected_conditions as EC # 導入 expected_conditions，用於顯式等待條件
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException # 導入 Selenium 的異常類
from selenium.webdriver.support.ui import WebDriverWait

def close_popup(driver, wait):
    """重複嘗試關閉彈出窗口，直到找不到或超時"""
    while True:
        try: # 等待具有 'close-btn' 類的關閉按鈕可點擊
            close_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//i[contains(@class, 'close-btn')]")))
            if close_button:
                driver.execute_script("arguments[0].click();", close_button) # 使用 JavaScript 點擊關閉按鈕，確保點擊穩定性
            else:
                break # 如果找不到按鈕，退出循環
        except (TimeoutException, StaleElementReferenceException): # 若超時或元素失效（例如網頁重載），退出循環
            break

def click_element(driver, wait, xpath):
    """等待元素可點擊後點擊"""
    element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath))) # 等待指定 XPath 的元素可點擊
    element.click()  # 執行點擊操作

def input_text(driver, wait, xpath, text):
    """等待元素存在後，清除並輸入文字"""
    element = wait.until(EC.presence_of_element_located((By.XPATH, xpath))) # 等待指定 XPath 的元素存在
    element.clear() # 清除輸入框現有內容
    element.send_keys(text) # 輸入指定文字

def wait_for_success_message(wait, success_text="我的钱包"):
    """等待頁面中出現成功訊息，返回該元素文字"""
    element = wait.until(EC.presence_of_element_located((By.XPATH, f"//span[contains(text(), '{success_text}')]"))) # 等待包含指定文字的 <span> 元素出現
    return element.text # 返回元素的文字內容


def wait_for_success_message1(wait, success_text="我的钱包", timeout=3):
    try:
        element = WebDriverWait(wait._driver, timeout).until(
            EC.visibility_of_element_located((By.XPATH, f"//span[contains(text(), '{success_text}')]"))
        )
        return element.text.strip()
    except TimeoutException:
        print(f"⚠️ 未在 {timeout} 秒內等到訊息: {success_text}")
        return None

def wait_for_err_message(wait, success_text="我的钱包"): 
    """等待頁面中出現指定的錯誤訊息，並返回該元素的文字"""
    element = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[contains(text(), '{success_text}')]"))) # 等待包含指定文字的 <div> 元素出現
    return element.text # 返回元素的文字內容


def perform_login(driver, wait, username, password,
                  username_xpath="//input[@maxlength='18']",
                  password_xpath="//input[@type='password']",
                  login_button_xpath="//button[contains(text(), '登录')]"):
    """封裝通用的登入流程"""
    input_text(driver, wait, username_xpath, username) # 輸入用戶名
    input_text(driver, wait, password_xpath, password) # 輸入密碼
    click_element(driver, wait, login_button_xpath) # 點擊登入按鈕
