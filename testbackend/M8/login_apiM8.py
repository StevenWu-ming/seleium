import requests
import json
import os
import sys
from urllib.parse import urljoin
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64
import logging

# 添加項目根目錄到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from config.config import Config

# 設置日誌
log_dir = os.path.dirname(__file__)
log_file = os.path.join(log_dir, 'test_log.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(name)s] %(message)s',
    handlers=[
        logging.FileHandler(log_file, mode='w'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
file_path = Config.RANDOM_DATA_JSON_PATH

LOGIN_URL = "https://uat8-newplatform.mxsyl.com/v1/member/auth/loginbyemail"
VERIFY2FA_URL = "https://uat8-newplatform.mxsyl.com/v1/member/auth/verify2fa"

class LoginAPI:
    # 分別存 setup token（before_token）和登入後 token（last_token）
    before_token = None
    last_token = None
    last_uniCode = None
    last_email = None

    @staticmethod
    def run_setup_api():
        cfg = Config.get_current_config()
        url = urljoin(cfg.BASE_URL, cfg.SET_UP_API)
        headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = response.json()
        else:
            logger.error(f"錯誤 {response.status_code}: {response.text}")
            result = None

        if result is not None and result.get("success"):
            LoginAPI.before_token = result["data"]
            logger.info(f"✅ {Config.ENV} setup 成功 before_token: {LoginAPI.before_token}")
        else:
            logger.error("❌ setup 失敗")
            if result:
                logger.error(f"錯誤訊息: {result}")
            else:
                logger.error("未收到錯誤訊息")
        return result

    @staticmethod
    def encrypt_password(password: str, public_key_pem: str) -> str:
        rsa_key = RSA.import_key(public_key_pem)
        cipher = PKCS1_v1_5.new(rsa_key)
        encrypted = cipher.encrypt(password.encode("utf-8"))
        return base64.b64encode(encrypted).decode("utf-8")

    @staticmethod
    def login(email=None, password=None):
        cfg = Config.get_current_config()
        email = email or "cooper009@grr.la"
        password = password or "1234Qwer"

        token = LoginAPI.before_token
        if not token:
            logger.error("❌ before_token 尚未取得，請先執行 run_setup_api")
            return None

        rsa_public_key = f"""-----BEGIN PUBLIC KEY-----
{cfg.public_key_content}
-----END PUBLIC KEY-----"""
        try:
            encrypted = LoginAPI.encrypt_password(password, rsa_public_key)
        except Exception as e:
            logger.error(f"❌ 密碼加密失敗: {str(e)}")
            return None

        headers = {
            "authorization": f"Bearer {token}",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
        }
        payload = {
            "email": email,
            "password": encrypted
        }

        response = requests.post(LOGIN_URL, json=payload, headers=headers)
        if response.status_code == 200:
            result = response.json()
        else:
            logger.error(f"錯誤 {response.status_code}: {response.text}")
            result = None

        if result is not None and result.get("success"):
            data = result["data"]
            LoginAPI.last_token = data.get("token", "")
            LoginAPI.last_uniCode = data.get("uniCode", "")
            LoginAPI.last_email = email
            logger.info(f"✅ {Config.ENV} 登入成功 last_token: {LoginAPI.last_token} uniCode: {LoginAPI.last_uniCode}")
        else:
            logger.error("❌ 登入失敗")
            if result:
                logger.error(f"失敗訊息: {result}")
            else:
                logger.error("未收到錯誤訊息")
            logger.error(f"payload: {payload}")

        return result

class TwoFAAPI:
    @staticmethod
    def verify_2fa(email=None, email_code="123456", use_setup_token=True):
        """
        預設使用登入後 token 驗證 2FA。
        如需用 before_token 驗證（非標準流程，僅測試用），請設 use_setup_token=True
        """
        token = LoginAPI.before_token if use_setup_token else LoginAPI.last_token
        uniCode = LoginAPI.last_uniCode
        email = email or LoginAPI.last_email

        if not (uniCode and email):
            logger.error("❌ 尚未登入成功，token/uniCode/email 不完整")
            return None

        headers = {
            "authorization": f"Bearer {token}",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
            "Content-Type": "application/json"
        }
        payload = {
            "uniCode": uniCode,
            "email": email,
            "emailCode": email_code
        }
        logger.info(f"發送 2FA 請求，用 {'before_token' if use_setup_token else 'last_token'}，payload: {payload}")

        response = requests.post(VERIFY2FA_URL, headers=headers, json=payload)
        try:
            result = response.json()
        except Exception:
            logger.error(f"⚠️ 2FA response JSON 解析失敗: {response.text}")
            return None

        logger.info(f"2FA 回應: {json.dumps(result, ensure_ascii=False)}")
        return result

if __name__ == "__main__":
    LoginAPI.run_setup_api()
    LoginAPI.login()
    # 預設正常驗證（登入後 token）
    TwoFAAPI.verify_2fa()
    # 如需驗證 setup token（除錯用，正常不需這樣做）
    # TwoFAAPI.verify_2fa(use_setup_token=True)
