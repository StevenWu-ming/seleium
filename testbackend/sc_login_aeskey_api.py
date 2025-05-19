# 執行後台管理員登入流程，包含 AES 密鑰獲取、密碼加密、保存加密數據及 API 登入
import requests
import json
import os
import sys
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
from urllib.parse import urljoin
from requests.exceptions import RequestException
import logging

# 設置日誌文件路徑為 selenium_tests/test_log.log
log_dir = os.path.dirname(__file__)  # 獲取當前腳本所在目錄 (selenium_tests)
log_file = os.path.join(log_dir, 'test_log.log')  # 直接放在 selenium_tests 根目錄
# 配置日誌，調整級別為 INFO
logging.basicConfig(
    level=logging.INFO,  # 改為 INFO 級別
    format='%(asctime)s - %(levelname)s - [%(name)s] %(message)s',
    handlers=[
        logging.FileHandler(log_file, mode='w'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 添加項目根目錄到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.config import Config  # 導入 Config

file_path = Config.RANDOM_DATA_JSON_PATH  # ✅ 此為全域值，保留

def load_encrypt_key(json_path: str) -> str:
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("encyptKey", "")  # 默認返回空字符串
    except (json.JSONDecodeError, FileNotFoundError):
        print(f"錯誤：無法讀取 {json_path} 或文件格式錯誤")
        return ""

def load_encrypt_key_ted(json_path: str = file_path) -> tuple[str, str]:
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("key", ""), data.get("encrypted", "")
    except (json.JSONDecodeError, FileNotFoundError):
        print(f"錯誤：無法讀取 {json_path} 或文件格式錯誤")
        return "", ""

def save_encrypted_to_json(json_path: str, encrypted: str):
    # 讀取現有數據
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                logger.warning(f"{json_path} 格式錯誤，將初始化為空數據")
                existing_data = {}
    else:
        existing_data = {}
    # 只更新 encrypted 字段，保留其他字段
    existing_data["encrypted"] = encrypted
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)
    logger.info(f"已更新 encrypted 字段至 {json_path}")

class aes_key_api:
    @staticmethod
    def aes_key():
        cfg = Config.get_current_config()
        endpoint = "/api/v1/admin/auth/getpasswordencryptkey"
        url = urljoin(cfg.BASE_SC_URL, endpoint)
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            result = response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"請求失敗 - {e}")
            return None
        
        if result and isinstance(result, dict):
            new_key = result.get("key", "")
            new_encyptKey = result.get("encyptKey", "")
            
            if not new_key or not new_encyptKey:
                logger.warning("API 響應缺少 key 或 encyptKey")
                return None
            
            # 讀取現有數據
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    try:
                        existing_data = json.load(f)
                    except json.JSONDecodeError:
                        logger.warning(f"{file_path} 格式錯誤，將初始化為空數據")
                        existing_data = {}
            else:
                existing_data = {}
            
            # 只更新 key 和 encyptKey 字段，保留其他字段
            existing_data["key"] = new_key
            existing_data["encyptKey"] = new_encyptKey
            
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(existing_data, f, indent=4, ensure_ascii=False)
                logger.info(f"✅ 數據已保存至 {file_path}")
            except Exception as e:
                logger.error(f"錯誤：無法寫入 {file_path} - {e}")
        else:
            logger.error("無效的 API 響應")
        
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
    PLAINTEXT = cfg.SC_PASSWORD

    # Step 1: Get AES Key
    aes_key_api.aes_key()

    # Step 2: Encrypt password
    KEY = load_encrypt_key(file_path)
    encrypted = encrypt_by_ae.encrypt_by_aes(PLAINTEXT, KEY)

    logger.info(f"明文: {PLAINTEXT}")
    logger.info(f"密鑰: {KEY}")
    logger.info(f"密文: {encrypted}")

    # Step 3: Save encrypted password to JSON
    save_encrypted_to_json(file_path, encrypted)

    # Step 4: Perform login with Admin API
    client = AdminAPIClient()
    try:
        result = client.login()
        logger.info(f"登入成功 狀態碼: {result['status_code']}")

        # 儲存 token 到 JSON
        if isinstance(result.get("response"), dict):
            token_value = result["response"].get("token")
            if token_value:
                # 讀取現有數據
                if os.path.exists(file_path):
                    with open(file_path, "r", encoding="utf-8") as f:
                        try:
                            existing_data = json.load(f)
                        except json.JSONDecodeError:
                            logger.warning(f"{file_path} 格式錯誤，將初始化為空數據")
                            existing_data = {}
                else:
                    existing_data = {}
                
                # 只更新 sc_token 字段，保留其他字段
                existing_data["sc_token"] = token_value
                
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(existing_data, f, indent=4, ensure_ascii=False)
                logger.info("後台token已更新")
            else:
                logger.warning("回傳結果中無 token")
    except RequestException as e:
        logger.error(f"發生錯誤: {e}")

if __name__ == "__main__":
    run_admin_login_workflow()