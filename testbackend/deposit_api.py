# 提供存款 API 調用功能，處理用戶存款請求，更新訂單 ID 至 JSON 文件
import requests
import json
import os
import sys
from login_api import LoginAPI
from urllib.parse import urljoin

# 添加項目根目錄到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.config import Config  # 導入 Config
import logging

# 設置日誌文件路徑為 selenium_tests/test_log.log
log_dir = os.path.dirname(__file__)  # 獲取當前腳本所在目錄 (selenium_tests)
log_file = os.path.join(log_dir, 'test_log.log')  # 直接放在 selenium_tests 根目錄
# 配置日誌，調整級別為 INFO
logging.basicConfig(
    level=logging.INFO,  # 改為 INFO 級別
    format='%(asctime)s - %(levelname)s - [%(name)s] %(message)s',
    handlers=[
        logging.FileHandler(log_file, mode='w'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
class deposit_api():

    @staticmethod
    
    def deposit(user_name=None, amount=None):
        cfg = Config.get_current_config()
       
        user_name = user_name or cfg.VALID_DP_NAME
        amount = amount or cfg.DP_Amount

        json_file_path = Config.RANDOM_DATA_JSON_PATH  # 此為全域變數，保留不動

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

        url = urljoin(cfg.BASE_URL, cfg.DEPOSIT_API)
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
            data = response.json().get("data", {})
            print(f"回傳狀態碼: {response.status_code}")
            print(f"✅ 充值金額: {data.get('amount')}")
            print(f"✅ 銀行名稱: {data.get('bankInfo', {}).get('bankName')}")
            print(f"✅ 銀行帳號: {data.get('bankInfo', {}).get('bankAccountNumber')}")

            result = None  # ✅ 保護避免 result 未定義錯誤

            if response.status_code == 200:
                result = response.json()

            if result and result.get("success") and result.get("data"):
                order_id = result["data"].get("orderId")
                if order_id:
                    if os.path.exists(json_file_path):
                        with open(json_file_path, "r", encoding="utf-8") as f:
                            try:
                                existing_data = json.load(f)
                            except json.JSONDecodeError:
                                existing_data = {}
                    else:
                        existing_data = {}

                    existing_data["orderId"] = order_id

                    with open(json_file_path, "w", encoding="utf-8") as f:
                        json.dump(existing_data, f, indent=4, ensure_ascii=False)

                    print(f"🔹 orderId 更新為: {order_id}")
                else:
                    print("⚠️ 回傳資料中未包含 orderId")

                return result
            else:
                print(f"錯誤 {response.status_code}: {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"網路請求失敗：{str(e)}")
            return None


if __name__ == "__main__":
    # LoginAPI.run_setup_api()
    # LoginAPI.login()
    deposit_api.deposit()
