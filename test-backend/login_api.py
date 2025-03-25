import requests
import json
import os
import sys
from urllib.parse import urljoin
# 添加項目根目錄到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.config import Config , config  # 導入 Config 和 config


file_path = "/Users/steven/deepseek/seleium/config/random_data.json"


class login_api():
    def login():
        url = urljoin(config.BASE_URL,config.LOGIN_API)
        
        headers = {
            "authorization":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJubyI6Ijg3ZTI4ZTYxOTA3MzE0MThmNmZhOWRiMDQ0M2IxMmRjIiwidmUiOiIiLCJsYSI6InpoLWNuIiwidGkiOiIxIiwidWEiOiJmSzNyMUJ2OU1nbjMyTXFUY1Y5cGl5ZE96ekxnSWJUeWNjSVk2UFJrZkt5N3Y0REkrMnN2YVJaR1FWZ2ZZcnJ6eUpBZlVBcGdLVm9GS2NWNHF3dGF6ZVpGdHYvQWh0VERteU1kSk5pblpBbmI0dFpjdTVUdlorQU1KZVZQd2wzSGhSdDBHOC9oWHRnOXNIbU1RSk5DL0tJMnpiMWQyVWltSStZT1JzY2JlT29VWkZRVHREbU9LMmhnNDRqOHhORTUiLCJpYXQiOiIxNzQyODY2OTU0IiwiZG8iOiJ1YXQtbmV3cGxhdGZvcm0ubXhzeWwuY29tIiwicmUiOiIxNzQ1NDg3NzU0IiwibmJmIjoxNzQyODY2OTU0LCJleHAiOjE3NDI4OTU3NTQsImlzcyI6Imh0dHA6Ly8xMjcuMC4wLjE6ODAwMCIsImF1ZCI6Imh0dHA6Ly8xMjcuMC4wLjE6ODAwMCJ9.-7Xge578GvrIODaQ1iNAwgaGDYA-8Mh2e5kqezDDA6A",
            "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0"
            }
        payload = {
            "userName": (config.VALID_DP_USERNAME),
            "password": (config.VALID_PASSWORD_MD5)
            }
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None

    # Example usage
    result = login()
    if result.get("success"):
        new_token = result["data"].get("token", "")

        # 讀取現有 JSON 檔案
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                try:
                    existing_data = json.load(f)
                except json.JSONDecodeError:
                    existing_data = {}  # 若解析錯誤則使用空字典
        else:
            existing_data = {}  # 若檔案不存在則初始化

        # 更新 token 值（不影響其他欄位）
        existing_data["token"] = new_token

        # 將更新後的資料寫回 JSON
        with open(file_path, "w") as f:
            json.dump(existing_data, f, indent=4)

        print("✅ Login successful!")
        print(f"🔹 Token updated in: {file_path}")
    else:
        print("❌ Login failed!")