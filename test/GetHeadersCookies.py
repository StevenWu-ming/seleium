from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from pprint import pprint
import json

def fetch_selenium_headers_and_cookies(url):
    # 設置 Chrome 選項
    options = Options()
    options.headless = True  # 無頭模式
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})  # 啟用性能日誌

    # 指定 Chrome 驅動路徑
    service = Service("/Users/steven/deepseek/chromedriver")  # 替換為你的 chromedriver 路徑
    driver = webdriver.Chrome(service=service, options=options)
    
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

    # 儲存 headers 和 cookies 至檔案
    if headers and cookies:
        with open("headers.txt", "w", encoding="utf-8") as f:
            f.write(str(headers))
        with open("cookies.txt", "w", encoding="utf-8") as f:
            f.write(str(cookies))