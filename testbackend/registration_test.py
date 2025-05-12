# 透過 API 批量註冊帳號，使用動態 token 和加密密碼，支援用戶輸入前綴和數量
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from pprint import pprint
import json

file_path = "/Users/steven/deepseek/seleium/config/random_data.json"
# 讀取原始 token（可選：在發送請求前讀取當前 token）
token = None
try:
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    token = data.get("before_token")
    if not token:
        raise ValueError("JSON 檔案中缺少 'token' 字段")
except FileNotFoundError:
    print(f"錯誤：找不到檔案 {file_path}")
except json.JSONDecodeError:
    print("錯誤：JSON 檔案格式無效")
except Exception as e:
    print(f"發生錯誤：{str(e)}")


# 修改後的註冊帳號函數
def register_accounts():
    # API 端點
    api_url = "https://uat-newplatform.mxsyl.com/v1/member/auth/registerbyuserpwd"
    
    # 獲取動態 headers 和 cookies
    headers = {
        'authorization': f"Bearer {token}",
         "user-agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
                )
        }

    cookies = {}

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
        print (token)
        # 檢查響應
        if response.status_code in [200, 201]:
            print(f"帳號 {account['userName']} 創建成功: {response.text}")
        else:
            print(f"帳號 {account['userName']} 創建失敗: {response.status_code} - {response.text}")


        # 避免觸發速率限制
        time.sleep(1)

if __name__ == "__main__":
    register_accounts()