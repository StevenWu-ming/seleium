import requests
import json
import os
import sys
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
from urllib.parse import urljoin
from requests.exceptions import RequestException

# 添加項目根目錄到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.config import Config  # 導入 Config

file_path = Config.RANDOM_DATA_JSON_PATH  # ✅ 此為全域值，保留


def load_encrypt_key(json_path: str) -> str:
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data["encyptKey"]

def load_encrypt_key_ted(json_path: str = file_path) -> tuple[str, str]:
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data["key"], data["encrypted"]

def save_encrypted_to_json(json_path: str, encrypted: str):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    data["encrypted"] = encrypted
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

class aes_key_api:
    @staticmethod
    def aes_key():
        cfg = Config.get_current_config()
        endpoint = "/api/v1/admin/auth/getpasswordencryptkey"
        url = urljoin(cfg.BASE_SC_URL, endpoint)
        
        try:
            print(f"請求URL: {url}")
            response = requests.get(url)
            print(f"狀態碼: {response.status_code}")
            # data = response.json()
            # print(f"✅ encyptKey: {data.get('key')}")
            # print(f"✅ key: {data.get('encyptKey')}")
            # print(f"Response Headers: {response.headers}")
            # print(f"Response Text: {response.text}")
            response.raise_for_status()
            result = response.json()
        except requests.exceptions.RequestException as e:
            print(f"錯誤 {response.status_code if '回傳' in locals() else 'N/A'}: {str(e)}")
            return None
        
        if result and isinstance(result, dict):
            new_key = result.get("key", "")
            new_encyptKey = result.get("encyptKey", "")

            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    try:
                        existing_data = json.load(f)
                    except json.JSONDecodeError:
                        existing_data = {}
            else:
                existing_data = {}

            existing_data["key"] = new_key
            existing_data["encyptKey"] = new_encyptKey

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(existing_data, f, indent=4, ensure_ascii=False)

            print("✅ 請求後台密碼加密成功")
            print(f"🔹 數據更新: {file_path}")
            # print(f"🔹 加密key: {new_key}")
            # print(f"🔹 加密密鑰: {new_encyptKey}")
        else:
            print("❌ 請求失敗!")
        
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

class AdminAPIClient:
    """用於處理管理員API請求的類別"""
    
    def __init__(self):
        cfg = Config.get_current_config()
        self.base_url = cfg.BASE_SC_URL
        self.session = requests.Session()
        self.headers = {
            'Content-Type': 'application/json'
        }

    def login(self, username=None, password=None, password_key=None):
        cfg = Config.get_current_config()
        username = username or cfg.SC_USERNAME
        password = password or load_encrypt_key_ted()[1]
        password_key = password_key or load_encrypt_key_ted()[0]

        endpoint = cfg.SC_LOGIN_API
        url = urljoin(self.base_url, endpoint)

        payload = {
            "userName": username,
            "password": password,
            "passwordKey": password_key
        }

        try:
            response = self.session.post(
                url,
                json=payload,
                headers=self.headers,
                verify=False
            )
            response.raise_for_status()
            return {
                "status_code": response.status_code,
                "response": json.loads(response.text)
            }
        except RequestException as e:
            raise RequestException(f"Login failed: {str(e)}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()


def run_admin_login_workflow():
    cfg = Config.get_current_config()
    PLAINTEXT = cfg.SC_PASSWORD  # ✅ 動態取得明文密碼

    # Step 1: Get AES Key
    aes_key_api.aes_key()

    # Step 2: Encrypt password
    KEY = load_encrypt_key(file_path)
    encrypted = encrypt_by_ae.encrypt_by_aes(PLAINTEXT, KEY)

    print(f"明文: {PLAINTEXT}")
    print(f"密鑰: {KEY}")
    print(f"密文: {encrypted}")

    # Step 3: Save encrypted password to JSON
    save_encrypted_to_json(file_path, encrypted)

    # Step 4: Perform login with Admin API
    client = AdminAPIClient()
    try:
        result = client.login()
        print(f"登入成功 狀態碼: {result['status_code']}")
        # print(f"Response: {result['response']}")

        # 儲存 token 到 JSON
        if isinstance(result.get("response"), dict):
            token_value = result["response"].get("token")
            if token_value:
                if os.path.exists(file_path):
                    with open(file_path, "r", encoding="utf-8") as f:
                        try:
                            existing_data = json.load(f)
                        except json.JSONDecodeError:
                            existing_data = {}
                else:
                    existing_data = {}

                existing_data["sc_token"] = token_value

                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(existing_data, f, indent=4, ensure_ascii=False)
                print(f"後台token已更新")
                # print(f"後台token已更新: {token_value}")
            else:
                print("回傳結果中無 token")
    except RequestException as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    run_admin_login_workflow()
