import time
import json
from login_api import LoginAPI
from deposit_api import deposit_api

json_file_path = "/Users/steven/deepseek/seleium/config/random_data.json"

def read_token_from_json():
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get("token")
    except Exception as e:
        print(f"❌ Failed to read token: {e}")
        return None

if __name__ == "__main__":
    print("🔹 Step 1: Running setup API...")
    LoginAPI.run_setup_api()

    time.sleep(2)

    print("🔹 Step 2: Logging in...")
    token = LoginAPI.login()

    if not token:
        print("❌ No token returned from login, aborting.")
    else:
        print(f"✅ Token received: {token}")

        # 等待確保 token 寫入完成
        time.sleep(2)

        # 確認 token 寫入成功
        json_token = read_token_from_json()
        if json_token == token:
            print("✅ Token successfully written to JSON. Proceeding to deposit...")
            deposit_api.deposit()
        else:
            print("❌ Token mismatch or not written correctly. Aborting deposit.")
