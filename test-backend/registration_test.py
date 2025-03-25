import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from pprint import pprint
import json



# 修改後的註冊帳號函數
def register_accounts():
    # API 端點
    api_url = "https://uat-newplatform.mxsyl.com/v1/member/auth/registerbyuserpwd"
    
    # 獲取動態 headers 和 cookies
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-TW,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'apm-request-id': '968b34647625c745',
        'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJubyI6ImExMjNmNzI1YzVkZTlmMjZjZTQzNmU4NzI2NjljYWUwIiwidmUiOiIiLCJsYSI6ImVuLXVzIiwidGkiOiIxIiwidWEiOiJmSzNyMUJ2OU1nbjMyTXFUY1Y5cGl5ZE96ekxnSWJUeWNjSVk2UFJrZkt5N3Y0REkrMnN2YVJaR1FWZ2ZZcnJ6eUpBZlVBcGdLVm9GS2NWNHF3dGF6ZVpGdHYvQWh0VERteU1kSk5pblpBbmI0dFpjdTVUdlorQU1KZVZQd2wzSGhSdDBHOC9oWHRnOXNIbU1RSk5DL0tJMnpiMWQyVWltSStZT1JzY2JlT29VWkZRVHREbU9LMmhnNDRqOHhORTUiLCJpYXQiOiIxNzQxNTc2MTM3IiwiZG8iOiJ1YXQtbmV3cGxhdGZvcm0ubXhzeWwuY29tIiwicmUiOiIxNzQ0MTk2OTM3IiwibmJmIjoxNzQxNTc2MTM3LCJleHAiOjE3NDE2MDQ5MzcsImlzcyI6Imh0dHA6Ly8xMjcuMC4wLjE6ODAwMCIsImF1ZCI6Imh0dHA6Ly8xMjcuMC4wLjE6ODAwMCJ9.NMeHZqtg5Smya42pCRK5q6PPkheAo6ttnlzUpNv6KII',
        'cache-control': 'no-store,no-cache',
        'content-type': 'application/json;charset=utf-8',
        'fp-visitor-id': 'nd8ffe2F0m1obxmzSvhh',
        'lang': 'en-us',
        'ngsw-bypass': 'true',
        'priority': 'u=1, i',
        'referer': 'https://uat-newplatform.mxsyl.com/en-us/casino/category/1152546797191237',
        'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Microsoft Edge";v="134"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0'
    }

    cookies = {
        '_ga': 'GA1.1.770330830.1741144518',
        '_hjSessionUser_3823075': 'eyJpZCI6ImM2ZDg0NTMyLWMwYjYtNTBlZi05ODg2LTg2NzIzMzQzYWMyZiIsImNyZWF0ZWQiOjE3NDExNDQ4Mjk5MDQsImV4aXN0aW5nIjp0cnVlfQ==',
        '_vid_t': 'b3y+hLkZPHNIXlsrAvj26nWMlsiy4cddQ2+rDQqqQcWJDUwrbJ6FBWXCCZK1tWpQDWny8JaZYFGylw==',
        '_hjSession_3823075': 'eyJpZCI6IjM0M2EzOTJlLTAxZDItNGE1My05ZTE0LWQwMTRiMmQ5ZDAxMyIsImMiOjE3NDE1NzQ4MzgzMzQsInMiOjEsInIiOjEsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=',
        '_hjHasCachedUserAttributes': 'true',
        'JSESSIONID': '474CE228F3161CC85939C4A39CBD6C94',
        '_hjUserAttributesHash': '1137861a9474880520c99bfc70722e34',
        '_ga_DP31FC7D8Z': 'GS1.1.1741574838.8.1.1741576165.0.0.0',
        '_ga_2RY83PV4BH': 'GS1.1.1741574838.8.1.1741576165.0.0.1213001250'
    }

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