import datetime # 導入 datetime 模組，用於生成時間戳記
import json # 導入 json 模組，用於讀寫 JSON 檔案
import os # 導入 os 模組，用於處理檔案路徑與目錄操作
import random # 導入 random 模組，用於生成隨機資料
import sys # 導入 sys 模組，用於檢測作業系統類型


class Config:
    """全域配置，包含環境參數、商戶選擇與隨機資料生成方法"""

    # 全域設定，直接在這裡指定要使用的環境與商戶
    ENV = "TestEnv"         # 可選："TestEnv", "ProdEnv"
    MERCHANT = "Merchant1"  # 可選："Merchant1", "Merchant2", "Merchant3", "Merchant4"
    DELAY_SECONDS = 0.5 # 測試步驟間的延遲時間（秒）
    WAIT_TIMEOUT = 10 # Selenium 等待網頁元素的超時時間（秒）

    # 根據作業系統動態設置 ChromeDriver 和隨機資料 JSON 檔案的路徑
    if sys.platform == "win32": # Windows 系統的路徑設置
        CHROMEDRIVER_PATH = r"C:\Users\d1031\新增資料夾\unittest\chormedrive\chromedriver.exe"
        RANDOM_DATA_JSON_PATH = r"C:\Users\d1031\新增資料夾\unittest\config\random_data.json"
    elif sys.platform == "darwin": # macOS 系統的路徑設置
        CHROMEDRIVER_PATH = "/Users/steven/deepseek/seleium/chormedrive/chromedriver"
        RANDOM_DATA_JSON_PATH = "/Users/steven/deepseek/seleium/config/random_data.json"
    elif sys.platform == "linux": # Linux 系統的路徑設置
        CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"
        RANDOM_DATA_JSON_PATH = "/app/config/random_data.json"
    else: # 若作業系統不受支援，拋出異常
        raise RuntimeError("Unsupported OS")

    @staticmethod
    def get_chromedriver_path():
        """返回 ChromeDriver 的路徑"""
        return Config.CHROMEDRIVER_PATH

    @staticmethod
    def get_random_data_json_path():
        """返回隨機資料 JSON 檔案的路徑"""
        return Config.RANDOM_DATA_JSON_PATH

    # 測試環境配置，包含多個商戶的設置
    class TestEnv:
        class MerchantBase:
            """測試環境的商戶基礎類，定義共用的 API 端點與帳戶資料"""
            # 後台相關
            SET_UP_API = "/v1/api/auth/setup?s=eSGwvL70s4%2F1Uc8jOs%2BEdjTTY7ABjG%2BCJta8QmZOtHULSAbatME47%2Bt1QY8ktqW9wbPxFmh7huwAApMflnR6PtjBqoTz%2FCmzADuNcMhdNxr0jRR5TfVyi%2FmSDnEPwGpNwpfwwKllYmSPqufI9RpgwuKI112fHbrG7jFq4F0spPZIxdC2aenXt5SwdPQv8D4xc2yw%2BOwRpttIaMKKo8xXiaqxrr52UfIfQyJCPfdjS0dIPtivex81oo6813jBPMjzNMMcmaJw4efnfDQPG6xfERAdTf8OdRj1XrNNFjTcP3rIg%2Bp89ObbZ7plal5xoQovmdF7JKiZi85RQzuuV%2BQgEg%3D%3D"
            public_key_content = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA1lcU5lRpSOqdLicIimSso8wSCTDWdtv3BXGeixALS+bcqOMmV2Tm5F5O3sOAku/a+XxeC+yXkaVrCXpgsl0LEPGVnqO5XoVs4LTeo0zwCJQ+H7TN1ZlqkpfFCL7Mn1+dUXvy+N2p5ijlTZiFsfetc+Jr/JH2Zj62nnc/Vpxne0RsKLwh4Mwp6i/BSv2H9xurablJpz3GPb0qoTniCuxzXvCR9h2tFfbCNacrdpOFVW/A8g27g5em+uqjVB5xAhM1pj0b5PlgR6Oyn5c5mmK1waBx/P+NZJRmGrDbHZMq07v3ma9LTOCGGoG90ReYHxVFRSlAzfl5NGF9nrkfZW4skQIDAQAB"
            BASE_SC_URL = "http://uat-admin-api.mxsyl.com:5012" # 後台基礎網址
            SC_LOGIN_API = "/api/v1/admin/auth/login" # 後台登入 API
            AES_KEY_API = "/api/v1/admin/auth/getpasswordencryptkey" # 獲取密碼加密金鑰

            # 前台API
            LOGIN_API = "/v1/member/auth/loginbyname" # 前台登入 API
            DEPOSIT_API = "/v1/asset/deposit/currency" # 存款 API
            # 後台帳密
            SC_USERNAME = "QA006" # 後台測試帳號
            SC_PASSWORD = "QA006" # 後台測試密碼
            # 驗證碼與金額
            VERIFY_CODE = "123456" # 測試用驗證碼
            DP_Amount = '100' # 測試用存款金額/

        class Merchant1(MerchantBase):
            """測試環境的 Merchant1 配置，繼承 MerchantBase"""
            BASE_URL = "https://uat-newplatform.mxsyl.com" # 前台基礎網址
            LOGIN_URL = "https://uat-newplatform.mxsyl.com/zh-cn/login" # 登入頁面網址
            REGISTER_URL = "https://uat-newplatform.mxsyl.com/zh-cn/register" # 註冊頁面網址

            PHONE_NUMBER = "13100000021" # 測試用手機號
            EMAIL = "hrtqdwmk@sharklasers.com" # 測試用電子郵件
            VALID_USERNAME = "cooper005" # 有效測試用戶名
            VALID_DP_USERNAME = "cooper024" # 存款測試用戶名
            VALID_DP_NAME = "测试" # 存款測試名稱
            VALID_PASSWORD = "1234Qwer" # 測試密碼

        class Merchant2(MerchantBase):
            SET_UP_API = "/v1/api/auth/setup?s=FK%2F8U1UoR1pvYyPGRc9Hf1UtH5CbChSdUcQi6LW5sHQUTdCvKymW1Pf7GbIRFka3v6oLkenl613jzTPscfyMupzFB6dG6ev7FC26xlxui%2FcTXAtpX9zc6uKG8yy%2F13ifghSFHvgR0Ya2g9A6hbLNwDcKcTY%2BAKKImQ%2BiDHHQXPs3eouxU5EECjcBGB0iDZqI0k0mZx1FuwaNzvB%2FvpHCsLpEqxhZCea9EVXOcLADGQ%2B4P9qU5zuwEMImvRsc8wREm56JT9ACcmvsE03QbDJKDsmPAqbKvKzFK59LRiXz%2BAvMYI5%2BBgegU5VFQu6NpyESqB81rKwyMONDcjBhqIRHmQ%3D%3D"
            BASE_URL = "https://uat2-newplatform.mxsyl.com/"
            LOGIN_URL = "https://uat2-newplatform.mxsyl.com/zh-cn/login"
            REGISTER_URL = "https://uat2-newplatform.mxsyl.com/zh-cn/register"

            PHONE_NUMBER = ""
            EMAIL = ""
            VALID_USERNAME = "cooper023"
            VALID_DP_USERNAME = "cooper023"
            VALID_DP_NAME = "测试" # 存款測試名稱
            VALID_PASSWORD = "1234Qwer"

        class Merchant5(MerchantBase):

            BASE_URL = "https://uat5-newplatform.mxsyl"
            LOGIN_URL = "https://uat5-newplatform.mxsyl/zh-cn/login"
            REGISTER_URL = "https://uat5-newplatform.mxsyl/zh-cn/register"

            PHONE_NUMBER = ""
            EMAIL = ""
            VALID_USERNAME = ""
            VALID_DP_USERNAME = ""
            VALID_PASSWORD = ""
  
        class Merchant7(MerchantBase):
            BASE_URL = "https://uat7-newplatform.mxsyl.com"
            LOGIN_URL = "https://uat7-newplatform.mxsyl.com/zh-cn/login"
            REGISTER_URL = "https://uat7-newplatform.mxsyl.com/zh-cn/register"

            PHONE_NUMBER = ""
            EMAIL = ""
            VALID_USERNAME = ""
            VALID_DP_USERNAME = ""
            VALID_PASSWORD = ""
        
    # 正式環境配置：拆分為 4 個商戶
    class ProdEnv:
        class MerchantBase:
            """正式環境的商戶基礎類，定義共用的 API 端點與帳戶資料"""
            # 後台相關
            SET_UP_API = "/v1/api/auth/setup?s=ftR3rOe39MF%2Fz7uj0TAxv%2B8f4%2FKCIfnsJgyah1%2FhPlBq3R0BmTbbGxUUdKpBtu3kPzg%2B9ALkFhSVMyxYTtywOMiM3k%2BI06gDTm3Ch2YlKTbUOX%2FDZkbVzO7nFhXPSqXpdPWbDCMCRN9Antj6XIoQWMpFapzQs2GUt7EOxLDhMg30zMxFno4S8%2BkjIEwy90famJExmRTKX0MJP%2FSbiJETJHklQVGKwP94c1PvA4CUoIwtF7YvfRjDwoz1HPaTKmzTcgXsr95WQPPQ0RHF4tMKyIRvPQya%2BR4pV4lRI2Kr7pq6Fn12Zq4Rj4M7uiAGdh8PLnUpuPS7Hw9LkF3c3IRpWw%3D%3D"
            public_key_content = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoTgcVORkxBPRQJimRKTUHrSS+vTBzbAm8l6bwaFqr1Mya/pjsHrUPCErJnchMfmfgEBFrsfX5/FLGfXvKFT//F949jgcl3My2oGCOk4dTh+zpp16q8e0qoOG5JtKmQjs2W+s2sAp2Xsk4hMfRY9ZzxsSORjS6YYvgLb0TwbLXZ1GAHhwJSVJS38AUqJH2Z0ng7xzDAklEqLfcP+99PBVau0iqRBEypUsJqcTPXTJMQw0wZg3Frci0SuOhTexmG7NzVhHZIV0cp07czo8lp8+2YvC14iaPwn2xB4dVXNtIILQFXorfNS9U+IO5uL0Y432GeWax1tVXrl6jowihrd1nwIDAQAB"
            BASE_SC_URL = "https://www.gobackend.xyz/" # 後台基礎網址
            SC_LOGIN_API = "/api/v1/admin/auth/login" # 後台登入 API
            AES_KEY_API = "/api/v1/admin/auth/getpasswordencryptkey" # 獲取密碼加密金鑰 API

            # 前台API
            LOGIN_API = "/v1/member/auth/loginbyname" # 前台登入 API
            DEPOSIT_API = "/api/v1/asset/deposit/currency" # 存款 API
            # 後台帳密
            SC_USERNAME = "Tech_QA_Tester" # 後台測試帳號
            SC_PASSWORD = "123@Tech_QA_Tester" # 後台測試密碼
            # 驗證碼與金額
            VERIFY_CODE = "123456" # 測試用驗證碼
            DP_Amount = '100' # 測試用存款金額

        class Merchant1(MerchantBase):
            """正式環境的 Merchant1 配置，繼承 MerchantBase"""
            BASE_URL = "https://www.lt.com" # 前台基礎網址
            LOGIN_URL = "https://www.lt.com/zh-cn/login" # 登入頁面網址
            REGISTER_URL = "https://www.lt.com/zh-cn/register" # 註冊頁面網址

            PHONE_NUMBER = "18700000005" # 測試用手機號
            EMAIL = "" # 電子郵件
            VALID_DP_NAME = "测试" # 存款測試名稱
            VALID_USERNAME = "QA_M1_05" # 有效測試用戶名
            VALID_DP_USERNAME = "QA_M1_05" # 存款測試用戶名
            VALID_PASSWORD = "QA_M1_05" # 測試密碼

        class Merchant2(MerchantBase):
            BASE_URL = "https://www.mrcatgo.com"
            LOGIN_URL = "https://www.mrcatgo.com/zh-cn/login"
            REGISTER_URL = "https://www.mrcatgo.com/zh-cn/register"

            PHONE_NUMBER = ""
            EMAIL = ""
            VALID_USERNAME = ""
            VALID_DP_USERNAME = ""
            VALID_PASSWORD = ""

        class Merchant5(MerchantBase):
            BASE_URL = "https://www.letou1.vip"
            LOGIN_URL = "https://www.letou1.vip/zh-cn#login"
            REGISTER_URL = "https://www.letou1.vip/zh-cn#register"

            PHONE_NUMBER = ""
            EMAIL = ""
            VALID_USERNAME = ""
            VALID_DP_USERNAME = ""
            VALID_PASSWORD = ""

        class Merchant7(MerchantBase):
            BASE_URL = "https://vwin158.com"
            LOGIN_URL = "https://vwin158.com/zh-cn/login"
            REGISTER_URL = "https://vwin158.com/zh-cn/register"

            PHONE_NUMBER = ""
            EMAIL = ""
            VALID_USERNAME = ""
            VALID_DP_USERNAME = ""
            VALID_PASSWORD = ""


    @classmethod
    def get_current_config(cls):
        """根據全域 ENV 與 MERCHANT 參數取得當前配置"""
        env_class = getattr(cls, cls.ENV) # 獲取環境類（如 TestEnv 或 ProdEnv）
        merchant_config = getattr(env_class, cls.MERCHANT) # 獲取商戶配置（如 Merchant1）
        # print("⚙️ 目前選擇的環境：", Config.ENV)
        # print("⚙️ 目前選擇的商戶：", Config.MERCHANT)
        return merchant_config

    @staticmethod
    def generate_random_username():
        """生成隨機用戶名，格式為 QAM1 + 時間戳記"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S") # 獲取當前時間戳記
        random_username = f"QAM1{timestamp}" # 組合用戶名
        save_random_data_to_json({"random_username": random_username}) # 儲存到 JSON
        return random_username

    @staticmethod
    def generate_japanese_phone_number():
        """生成隨機日本手機號，格式為 070/080/090 + 8 位數字"""
        prefixes = ['070', '080', '090'] # 日本手機號前綴
        prefix = random.choice(prefixes) # 隨機選擇前綴
        remaining_digits = ''.join(str(random.randint(1, 9)) for _ in range(8)) # 生成 8 位隨機數字
        japanese_phone = prefix + remaining_digits # 組合手機號
        save_random_data_to_json({"japanese_phone_number": japanese_phone}) # 儲存到 JSON
        return japanese_phone

    @staticmethod
    def generate_random_email():
        """生成隨機電子郵件，格式為 隨機用戶名@gmail.com"""
        username = Config.generate_random_username() # 獲取隨機用戶名
        email = f"{username}@gmail.com" # 組合電子郵件
        save_random_data_to_json({"random_email": email}) # 儲存到 JSON
        return email

def save_random_data_to_json(data):
    """將隨機生成的資料儲存到 JSON 檔案"""
    json_path = Config.get_random_data_json_path() # 獲取 JSON 檔案路徑
    if os.path.exists(json_path): # 如果檔案存在，讀取現有資料
        with open(json_path, 'r') as f:
            existing_data = json.load(f)
    else: # 如果檔案不存在，初始化為空字典
        existing_data = {}
    existing_data.update(data) # 更新資料
    with open(json_path, 'w') as f: # 寫入更新後的資料，確保支援非 ASCII 字元（如中文）
        json.dump(existing_data, f, indent=4, ensure_ascii=False)
    print(f"隨機資料已儲存到: {json_path}") # 輸出儲存路徑


# 確保隨機資料 JSON 檔案的目標目錄存在，若不存在則創建
os.makedirs(os.path.dirname(Config.get_random_data_json_path()), exist_ok=True)



if __name__ == "__main__":
    config = Config.get_current_config()  
    print(f"當前環境: {Config.ENV}")
    print(f"目前商戶: {Config.MERCHANT}")
    print(f"BASE_URL: {config.BASE_URL}")
    print(f"LOGIN_URL: {config.LOGIN_URL}")
    print(f"VALID_USERNAME: {config.VALID_USERNAME}")
