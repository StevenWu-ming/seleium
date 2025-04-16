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
from config.config import Config  # 導入 Config 和 config


config = Config.get_current_config()
file_path = Config.RANDOM_DATA_JSON_PATH


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

class AdminAPIClient:
    """用於處理管理員API請求的類別"""
    
    def __init__(self, base_url=config.BASE_SC_URL):
        """初始化API客戶端
        
        Args:
            base_url (str): API的基本URL，預設為UAT環境
        """
        self.base_url = base_url
        self.session = requests.Session()
        self.headers = {
            'Content-Type': 'application/json'
        }

    def login(self, username=config.SC_USERNAME, 
             password=load_encrypt_key_ted()[1], 
             password_key=load_encrypt_key_ted()[0]
             ):
        """執行管理員登錄
        
        Args:
            username (str): 用戶名，預設為"QA006"
            password (str): 密碼，預設為加密後的值
            password_key (str): 密碼密鑰
            
        Returns:
            dict: 包含狀態碼和響應數據的字典
            
        Raises:
            RequestException: 當請求失敗時拋出
        """
        endpoint = config.SC_LOGIN_API
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
        """支援上下文管理器"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """關閉session"""
        self.session.close()


def run_admin_login_workflow():
    """執行整體管理員登入流程，包括取得密鑰、加密密碼、登入並存儲 token"""
    # 1. 取得 AES 密鑰
    aes_key_api.aes_key()

    # 2. 使用新的 key 對密碼加密
    KEY = load_encrypt_key(file_path)
    encrypted = encrypt_by_ae.encrypt_by_aes(PLAINTEXT, KEY)

    print(f"明文: {PLAINTEXT}")
    print(f"密鑰: {KEY}")
    print(f"密文: {encrypted}")

    # 3. 存儲加密密碼到 JSON
    save_encrypted_to_json(file_path, encrypted)
    print(f"密文已存入 {file_path}")

    # 4. 使用 Admin API 登入並儲存 token
    client = AdminAPIClient()
    try:
        result = client.login()
        print(f"Status Code: {result['status_code']}")
        print(f"Response: {result['response']}")

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

                print(f"sc_token 已儲存: {token_value}")
            else:
                print("回傳結果中無 token")
    except RequestException as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    run_admin_login_workflow()