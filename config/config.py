import datetime
import json
import os
import random
import sys


class Config:
    """全域配置，包含環境參數與隨機資料生成方法"""

    ENV = "TestEnv"
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

    class TestEnv:
        BASE_SC_URL = "http://uat-admin-api.mxsyl.com:5012"
        BASE_URL = "https://uat-newplatform.mxsyl.com"
        LOGIN_URL = "https://uat-newplatform.mxsyl.com/zh-cn/login"
        REGISTER_URL = "https://uat-newplatform.mxsyl.com/zh-cn/register"

        SC_LOGIN_API = "/api/v1/admin/auth/login"
        AES_KEY_API = "/api/v1/admin/auth/getpasswordencryptkey"
        LOGIN_API = "/v1/member/auth/loginbyname"
        DEPOSIT_API = "/v1/asset/deposit/currency"

        SC_USERNAME = "QA006"
        SC_PASSWORD = "QA006"

        VALID_USERNAME = "cooper005"
        VALID_DP_USERNAME = "cooper006"
        VALID_PASSWORD = "1234Qwer"
        VALID_PASSWORD_MD5 = (
            "sDU34ZeaABRD77WOcpBQVNg5Am8h0a8nKKNiu6LASXY5yitfJx6DUAHh8OIXS9cKeU/O4ZwIkpJFglz/"
            "oeEEiUsSjTuJxVXsaKOtq8Yu0e0iiIEFlucnlzRPHFISgz0wTYk/+kzkFUuciDPYt8hWkR99D+PiMQSX+iC"
            "NLXhxnsvjw2/gkXF9IC827hwWiKqhcc5JqBSGvDUmLzih5QlzYchzpCQrnheACEaPT9m2GNL7OYWhaZtZA42a"
            "X02iOBvtfgegrORepatpjcRowVRT77B7Nst97x13vkbRZ983rFEki1yZFWD24OutSgr4bB8X1mtXstJ2C495OA3GdZNkQQ=="
        )

        NVALID_USERNAME_PREFIX = None  # 動態生成
        INVALID_PHONE_NUMBER = None    # 動態生成
        INVALID_EMAIL = None           # 動態生成

        PHONE_NUMBER = "13100000021"
        EMAIL = "hrtqdwmk@sharklasers.com"
        VERIFY_CODE = "123456"
        DP_Amount = '100'

    class DevEnv:
        BASE_URL = "https://dev-newplatform.mxsyl.com"
        BASE_SC_URL = "http://uat.newplatformadmin.mxsyl.com/"
        LOGIN_URL = "https://dev-newplatform.mxsyl.com/zh-cn/login"
        REGISTER_URL = "https://uat-newplatform.mxsyl.com/zh-cn/register"

        VALID_USERNAME = "cooper018"
        VALID_PASSWORD = "Dev1234Qwer"
        INVALID_USERNAME_PREFIX = None  # 動態生成
        INVALID_PHONE_NUMBER = None     # 動態生成
        INVALID_EMAIL = None            # 動態生成

        PHONE_NUMBER = "13900000001"
        EMAIL = "dev_hrtqdwmk@sharklasers.com"
        VERIFY_CODE = "123456"

    class ProdEnv:
        BASE_URL = "https://www.lt.com/zh-cn/login"
        LOGIN_URL = "https://www.lt.com/zh-cn/login"
        REGISTER_URL = "https://www.lt.com/zh-cn/register"

        VALID_USERNAME = "QA_M1_02"
        VALID_PASSWORD = "QA_M1_02"
        INVALID_USERNAME_PREFIX = None  # 動態生成
        INVALID_PHONE_NUMBER = None     # 動態生成
        INVALID_EMAIL = None            # 動態生成

        PHONE_NUMBER = "18700000002"
        EMAIL = "hrtqdwmk@sharklasers.com"
        VERIFY_CODE = "123456"

    @staticmethod
    def generate_random_username():
        """根據當前時間生成隨機使用者名稱"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        random_username = f"QAM1{timestamp}"
        save_random_data_to_json({"random_username": random_username})
        return random_username

    @staticmethod
    def generate_japanese_phone_number():
        """生成隨機日本手機號碼"""
        prefixes = ['070', '080', '090']
        prefix = random.choice(prefixes)
        remaining_digits = ''.join(str(random.randint(1, 9)) for _ in range(8))
        japanese_phone = prefix + remaining_digits
        save_random_data_to_json({"japanese_phone_number": japanese_phone})
        return japanese_phone

    @staticmethod
    def generate_random_email():
        """使用隨機使用者名稱生成隨機 email"""
        username = Config.generate_random_username()
        email = f"{username}@gmail.com"
        save_random_data_to_json({"random_email": email})
        return email


def save_random_data_to_json(data):
    """將隨機生成的資料儲存到 JSON 文件中"""
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

# 根據配置環境取得對應環境設定
CURRENT_ENV = getattr(Config, Config.ENV)
config = CURRENT_ENV

if __name__ == "__main__":
    print(f"當前環境: {Config.ENV}")
    print(f"BASE_URL: {config.BASE_URL}")
    print(f"LOGIN_URL: {config.LOGIN_URL}")
    print(f"VALID_USERNAME: {config.VALID_USERNAME}")
    print(f"VALID_DP_USERNAME: {config.VALID_DP_USERNAME}")
