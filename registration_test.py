import requests
import time

# API 端点
url = "https://uat-newplatform.mxsyl.com/v1/member/auth/registerbyuserpwd"

# Headers
headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "apm-request-id": "65b5b124f09eb8bd",
    "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJubyI6Ijk3ZDZjYTlkOGMxMTEzNGU0MzBkNWI4MjY0ZmFlNWE2IiwidmUiOiIiLCJsYSI6InpoLWNuIiwidGkiOiIxIiwidWEiOiIycUFPYVFNUjVnSDVYSXdrQmZJa1orUkg4V21kWmJ3Ym5BSzBmS21LYWM2TGhPN24xZW9FazJwSWZPUDZ1QTk4TGFiL1NsWXpTRXRuaDZLejZTMlkzOStqYlhyendlM0pWNFZ0ZndFVjdHUDM4WlBuWVNLdVlIaTJxNVplME5yQkR4UFhZeXZROU1qRWx6QlNJdWhYcWc9PSIsImlhdCI6IjE3NDEwNzM2NDYiLCJkbyI6InVhdC1uZXdwbGF0Zm9ybS5teHN5bC5jb20iLCJyZSI6IjE3NDM2OTQ0NDYiLCJuYmYiOjE3NDEwNzM2NDYsImV4cCI6MTc0MTEwMjQ0NiwiaXNzIjoiaHR0cDovLzEyNy4wLjAuMTo4MDAwIiwiYXVkIjoiaHR0cDovLzEyNy4wLjAuMTo4MDAwIn0.nLzv_i-VPQaOe44lUhch4RRajN5B918Uu-1gsi2nsz4",
    "content-type": "application/json;charset=UTF-8",
    "lang": "zh-cn",
    "origin": "https://uat-newplatform.mxsyl.com",
    "referer": "https://uat-newplatform.mxsyl.com/zh-cn/register",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
}

# Cookies
cookies = {
    "_ga": "GA1.1.806440740.1740449444",
    "_vid_t": "M3xBF/0kYTxoSIFUnB2btxMreX8d6tto1N+EJ/jOh/J+Bm8RD7Ba1yc3HcQ+oQPaEaS/1jSyC7Pe8Q==",
    "JSESSIONID": "39C80BFC6B5FCDC37ED7AE1ED3324599"
}

# 获取用户输入
prefix = input("請輸入帳號前綴（例如 cooper）：")
count = int(input("請輸入次數（例如 100）："))

# 生成帳號列表，例如 cooper001 到 cooper100
accounts = [{"userName": f"{prefix}{i:03d}", "password": "1234Qwer"} for i in range(1, count + 1)]

# 假设的加密后密码（如果需要动态加密，这里要替换成加密函数）
encrypted_password = "SsazwZkvhNbFZxjJkdzrvbASCazrs3cdX+r0yM7gSL1uHrClJYX4hpSDjZkeAEZ91Ji3j5aUcRGthBEm9mx00BOdrNHL7qBEbQlSI1wvW8G32OtLQPnFE/kUDMnHgQ12i1d20/fdRBxyuzr8T5EhyyTBPbvdvNOJq44qTaWtOgFUzIcCSnlbVxluzJ8159nob8/k12SytslbGreQkgrwj8D2Sm6zEABEELkHSiQX8L1nb3wV8Te4cCXataMiAF//rOrK/sBvg00E/x9VGgUGFb0/mVvtLp8lJvnkqbguNFLZQVcu2txjgM7Tv/uQUWgmBCt1YwEw9zhVDGTsZzllvQ=="

# 循环创建账户
for account in accounts:
    payload = {
        "userName": account["userName"],
        "password": encrypted_password,  # 使用你提供的加密密码
        "lotNumber": "8ddccca26e2a46eca274f2fca8fdb4a7",
        "captchaOutput": "Mx262209Ac0tOd6HiWXwDGZd_w036Cr-0l62HPaKbIJxHi_DsG9Qe7j6nznbNq38ekxwvv9GocjNGgUhziq5Ezec1YlBrOrO_dRwa4jjv6EANU8_m9kzOGvkI62n0Ef4aFC3kHu8v5h9WdJxoJYxckorwquztuizs5lkIqb5lvTCp5HLIX6u0uKMbzPCgLpwkXrFwNEvJWBDNsQRg0cdnlsMDp9mqrJZdpjf4krKwUGG6DpL-hL3uhldCOHivalVkKSYBXYPHNRFYtoG1u02lNlqn70lz9fvJOwvHQkdrxEtCxi3L3Kd2wq9ROtef0ZebVb8-ZXfiitvkj762R8njyC85dC5MWbNlnqSZe6uBMsDei1Vr_uCmRL0BbgL1pwesRK9xKey1lae50BFoxdELGujp8cM1egdUJ6eexNoZ2nK8MWDVKR7AhyVtiXY8pv1EbVbOAI-nYBvPNsK1iwscg==",
        "passToken": "65a9d25182ba01f351644510a92bff3add6e9dd54ead5e3419db2799b4485720",
        "genTime": str(int(time.time()))  # 当前时间戳
    }

    # 发送请求
    response = requests.post(url, json=payload, headers=headers, cookies=cookies)

    # 检查响应
    if response.status_code in [200, 201]:
        print(f"帳號 {account['userName']} 創建成功: {response.text}")
    else:
        print(f"帳號 {account['userName']} 創建失敗: {response.status_code} - {response.text}")

    # 避免触发速率限制
    time.sleep(1)