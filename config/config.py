import datetime
import json
import os
import random
import sys


class Config:
    """全域配置，包含環境參數、商戶選擇與隨機資料生成方法"""

    # 全域設定，直接在這裡指定要使用的環境與商戶
    ENV = "TestEnv"         # 可選："TestEnv", "DevEnv", "ProdEnv"
    MERCHANT = "Merchant1"  # 可選："Merchant1", "Merchant2", "Merchant3", "Merchant4"
    DELAY_SECONDS = 0.5
    WAIT_TIMEOUT = 10

    # 根據作業系統設定路徑
    if sys.platform == "win32":
        CHROMEDRIVER_PATH = r"C:\Users\d1031\新增資料夾\unittest\chormedrive\chromedriver.exe"
        RANDOM_DATA_JSON_PATH = r"C:\Users\d1031\新增資料夾\unittest\config\random_data.json"
    elif sys.platform == "darwin":
        CHROMEDRIVER_PATH = "/Users/steven/deepseek/seleium/chormedrive/chromedriver"
        RANDOM_DATA_JSON_PATH = "/Users/steven/deepseek/seleium/config/random_data.json"
    elif sys.platform == "linux":
        CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"
        RANDOM_DATA_JSON_PATH = "/app/config/random_data.json"
    else:
        raise RuntimeError("Unsupported OS")

    @staticmethod
    def get_chromedriver_path():
        return Config.CHROMEDRIVER_PATH

    @staticmethod
    def get_random_data_json_path():
        return Config.RANDOM_DATA_JSON_PATH

    # 測試環境配置：拆分為 4 個商戶
    class TestEnv:
        class MerchantBase:
            # 後台相關
            BASE_SC_URL = "http://uat-admin-api.mxsyl.com:5012"
            SC_LOGIN_API = "/api/v1/admin/auth/login"
            AES_KEY_API = "/api/v1/admin/auth/getpasswordencryptkey"
            # 前台API
            LOGIN_API = "/v1/member/auth/loginbyname"
            DEPOSIT_API = "/v1/asset/deposit/currency"
            # 後台帳密
            SC_USERNAME = "QA002"
            SC_PASSWORD = "QA002"
            # 驗證碼與金額
            VERIFY_CODE = "123456"
            DP_Amount = '100'
        class Merchant1(MerchantBase):
            BASE_URL = "https://uat-newplatform.mxsyl.com"
            LOGIN_URL = "https://uat-newplatform.mxsyl.com/zh-cn/login"
            REGISTER_URL = "https://uat-newplatform.mxsyl.com/zh-cn/register"

            PHONE_NUMBER = "13100000021"
            EMAIL = "hrtqdwmk@sharklasers.com"
            VALID_USERNAME = "cooper005"
            VALID_DP_USERNAME = "cooper024"
            VALID_DP_NAME = "测试"
            VALID_PASSWORD = "1234Qwer"
            VALID_PASSWORD_MD5 = (
                "J+qUZNvIJnsQ91KG1wDjBxnvIA3w+98epcCr8jN9u03wwEVytx57ScGfoeySN0nex4jiIzG2qfUfRXnSTtsULjPEvtgpTOdEXEH3SKSR1GJEENUxOo7uezgpKrpxobKLJQehXQEeXivDZla7tNe6EDBT6qKsCgmBYMZGNNRaJdmZSG0HkZnZWcJ34/rhQQxEPeU1ZseiK+q3H9Q9RSyB6+fn2wyQtoU4o4BdzjvrapRtLwrIwobiaOH1PeaeIcUKgCX30FQCuYHtOMnKwEBoz4IwuS5z+XFT1XIbdkRMm+FXoZZOQ7BeLCYGgWOEWMhnOQzAKaYkJvI1KYq4OFEraA=="
                )
        class Merchant2(MerchantBase):
            BASE_URL = "https://uat2-newplatform.mxsyl.com/"
            LOGIN_URL = "https://uat2-newplatform.mxsyl.com/zh-cn/login"
            REGISTER_URL = "https://uat2-newplatform.mxsyl.com/zh-cn/register"

            PHONE_NUMBER = ""
            EMAIL = ""
            VALID_USERNAME = ""
            VALID_DP_USERNAME = ""
            VALID_PASSWORD = ""
            VALID_PASSWORD_MD5 = (
                ""
                  )
        class Merchant5(MerchantBase):
            BASE_URL = "https://uat5-newplatform.mxsyl"
            LOGIN_URL = "https://uat5-newplatform.mxsyl/zh-cn/login"
            REGISTER_URL = "https://uat5-newplatform.mxsyl/zh-cn/register"

            PHONE_NUMBER = ""
            EMAIL = ""
            VALID_USERNAME = ""
            VALID_DP_USERNAME = ""
            VALID_PASSWORD = ""
            VALID_PASSWORD_MD5 = (
                ""
                )
        class Merchant7(MerchantBase):
            BASE_URL = "https://uat7-newplatform.mxsyl.com"
            LOGIN_URL = "https://uat7-newplatform.mxsyl.com/zh-cn/login"
            REGISTER_URL = "https://uat7-newplatform.mxsyl.com/zh-cn/register"

            PHONE_NUMBER = ""
            EMAIL = ""
            VALID_USERNAME = ""
            VALID_DP_USERNAME = ""
            VALID_PASSWORD = ""
            VALID_PASSWORD_MD5 = (
                ""
                )

    # 正式環境配置：拆分為 4 個商戶
    class ProdEnv:
        class MerchantBase:
            # 後台相關
            BASE_SC_URL = "https://www.gobackend.xyz/"
            SC_LOGIN_API = "/api/v1/admin/auth/login"
            AES_KEY_API = "/api/v1/admin/auth/getpasswordencryptkey"
            # 前台API
            LOGIN_API = "/v1/member/auth/loginbyname"
            DEPOSIT_API = "/api/v1/asset/deposit/currency"
            # 後台帳密
            SC_USERNAME = "Tech_QA_Tester"
            SC_PASSWORD = "123@Tech_QA_Tester"
            # 驗證碼與金額
            VERIFY_CODE = "123456"
            DP_Amount = '100'
        class Merchant1(MerchantBase):
            BASE_URL = "https://www.lt.com/"
            LOGIN_URL = "https://www.lt.com/zh-cn/login"
            REGISTER_URL = "https://www.lt.com/zh-cn/register"

            PHONE_NUMBER = "18700000005"
            EMAIL = ""
            VALID_DP_NAME = "测试"
            VALID_USERNAME = "QA_M1_05"
            VALID_DP_USERNAME = "QA_M1_05"
            VALID_PASSWORD = "QA_M1_05"
            VALID_PASSWORD_MD5 = (
                "lcuX0yzXBtLR3oEP9Uf4kLmP+zg9IXwq63PnpDwWAPk1x9TbJCFoov0bIUHXIaJsmRkGnJfpshHdTUZeWhs1Lr9Uq1W3DemXoDeOGjMZXdkwyJiol5VRe29tSKzcxHeailQ4BbYE7LC3cIWaOgRKMFcyrbtaehxRb3py+kA513FVMA0ywfjS9B61cgWUwo/NU3F5csERXapGIuPovE9g4ip1ZSq92+9f712PXP5feIp4oDw1XTmtfoUK1aaF9648/rlAeK1RZWc6hiU9vyDs8acK9hkXYpYdbTcE1daL+f+MCL68emCQFZAob73Ke1B3rix36jsRn7Ma1UE+V+jB1A=="
                )
        class Merchant2(MerchantBase):
            BASE_URL = "https://www.mrcatgo.com"
            LOGIN_URL = "https://www.mrcatgo.com/zh-cn/login"
            REGISTER_URL = "https://www.mrcatgo.com/zh-cn/register"

            PHONE_NUMBER = ""
            EMAIL = ""
            VALID_USERNAME = ""
            VALID_DP_USERNAME = ""
            VALID_PASSWORD = ""
            VALID_PASSWORD_MD5 = (
                ""
                )
        class Merchant5(MerchantBase):
            BASE_URL = "https://www.letou1.vip"
            LOGIN_URL = "https://www.letou1.vip/zh-cn#login"
            REGISTER_URL = "https://www.letou1.vip/zh-cn#register"

            PHONE_NUMBER = ""
            EMAIL = ""
            VALID_USERNAME = ""
            VALID_DP_USERNAME = ""
            VALID_PASSWORD = ""
            VALID_PASSWORD_MD5 = (
                ""
                )
        class Merchant7(MerchantBase):
            BASE_URL = "https://vwin158.com"
            LOGIN_URL = "https://vwin158.com/zh-cn/login"
            REGISTER_URL = "https://vwin158.com/zh-cn/register"

            PHONE_NUMBER = ""
            EMAIL = ""
            VALID_USERNAME = ""
            VALID_DP_USERNAME = ""
            VALID_PASSWORD = ""
            VALID_PASSWORD_MD5 = (
                ""
                )



    @classmethod
    def get_current_config(cls):
        """根據全域 ENV 與 MERCHANT 參數取得當前配置"""
        env_class = getattr(cls, cls.ENV)
        merchant_config = getattr(env_class, cls.MERCHANT)
        return merchant_config

    @staticmethod
    def generate_random_username():
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        random_username = f"QAM1{timestamp}"
        save_random_data_to_json({"random_username": random_username})
        return random_username

    @staticmethod
    def generate_japanese_phone_number():
        prefixes = ['070', '080', '090']
        prefix = random.choice(prefixes)
        remaining_digits = ''.join(str(random.randint(1, 9)) for _ in range(8))
        japanese_phone = prefix + remaining_digits
        save_random_data_to_json({"japanese_phone_number": japanese_phone})
        return japanese_phone

    @staticmethod
    def generate_random_email():
        username = Config.generate_random_username()
        email = f"{username}@gmail.com"
        save_random_data_to_json({"random_email": email})
        return email

def save_random_data_to_json(data):
    json_path = Config.get_random_data_json_path()
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            existing_data = json.load(f)
    else:
        existing_data = {}
    existing_data.update(data)
    with open(json_path, 'w') as f:
        json.dump(existing_data, f, indent=4, ensure_ascii=False)
    print(f"隨機資料已儲存到: {json_path}")


# 確保目標目錄存在
os.makedirs(os.path.dirname(Config.get_random_data_json_path()), exist_ok=True)

# 自動取得目前設定的環境與商戶配置
# config = Config.get_current_config()

if __name__ == "__main__":
    print(f"當前環境: {Config.ENV}")
    print(f"目前商戶: {Config.MERCHANT}")
    print(f"BASE_URL: {config.BASE_URL}")
    print(f"LOGIN_URL: {config.LOGIN_URL}")
    print(f"VALID_USERNAME: {config.VALID_USERNAME}")
