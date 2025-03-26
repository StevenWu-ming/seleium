# selenium_helpers.py
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

def close_popup(driver, wait):
    """重複嘗試關閉彈出窗口，直到找不到或超時"""
    while True:
        try:
            close_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//i[contains(@class, 'close-btn')]")))
            if close_button:
                driver.execute_script("arguments[0].click();", close_button)
            else:
                break
        except (TimeoutException, StaleElementReferenceException):
            break

def click_element(driver, wait, xpath):
    """等待元素可點擊後點擊"""
    element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    element.click()

def input_text(driver, wait, xpath, text):
    """等待元素存在後，清除並輸入文字"""
    element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    element.clear()
    element.send_keys(text)

def wait_for_success_message(wait, success_text="我的钱包"):
    """等待頁面中出現成功訊息，返回該元素文字"""
    element = wait.until(EC.presence_of_element_located((By.XPATH, f"//span[contains(text(), '{success_text}')]")))
    return element.text

def wait_for_err_message(wait, success_text="我的钱包"):
    """等待頁面中出現成功訊息，返回該元素文字"""
    element = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[contains(text(), '{success_text}')]")))
    return element.text


def perform_login(driver, wait, username, password,
                  username_xpath="//input[@maxlength='18']",
                  password_xpath="//input[@type='password']",
                  login_button_xpath="//button[contains(text(), '登录')]"):
    """封裝通用的登入流程"""
    input_text(driver, wait, username_xpath, username)
    input_text(driver, wait, password_xpath, password)
    click_element(driver, wait, login_button_xpath)
