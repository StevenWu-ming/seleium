# 提供登入相關 API 調用功能，包括獲取初始 token、RSA 密碼加密及用戶登入流程
import requests
import json
import os
import sys
from urllib.parse import urljoin
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64

# 添加項目根目錄到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from config.config import Config  # 導入 Config
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
file_path = Config.RANDOM_DATA_JSON_PATH  

LOGIN_URL = "https://uat8-newplatform.mxsyl.com/v1/member/auth/loginbyemail"


class LoginAPI:
    def run_setup_api():
        cfg = Config.get_current_config()

        url = urljoin(cfg.BASE_URL, cfg.SET_UP_API)
        headers = {
            "user-agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/134.0.0.0 Safari/537.36"
            )
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            result = response.json()
        else:
            print(f"錯誤 {response.status_code}: {response.text}")
            result = None

        if result is not None and result.get("success"):
            new_token = result["data"]

            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    try:
                        existing_data = json.load(f)
                    except json.JSONDecodeError:
                        existing_data = {}
            else:
                existing_data = {}

            existing_data["before_token"] = new_token

            with open(file_path, "w") as f:
                json.dump(existing_data, f, indent=4)

            print(f"✅ {Config.ENV} 獲取未登入Token成功!")  
            print(f"🔹 Token 更新至: {file_path}")
        else:
            print("❌ 登入失敗")
            if result:
                print(f"錯誤訊息: {result}")
            else:
                print("未收到錯誤訊息")
        return result


    #前台登入密碼加密流程
    @staticmethod
    def encrypt_password(password: str, public_key_pem: str) -> str:
        rsa_key = RSA.import_key(public_key_pem)
        cipher = PKCS1_v1_5.new(rsa_key)
        encrypted = cipher.encrypt(password.encode("utf-8"))
        return base64.b64encode(encrypted).decode("utf-8")

    @staticmethod
    def login(email=None, password=None):
        cfg = Config.get_current_config()

        email = email or "cooper003@grr.la"
        password = password or  "1234Qwer"

        token = None
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            token = data.get("before_token")
            if not token:
                raise ValueError("JSON 檔案中缺少 'before_token' 字段")
        except FileNotFoundError:
            print(f"錯誤：找不到檔案 {file_path}")
        except json.JSONDecodeError:
            print("錯誤：JSON 檔案格式無效")
        except Exception as e:
            print(f"發生錯誤：{str(e)}")

        url = LOGIN_URL


        print("🔐 RSA 密碼加密工具")
        rsa_public_key = f"""-----BEGIN PUBLIC KEY-----
        {cfg.public_key_content}
        -----END PUBLIC KEY-----"""
        try:
            password = "1234Qwer"
            encrypted = LoginAPI.encrypt_password(password, rsa_public_key)
        except Exception as e:
            print("❌ 錯誤訊息：", str(e))

        headers = {
            "authorization": f"Bearer {token}",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
        }
        payload = {
            "email": email,
            "password": encrypted
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            result = response.json()
        else:
            print(f"錯誤 {response.status_code}: {response.text}")
            result = None

        if result is not None and result.get("success"):
            new_token = result["data"].get("token", "")

            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    try:
                        existing_data = json.load(f)
                    except json.JSONDecodeError:
                        existing_data = {}
            else:
                existing_data = {}

            existing_data["token"] = new_token

            with open(file_path, "w") as f:
                json.dump(existing_data, f, indent=4)

            print(f"✅ {Config.ENV} 登入成功!")  
            print(f"🔹 登入Token更新至: {file_path}")
        else:
            print("❌ 登入失敗")
            if result:
                print(f"失敗訊息: {result}")
            else:
                print("未收到錯誤訊息")
                print(email, encrypted)  

        return result


# Example usage
if __name__ == "__main__":
    LoginAPI.run_setup_api()
    LoginAPI.login()
