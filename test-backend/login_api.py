import requests
import json
import os
import sys
from urllib.parse import urljoin
# 添加項目根目錄到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.config import Config , config  # 導入 Config 和 config


file_path = "/Users/steven/deepseek/seleium/config/random_data.json"
# 定義 token 為全局變數
token = None
# 讀取 token
try:
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        
    # 提取 token 值
    token = data.get("token")
    if not token:
        raise ValueError("JSON 檔案中缺少 'token' 字段")
    
    # print("authorization:", authorization)  # 確認 token 是否正確提取
except FileNotFoundError:
    print(f"錯誤：找不到檔案 {file_path}")
except json.JSONDecodeError:
    print("錯誤：JSON 檔案格式無效")
except Exception as e:
    print(f"發生錯誤：{str(e)}")

class login_api():
    def login():
        url = urljoin(config.BASE_URL,config.LOGIN_API)
        
        headers = {
            "authorization":f"Bearer {token}",
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
    if result is not None and result.get("success"):
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
        if result:
            print(f"Error details: {result}")
        else:
            print("No valid response received.")