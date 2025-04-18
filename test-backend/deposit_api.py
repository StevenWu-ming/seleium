import requests
import json
import os
import sys
from login_api import LoginAPI
from urllib.parse import urljoin
# 添加項目根目錄到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.config import Config  # 導入 Config 和 config

config = Config.get_current_config()



class deposit_api():
    @staticmethod
    def deposit(user_name=None, amount=None):
        user_name = user_name or config.VALID_DP_NAME
        amount = amount or config.DP_Amount

        json_file_path = Config.RANDOM_DATA_JSON_PATH
        
        try:
            with open(json_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            token = data.get("token")
            if not token:
                print("錯誤：token 缺失")
                return None
            authorization = f"Bearer {token}"
        except Exception as e:
            print(f"❌ 讀取 token 發生錯誤: {str(e)}")
            return None

        url = urljoin(config.BASE_URL, config.DEPOSIT_API)
        headers = {
            "authorization": authorization,
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
        }
        payload = {
            "amount": amount,
            "currency": "CNY",
            "paymentCode": "C2CBankTransfer",
            "actionType": 1,
            "userName": user_name,
            "bankCode": "CMBC",
            "activityNo": "2607512053222021"
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            # print(url)
            print(f"Response status code: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                # print("Response data:", result)
                
            if result.get("success") and result.get("data"):
                order_id = result["data"].get("orderId")
                if order_id:
                    # 讀取現有 JSON 檔案
                    if os.path.exists(json_file_path):
                        with open(json_file_path, "r", encoding="utf-8") as f:
                            try:
                                existing_data = json.load(f)
                            except json.JSONDecodeError:
                                existing_data = {}
                    else:
                        existing_data = {}

                    # 更新 orderId
                    existing_data["orderId"] = order_id

                    # 寫入 JSON 檔案
                    with open(json_file_path, "w", encoding="utf-8") as f:
                        json.dump(existing_data, f, indent=4, ensure_ascii=False)
                    
                    print(f"🔹 orderId 更新為: {order_id}")
                else:
                    print("⚠️ 回傳資料中未包含 orderId")

                return result
            else:
                print(f"Error {response.status_code}: {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"網路請求失敗：{str(e)}")
            return None


if __name__ == "__main__":
    # LoginAPI.run_setup_api()
    # LoginAPI.login()
    deposit_api.deposit()
