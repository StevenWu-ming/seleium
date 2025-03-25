import requests
import json
import os
import sys
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
from urllib.parse import urljoin

# 添加項目根目錄到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.config import Config, config  # 導入 Config 和 config

file_path = "/Users/steven/deepseek/seleium/config/random_data.json"

class aes_key_api:
    @staticmethod
    def aes_key():
        url = "http://uat-admin-api.mxsyl.com:5012/api/v1/admin/auth/getpasswordencryptkey"
        
        try:
            print(f"Requesting URL: {url}")
            response = requests.get(url)
            print(f"Status Code: {response.status_code}")
            print(f"Response Headers: {response.headers}")
            print(f"Response Text: {response.text}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error {response.status_code if 'response' in locals() else 'N/A'}: {str(e)}")
            return None
        
    


    # 執行 API 請求
    result = aes_key()
    
    # 修改成功條件，檢查 result 是否為 dict
    if result and isinstance(result, dict):
        # 獲取 key 和 encyptKey，若不存在則使用空字串
        new_key = result.get("key", "")
        new_encyptKey = result.get("encyptKey", "")
        
        # 讀取現有 JSON 檔案
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                try:
                    existing_data = json.load(f)
                except json.JSONDecodeError:
                    existing_data = {}  # 若解析錯誤則使用空字典
        else:
            existing_data = {}  # 若檔案不存在則初始化
        
        # 更新 key 和 encyptKey 到資料中
        existing_data["key"] = new_key
        existing_data["encyptKey"] = new_encyptKey
        
        # 將更新後的資料寫回 JSON
        with open(file_path, "w") as f:
            json.dump(existing_data, f, indent=4)
        
        print("✅ Request successful!")
        print(f"🔹 Data updated in: {file_path}")
        print(f"🔹 Key value: {new_key}")
        print(f"🔹 EncyptKey value: {new_encyptKey}")
    else:
        print("❌ Request failed!")