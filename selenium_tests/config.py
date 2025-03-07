# selenium_tests/config.py

import os

class Config:
    # 通用配置
    CHROMEDRIVER_PATH = "/Users/steven/deepseek/chromedriver"  # ChromeDriver 路徑，根據需要調整
    DELAY_SECONDS = 2
    WAIT_TIMEOUT = 10  # WebDriverWait 超時時間

    # 測試環境配置
    class TestEnv:
        BASE_URL = "https://uat-newplatform.mxsyl.com/zh-cn/login"
        LOGIN_URL = "https://uat-newplatform.mxsyl.com/zh-cn/login"
        VALID_USERNAME = "cooper005"
        VALID_PASSWORD = "1234Qwer"
        INVALID_USERNAME_PREFIX = "random"
        PHONE_NUMBER = "13100000001"
        EMAIL = "hrtqdwmk@sharklasers.com"
        VERIFY_CODE = "123456"

    # 開發環境配置
    class DevEnv:
        BASE_URL = "https://dev-newplatform.mxsyl.com/zh-cn/login"
        LOGIN_URL = "https://dev-newplatform.mxsyl.com/zh-cn/login"
        VALID_USERNAME = "dev_cooper005"
        VALID_PASSWORD = "Dev1234Qwer"
        INVALID_USERNAME_PREFIX = "dev_random"
        PHONE_NUMBER = "13900000001"
        EMAIL = "dev_hrtqdwmk@sharklasers.com"
        VERIFY_CODE = "123456"

    # 生產環境配置
    class ProdEnv:
        BASE_URL = "https://prod-newplatform.mxsyl.com/zh-cn/login"
        LOGIN_URL = "https://prod-newplatform.mxsyl.com/zh-cn/login"
        VALID_USERNAME = "prod_cooper005"
        VALID_PASSWORD = "Prod1234Qwer"
        INVALID_USERNAME_PREFIX = "prod_random"
        PHONE_NUMBER = "13800000001"
        EMAIL = "prod_hrtqdwmk@sharklasers.com"
        VERIFY_CODE = "123456"

    # 根據環境變數選擇環境
    ENV = os.getenv("TEST_ENV", "TestEnv")

# 在類定義完成後設置 CURRENT_ENV 和 config
CURRENT_ENV = getattr(Config, Config.ENV)
config = CURRENT_ENV

if __name__ == "__main__":
    print(f"當前環境: {Config.ENV}")
    print(f"BASE_URL: {config.BASE_URL}")
    print(f"LOGIN_URL: {config.LOGIN_URL}")
    print(f"VALID_USERNAME: {config.VALID_USERNAME}")