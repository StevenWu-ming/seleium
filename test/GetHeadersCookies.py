from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from pprint import pprint
import json
import os

def fetch_selenium_headers_and_cookies(url):
    # 設置 Chrome 選項
    options = Options()
    options.headless = True  # 無頭模式
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})  # 啟用性能日誌

    # 指定 Chrome 驅動路徑
    driver = webdriver.Chrome(options=options)    
    
    try:
        # 開啟網頁
        driver.get(url)
        driver.implicitly_wait(10)

        # 獲取網絡請求的性能日誌
        logs = driver.get_log("performance")
        headers = {}
        
        # 解析日誌以提取 headers
        for entry in logs:
            message = json.loads(entry['message'])['message']
            if message['method'] == 'Network.requestWillBeSent':
                request = message['params']['request']
                if request['url'] == url:  # 只提取目標 URL 的請求
                    headers = request['headers']
                    break  # 找到後退出循環

        # 獲取 cookies
        cookies = driver.get_cookies()
        cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}

        # 打印 headers 和 cookies
        print("Headers:")
        pprint(headers)
        print("\nCookies:")
        pprint(cookies_dict)
        
        return headers, cookies_dict
    
    finally:
        driver.quit()

# 示例用法
if __name__ == "__main__":
    target_url = "https://uat-newplatform.mxsyl.com/"
    headers, cookies = fetch_selenium_headers_and_cookies(target_url)

    # 獲取當前腳本所在目錄
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # 確保 test 資料夾存在
    test_dir = os.path.join(script_dir, "test")
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)

    # 儲存 headers 和 cookies 至 test 資料夾
    if headers and cookies:
        with open(os.path.join(test_dir, "headers.txt"), "w", encoding="utf-8") as f:
            json.dump(headers, f, ensure_ascii=False, indent=4)  # 使用 JSON 格式儲存
        with open(os.path.join(test_dir, "cookies.txt"), "w", encoding="utf-8") as f:
            json.dump(cookies, f, ensure_ascii=False, indent=4)  # 使用 JSON 格式儲存