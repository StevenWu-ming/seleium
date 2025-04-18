import requests
import json
import os
import sys
from urllib.parse import urljoin
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64

# 添加項目根目錄到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.config import Config  # 導入 Config 和 config

config = Config.get_current_config()
file_path = Config.RANDOM_DATA_JSON_PATH


class LoginAPI:
    def run_setup_api():
        # query_string = ("")
        url = urljoin(config.BASE_URL, config.SET_UP_API)

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
            print(f"Error {response.status_code}: {response.text}")
            result = None
        
        # 整合 token 更新邏輯到 login 方法中
        if result is not None and result.get("success"):
            new_token = result["data"]
            
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
            existing_data["before_token"] = new_token
            
            # 將更新後的資料寫回 JSON 檔案
            with open(file_path, "w") as f:
                json.dump(existing_data, f, indent=4)
            
            print(f"✅ {Config.ENV} Login successful!")
            print(f"🔹 Token updated in: {file_path}")
        else:
            print("❌ Login failed!")
            if result:
                print(f"Error details: {result}")
            else:
                print("No valid response received.")
        
        return result
            
    @staticmethod
    def encrypt_password(password: str, public_key_pem: str) -> str:
        rsa_key = RSA.import_key(public_key_pem)
        cipher = PKCS1_v1_5.new(rsa_key)
        encrypted = cipher.encrypt(password.encode("utf-8"))
        return base64.b64encode(encrypted).decode("utf-8")


    @staticmethod
    def login(userName=None, password=None):
        userName = userName or config.VALID_DP_USERNAME
        password = password or config.VALID_PASSWORD
        # 讀取原始 token（可選：在發送請求前讀取當前 token）
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

        # 拼接 URL
        url = urljoin(config.BASE_URL, config.LOGIN_API)
        print("🔐 RSA 密碼加密工具 (模擬前端 JSEncrypt)")
        rsa_public_key = f"""-----BEGIN PUBLIC KEY-----
        {config.public_key_content}
        -----END PUBLIC KEY-----"""
        try:
                password = config.VALID_PASSWORD
                encrypted = LoginAPI.encrypt_password(password, rsa_public_key)
                # print("\n📦 加密後密文 (Base64)：\n", encrypted)
        except Exception as e:
                print("❌ 發生錯誤：", str(e))

        headers = {
            "authorization": f"Bearer {token}",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
        }
        payload = {
            "userName": userName,
            "password": encrypted
        }

        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
        else:
            print(f"Error {response.status_code}: {response.text}")
            result = None
        
        # 整合 token 更新邏輯到 login 方法中
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
            
            # 將更新後的資料寫回 JSON 檔案
            with open(file_path, "w") as f:
                json.dump(existing_data, f, indent=4)
            
            print(f"✅ {Config.ENV} Login successful!")
            print(f"🔹 Token updated in: {file_path}")
        else:
            print("❌ Login failed!")
            if result:
                print(f"Error details: {result}")
            else:
                print("No valid response received.")
        
        return result  # ✅ 只回傳字串，不要整包 result

        


# Example usage
if __name__ == "__main__":
    LoginAPI.run_setup_api()
    LoginAPI.login()
