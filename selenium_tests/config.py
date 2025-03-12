import random
import string
import json
import os

# 定義儲存隨機資料的 JSON 文件路徑
RANDOM_DATA_JSON_PATH = "/Users/steven/deepseek/uninttest/selenium_tests/random_data.json"

# 確保目標目錄存在
os.makedirs(os.path.dirname(RANDOM_DATA_JSON_PATH), exist_ok=True)

def save_random_data_to_json(data):
    """將隨機生成的資料儲存到 JSON 文件中"""
    # 如果文件已存在，讀取現有資料並更新
    if os.path.exists(RANDOM_DATA_JSON_PATH):
        with open(RANDOM_DATA_JSON_PATH, 'r') as f:
            existing_data = json.load(f)
    else:
        existing_data = {}

    # 更新資料
    existing_data.update(data)

    # 寫入 JSON 文件
    with open(RANDOM_DATA_JSON_PATH, 'w') as f:
        json.dump(existing_data, f, indent=4, ensure_ascii=False)
    print(f"隨機資料已儲存到: {RANDOM_DATA_JSON_PATH}")

def generate_random_username(length=8):
    letters_and_digits = string.ascii_lowercase + string.digits
    random_username = 'A' + ''.join(random.choice(letters_and_digits) for _ in range(length))
    # 儲存到 JSON
    save_random_data_to_json({"random_username": random_username})
    return random_username

def generate_japanese_phone_number():
    prefixes = ['070', '080', '090']
    prefix = random.choice(prefixes)
    remaining_digits = ''.join([str(random.randint(0, 9)) for _ in range(8)])
    japanese_phone = prefix + remaining_digits
    # 儲存到 JSON
    save_random_data_to_json({"japanese_phone_number": japanese_phone})
    return japanese_phone

def generate_chinese_phone_number():
    # 中國大陸常見的行動電話號段（僅列出部分作為範例）
    prefixes = [
        '130', '131', '132', '133', '134', '135', '136', '137', '138', '139',  # 中國聯通
        '145', '147',  # 中國聯通（數據卡）
        '150', '151', '152', '153', '155', '156', '157', '158', '159',  # 中國聯通
        '166', '167', '170', '171', '173', '175', '176', '177', '178',  # 中國聯通
        '180', '181', '182', '183', '184', '185', '186', '187', '188', '189',  # 中國電信
        '190', '191', '193', '195', '196', '197', '198', '199',  # 中國電信
    ]
    # 隨機選擇一個號段
    prefix = random.choice(prefixes)
    # 隨機生成剩餘的 8 位數字
    remaining_digits = ''.join([str(random.randint(0, 9)) for _ in range(8)])
    chinese_phone = prefix + remaining_digits
    # 儲存到 JSON
    save_random_data_to_json({"chinese_phone_number": chinese_phone})
    return chinese_phone

def generate_random_email():
    """生成隨機的 Gmail 地址"""
    username = generate_random_username()
    email = f"{username}@gmail.com"
    # 儲存到 JSON
    save_random_data_to_json({"random_email": email})
    return email


class Config:
    # 通用配置
    CHROMEDRIVER_PATH = "/Users/steven/deepseek/uninttest/selenium_tests/chormedrive/chromedriver"  # ChromeDriver 路徑，根據需要調整
    DELAY_SECONDS = 2
    WAIT_TIMEOUT = 10  # WebDriverWait 超時時間
    
    # 直接指定環境（不再依賴環境變數）
    ENV = "TestEnv"
        
    # 測試環境配置
    class TestEnv:
        BASE_URL = "https://uat-newplatform.mxsyl.com/zh-cn/login"
        LOGIN_URL = "https://uat-newplatform.mxsyl.com/zh-cn/login"
        REGISTER_URL = "https://uat-newplatform.mxsyl.com/zh-cn/register"
        VALID_USERNAME = "cooper005"
        VALID_PASSWORD = "1234Qwer"
        INVALID_USERNAME_PREFIX = generate_random_username()
        INVALID_PHONE_NUMBER = generate_japanese_phone_number()
        INVALID_EMAIL = generate_random_email()
        PHONE_NUMBER = "13100000032"
        EMAIL = "hrtqdwmk@sharklasers.com"
        VERIFY_CODE = "123456"
        DP_Amount = '1'

    # 開發環境配置
    class DevEnv:
        BASE_URL = "https://dev-newplatform.mxsyl.com/zh-cn/login"
        LOGIN_URL = "https://dev-newplatform.mxsyl.com/zh-cn/login"
        REGISTER_URL = "https://uat-newplatform.mxsyl.com/zh-cn/register"
        VALID_USERNAME = "cooper018"
        VALID_PASSWORD = "Dev1234Qwer"
        INVALID_USERNAME_PREFIX = generate_random_username()
        INVALID_PHONE_NUMBER = generate_japanese_phone_number()
        INVALID_EMAIL = generate_random_email()
        PHONE_NUMBER = "13900000001"
        EMAIL = "dev_hrtqdwmk@sharklasers.com"
        VERIFY_CODE = "123456"

    # 生產環境配置
    class ProdEnv:
        BASE_URL = "https://prod-newplatform.mxsyl.com/zh-cn/login"
        LOGIN_URL = "https://prod-newplatform.mxsyl.com/zh-cn/login"
        REGISTER_URL = "https://uat-newplatform.mxsyl.com/zh-cn/register"
        VALID_USERNAME = "prod_cooper005"
        VALID_PASSWORD = "Prod1234Qwer"
        INVALID_USERNAME_PREFIX = generate_random_username()
        INVALID_PHONE_NUMBER = generate_japanese_phone_number()
        INVALID_EMAIL = generate_random_email()           
        PHONE_NUMBER = "13100000029"
        EMAIL = "prod_hrtqdwmk@sharklasers.com"
        VERIFY_CODE = "123456"

# 在類定義完成後設置 CURRENT_ENV 和 config
CURRENT_ENV = getattr(Config, Config.ENV)
config = CURRENT_ENV

if __name__ == "__main__":
    print(f"當前環境: {Config.ENV}")
    print(f"BASE_URL: {config.BASE_URL}")
    print(f"LOGIN_URL: {config.LOGIN_URL}")
    print(f"VALID_USERNAME: {config.VALID_USERNAME}")