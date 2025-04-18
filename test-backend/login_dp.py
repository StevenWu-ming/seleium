import time
import json
import os
import sys
from login_api import LoginAPI
from deposit_api import deposit_api

# 添加項目根目錄到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.config import Config  # 導入 Config

json_file_path = Config.RANDOM_DATA_JSON_PATH  # ✅ 全域設定保留

def read_token_from_json():
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get("token")
    except Exception as e:
        print(f"❌ Failed to read token: {e}")
        return None

def main(userName=None, user_name=None, password=None, amount=None):
    print(f"⚙️ 目前選擇的環境： {Config.ENV}")
    print(f"⚙️ 目前選擇的商戶： {Config.MERCHANT}")
    print("🔹 Step 1: Running setup API...")
    LoginAPI.run_setup_api()

    time.sleep(2)

    print("🔹 Step 2: Logging in...")
    login_result = LoginAPI.login(userName=userName, password=password)

    if not login_result or not isinstance(login_result.get("data"), dict):
        print("❌ No token returned from login, aborting.")
        return

    token = login_result["data"].get("token")
    time.sleep(2)  # 確保寫入完成

    json_token = read_token_from_json()
    if json_token == token:
        print("✅ Token successfully written to JSON. Proceeding to deposit...")
        deposit_api.deposit(user_name=user_name, amount=amount)
    else:
        print("❌ Token mismatch or not written correctly. Aborting deposit.")

if __name__ == "__main__":
    main()
