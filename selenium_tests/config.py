# config.py
import random
import string
import datetime
import json
import os
import sys


def save_random_data_to_json(data):
    """將隨機生成的資料儲存到 JSON 文件中"""
    random_data_json_path = Config.get_random_data_json_path()  # ✅ 正確獲取 JSON 文件路徑

    if os.path.exists(random_data_json_path):
        with open(random_data_json_path, 'r') as f:
            existing_data = json.load(f)
    else:
        existing_data = {}

    existing_data.update(data)
    with open(random_data_json_path, 'w') as f:
        json.dump(existing_data, f, indent=4, ensure_ascii=False)
    print(f"隨機資料已儲存到: {random_data_json_path}")



class Config:
    if sys.platform == "win32":  # Windows 環境
        CHROMEDRIVER_PATH = r"C:\Users\d1031\新增資料夾\unittest\selenium_tests\chormedrive\chromedriver.exe"
        RANDOM_DATA_JSON_PATH = r"C:\Users\d1031\新增資料夾\unittest\selenium_tests\random_data.json"
    elif sys.platform == "darwin":  # macOS 環境
        CHROMEDRIVER_PATH = "/Users/steven/deepseek/seleium/selenium_tests/chormedrive/chromedriver"
        RANDOM_DATA_JSON_PATH = "/Users/steven/deepseek/seleium/selenium_tests/random_data.json"
    else:
        raise RuntimeError("Unsupported OS")

    @staticmethod
    def get_chromedriver_path():
        return Config.CHROMEDRIVER_PATH

    @staticmethod
    def get_random_data_json_path():
        return Config.RANDOM_DATA_JSON_PATH


    DELAY_SECONDS = 2
    WAIT_TIMEOUT = 10
    
    # 直接指定環境（不再依賴環境變數）
    ENV = "TestEnv"



    # 測試環境配置
    class TestEnv:
        BASE_URL = "https://uat-newplatform.mxsyl.com/zh-cn/login"
        LOGIN_URL = "https://uat-newplatform.mxsyl.com/zh-cn/login"
        REGISTER_URL = "https://uat-newplatform.mxsyl.com/zh-cn/register"
        VALID_USERNAME = "cooper006"
        VALID_PASSWORD = "1234Qwer"
        INVALID_USERNAME_PREFIX = None  # 初始化為 None，動態生成
        INVALID_PHONE_NUMBER = None     # 初始化為 None，動態生成
        INVALID_EMAIL = None            # 初始化為 None，動態生成
        PHONE_NUMBER = "13100000033"
        EMAIL = "hrtqdwmk@sharklasers.com"
        VERIFY_CODE = "123456"
        DP_Amount = '100'

    # 開發環境配置
    class DevEnv:
        BASE_URL = "https://dev-newplatform.mxsyl.com/zh-cn/login"
        LOGIN_URL = "https://dev-newplatform.mxsyl.com/zh-cn/login"
        REGISTER_URL = "https://uat-newplatform.mxsyl.com/zh-cn/register"
        VALID_USERNAME = "cooper018"
        VALID_PASSWORD = "Dev1234Qwer"
        INVALID_USERNAME_PREFIX = None  # 初始化為 None，動態生成
        INVALID_PHONE_NUMBER = None     # 初始化為 None，動態生成
        INVALID_EMAIL = None            # 初始化為 None，動態生成
        PHONE_NUMBER = "13900000001"
        EMAIL = "dev_hrtqdwmk@sharklasers.com"
        VERIFY_CODE = "123456"

    # 生產環境配置
    class ProdEnv:
        BASE_URL = "https://www.lt.com/zh-cn/login"
        LOGIN_URL = "https://www.lt.com/zh-cn/login"
        REGISTER_URL = "https://www.lt.com/zh-cn/register"
        VALID_USERNAME = "QA_M1_02"
        VALID_PASSWORD = "QA_M1_02"
        INVALID_USERNAME_PREFIX = None  # 初始化為 None，動態生成
        INVALID_PHONE_NUMBER = None     # 初始化為 None，動態生成
        INVALID_EMAIL = None            # 初始化為 None，動態生成
        PHONE_NUMBER = "18700000002"
        EMAIL = "hrtqdwmk@sharklasers.com"
        VERIFY_CODE = "123456"

    # 隨機生成方法
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
        remaining_digits = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        japanese_phone = prefix + remaining_digits
        save_random_data_to_json({"japanese_phone_number": japanese_phone})
        return japanese_phone

    @staticmethod
    def generate_random_email():
        username = Config.generate_random_username()
        email = f"{username}@gmail.com"
        save_random_data_to_json({"random_email": email})
        return email

# 確保目標目錄存在
os.makedirs(os.path.dirname(Config.get_random_data_json_path()), exist_ok=True)


# 在類定義完成後設置 CURRENT_ENV 和 config
CURRENT_ENV = getattr(Config, Config.ENV)
config = CURRENT_ENV

if __name__ == "__main__":
    print(f"當前環境: {Config.ENV}")
    print(f"BASE_URL: {config.BASE_URL}")
    print(f"LOGIN_URL: {config.LOGIN_URL}")
    print(f"VALID_USERNAME: {config.VALID_USERNAME}")