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
    # api_url = "https://uat-newplatform.mxsyl.com/v1/member/auth/registerbyuserpwd"
    api_url = "https://uat8-newplatform.mxsyl.com/v1/member/auth/registerbyemail"

    
    # 獲取動態 headers 和 cookies
    headers = {
        'authorization': f"Bearer {token}",
         "user-agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
                )
        }

    cookies = {}

    # 獲取用戶輸入
    prefix = input("請輸入帳號前綴（例如 cooper）：")
    count = int(input("請輸入次數（例如 100）："))

    # 生成帳號列表
    accounts = [{"userName": f"{prefix}{i:03d}@cooper.com", "password": "1234Qwer"} for i in range(1, count + 1)]

    # 加密後的密碼（假設這是你從某處獲取的固定值）
    encrypted_password = "SsazwZkvhNbFZxjJkdzrvbASCazrs3cdX+r0yM7gSL1uHrClJYX4hpSDjZkeAEZ91Ji3j5aUcRGthBEm9mx00BOdrNHL7qBEbQlSI1wvW8G32OtLQPnFE/kUDMnHgQ12i1d20/fdRBxyuzr8T5EhyyTBPbvdvNOJq44qTaWtOgFUzIcCSnlbVxluzJ8159nob8/k12SytslbGreQkgrwj8D2Sm6zEABEELkHSiQX8L1nb3wV8Te4cCXataMiAF//rOrK/sBvg00E/x9VGgUGFb0/mVvtLp8lJvnkqbguNFLZQVcu2txjgM7Tv/uQUWgmBCt1YwEw9zhVDGTsZzllvQ=="

    # 循環創建帳戶
    for account in accounts:
        payload = {
            "email": account["userName"],
            "password": encrypted_password,
            "otpCode":"123456"
        }

        # 發送 POST 請求，使用動態抓取的 headers 和 cookies
        response = requests.post(api_url, json=payload, headers=headers, cookies=cookies)
        # print (token)
        # 檢查響應
        if response.status_code in [200, 201]:
            print(f"帳號 {account['userName']} 創建成功: {response.text}")
        else:
            print(f"帳號 {account['userName']} 創建失敗: {response.status_code} - {response.text}")

        # 避免觸發速率限制
        time.sleep(1)

if __name__ == "__main__":
    register_accounts()




'''    線上人數有一個後端bug  一個玩家進入遊戲會計算到兩個人數
重複進入不會重複計算<這點沒錯
以下還沒測試
進入後開始計算120分鐘 超過120分鐘人數會-1
過60分鐘後再重新進去一變會重新開始計算120分鐘 總共180分鐘才會-1'''
