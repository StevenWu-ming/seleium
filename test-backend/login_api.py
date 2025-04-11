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


file_path = "/Users/steven/deepseek/seleium/config/random_data.json"
config = Config.get_current_config()

# 讀取原始 token（可選：在發送請求前讀取當前 token）
token = None
try:
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    token = data.get("before_token")
    if not token:
        raise ValueError("JSON 檔案中缺少 'token' 字段")
except FileNotFoundError:
    print(f"錯誤：找不到檔案 {file_path}")
except json.JSONDecodeError:
    print("錯誤：JSON 檔案格式無效")
except Exception as e:
    print(f"發生錯誤：{str(e)}")


class LoginAPI:
    def run_setup_api():
        url = (
            "https://uat-newplatform.mxsyl.com/v1/api/auth/setup?s="
            "eSGwvL70s4%2F1Uc8jOs%2BEdjTTY7ABjG%2BCJta8QmZOtHULSAbatME47%2Bt1QY8ktqW9wbPxFmh7huwAApMflnR6PtjBqoTz%2FCmzADuNcMhdNxr0jRR5TfVyi%2FmSDnEPwGpNwpfwwKllYmSPqufI9RpgwuKI112fHbrG7jFq4F0spPZIxdC2aenXt5SwdPQv8D4xc2yw%2BOwRpttIaMKKo8xXiaqxrr52UfIfQyJCPfdjS0dIPtivex81oo6813jBPMjzNMMcmaJw4efnfDQPG6xfERAdTf8OdRj1XrNNFjTcP3rIg%2Bp89ObbZ7plal5xoQovmdF7JKiZi85RQzuuV%2BQgEg%3D%3D"
            )

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
    def login():
        # 拼接 URL
        url = urljoin(config.BASE_URL, config.LOGIN_API)
        print("🔐 RSA 密碼加密工具 (模擬前端 JSEncrypt)")

        rsa_public_key = """-----BEGIN PUBLIC KEY-----
        MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA1lcU5lRpSOqdLicIimSso8wSCTDWdtv3BXGeixALS+bcqOMmV2Tm5F5O3sOAku/a+XxeC+yXkaVrCXpgsl0LEPGVnqO5XoVs4LTeo0zwCJQ+H7TN1ZlqkpfFCL7Mn1+dUXvy+N2p5ijlTZiFsfetc+Jr/JH2Zj62nnc/Vpxne0RsKLwh4Mwp6i/BSv2H9xurablJpz3GPb0qoTniCuxzXvCR9h2tFfbCNacrdpOFVW/A8g27g5em+uqjVB5xAhM1pj0b5PlgR6Oyn5c5mmK1waBx/P+NZJRmGrDbHZMq07v3ma9LTOCGGoG90ReYHxVFRSlAzfl5NGF9nrkfZW4skQIDAQAB
        -----END PUBLIC KEY-----"""

        try:
                password = config.VALID_PASSWORD
                encrypted = LoginAPI.encrypt_password(password, rsa_public_key)
                print("\n📦 加密後密文 (Base64)：\n", encrypted)
        except Exception as e:
                print("❌ 發生錯誤：", str(e))

        headers = {
            "authorization": f"Bearer {token}",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
        }
        payload = {
            "userName": config.VALID_DP_USERNAME,
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
