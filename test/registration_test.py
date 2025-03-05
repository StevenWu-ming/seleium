import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from pprint import pprint
import json

# 動態抓取 headers 和 cookies 的函數（來自之前的修復版本）
def fetch_selenium_headers_and_cookies(url):
    options = Options()
    options.headless = True  # 無頭模式
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})  # 啟用性能日誌

    service = Service("/Users/steven/deepseek/chromedriver")  # 替換為你的 chromedriver 路徑
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
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
                    break

        # 獲取 cookies
        cookies = driver.get_cookies()
        cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}

        # 打印 headers 和 cookies
        print("Fetched Headers:")
        pprint(headers)
        print("\nFetched Cookies:")
        pprint(cookies_dict)
        
        return headers, cookies_dict
    
    finally:
        driver.quit()

# 修改後的註冊帳號函數
def register_accounts():
    # API 端點
    api_url = "https://uat-newplatform.mxsyl.com/v1/member/auth/registerbyuserpwd"
    
    # 獲取動態 headers 和 cookies
    target_url = "https://uat-newplatform.mxsyl.com/"
    headers, cookies = fetch_selenium_headers_and_cookies(target_url)

    # 獲取用戶輸入
    prefix = input("請輸入帳號前綴（例如 cooper）：")
    count = int(input("請輸入次數（例如 100）："))

    # 生成帳號列表
    accounts = [{"userName": f"{prefix}{i:03d}", "password": "1234Qwer"} for i in range(1, count + 1)]

    # 加密後的密碼（假設這是你從某處獲取的固定值）
    encrypted_password = "SsazwZkvhNbFZxjJkdzrvbASCazrs3cdX+r0yM7gSL1uHrClJYX4hpSDjZkeAEZ91Ji3j5aUcRGthBEm9mx00BOdrNHL7qBEbQlSI1wvW8G32OtLQPnFE/kUDMnHgQ12i1d20/fdRBxyuzr8T5EhyyTBPbvdvNOJq44qTaWtOgFUzIcCSnlbVxluzJ8159nob8/k12SytslbGreQkgrwj8D2Sm6zEABEELkHSiQX8L1nb3wV8Te4cCXataMiAF//rOrK/sBvg00E/x9VGgUGFb0/mVvtLp8lJvnkqbguNFLZQVcu2txjgM7Tv/uQUWgmBCt1YwEw9zhVDGTsZzllvQ=="

    # 循環創建帳戶
    for account in accounts:
        payload = {
            "userName": account["userName"],
            "password": encrypted_password,
            "lotNumber": "8ddccca26e2a46eca274f2fca8fdb4a7",
            "captchaOutput": "Mx262209Ac0tOd6HiWXwDGZd_w036Cr-0l62HPaKbIJxHi_DsG9Qe7j6nznbNq38ekxwvv9GocjNGgUhziq5Ezec1YlBrOrO_dRwa4jjv6EANU8_m9kzOGvkI62n0Ef4aFC3kHu8v5h9WdJxoJYxckorwquztuizs5lkIqb5lvTCp5HLIX6u0uKMbzPCgLpwkXrFwNEvJWBDNsQRg0cdnlsMDp9mqrJZdpjf4krKwUGG6DpL-hL3uhldCOHivalVkKSYBXYPHNRFYtoG1u02lNlqn70lz9fvJOwvHQkdrxEtCxi3L3Kd2wq9ROtef0ZebVb8-ZXfiitvkj762R8njyC85dC5MWbNlnqSZe6uBMsDei1Vr_uCmRL0BbgL1pwesRK9xKey1lae50BFoxdELGujp8cM1egdUJ6eexNoZ2nK8MWDVKR7AhyVtiXY8pv1EbVbOAI-nYBvPNsK1iwscg==",
            "passToken": "65a9d25182ba01f351644510a92bff3add6e9dd54ead5e3419db2799b4485720",
            "genTime": str(int(time.time()))
        }

        # 發送 POST 請求，使用動態抓取的 headers 和 cookies
        response = requests.post(api_url, json=payload, headers=headers, cookies=cookies)

        # 檢查響應
        if response.status_code in [200, 201]:
            print(f"帳號 {account['userName']} 創建成功: {response.text}")
        else:
            print(f"帳號 {account['userName']} 創建失敗: {response.status_code} - {response.text}")

        # 避免觸發速率限制
        time.sleep(1)

if __name__ == "__main__":
    register_accounts()