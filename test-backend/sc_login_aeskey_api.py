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

def load_encrypt_key(json_path: str) -> str:
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data["encyptKey"]

def save_encrypted_to_json(json_path: str, encrypted: str):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    data["encrypted"] = encrypted
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

PLAINTEXT = config.SC_PASSWORD  # 從 config.py 獲取明文

class aes_key_api:
    @staticmethod
    def aes_key():
        endpoint = "/api/v1/admin/auth/getpasswordencryptkey"
        url = urljoin(config.BASE_SC_URL, endpoint)
        # url = "http://uat-admin-api.mxsyl.com:5012/api/v1/admin/auth/getpasswordencryptkey"
        
        try:
            print(f"Requesting URL: {url}")
            response = requests.get(url)
            print(f"Status Code: {response.status_code}")
            print(f"Response Headers: {response.headers}")
            print(f"Response Text: {response.text}")
            response.raise_for_status()
            result = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error {response.status_code if 'response' in locals() else 'N/A'}: {str(e)}")
            return None
        
        if result and isinstance(result, dict):
            new_key = result.get("key", "")
            new_encyptKey = result.get("encyptKey", "")
            
            # 讀取現有 JSON 檔案
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    try:
                        existing_data = json.load(f)
                    except json.JSONDecodeError:
                        existing_data = {}
            else:
                existing_data = {}
            
            # 更新 key 和 encyptKey 到 JSON
            existing_data["key"] = new_key
            existing_data["encyptKey"] = new_encyptKey
            
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(existing_data, f, indent=4, ensure_ascii=False)
            
            print("✅ Request successful!")
            print(f"🔹 Data updated in: {file_path}")
            print(f"🔹 Key value: {new_key}")
            print(f"🔹 EncyptKey value: {new_encyptKey}")
        else:
            print("❌ Request failed!")
        
        return result

class encrypt_by_ae:
    @staticmethod
    def encrypt_by_aes(plaintext: str, key: str) -> str:
        key_bytes = key.encode('utf-8')
        if len(key_bytes) != 16:
            raise ValueError("密鑰長度必須為 16 字節 (128 位)")
        plaintext_bytes = plaintext.encode('utf-8')
        cipher = AES.new(key_bytes, AES.MODE_ECB)
        padded_bytes = pad(plaintext_bytes, AES.block_size, style='pkcs7')
        ciphertext_bytes = cipher.encrypt(padded_bytes)
        ciphertext_base64 = base64.b64encode(ciphertext_bytes).decode('utf-8')
        return ciphertext_base64

if __name__ == "__main__":
    # 先呼叫 aes_key_api.aes_key()，更新 JSON 檔案中的密鑰資料
    aes_key_api.aes_key()
    
    # 重新讀取最新的密鑰
    KEY = load_encrypt_key(file_path)
    
    # 使用更新後的 KEY 進行加密
    encrypted = encrypt_by_ae.encrypt_by_aes(PLAINTEXT, KEY)
    print(f"明文: {PLAINTEXT}")
    print(f"密鑰: {KEY}")
    print(f"密文: {encrypted}")
    
    save_encrypted_to_json(file_path, encrypted)
    print(f"密文已存入 {file_path}")
