# 處理存款風險審核流程，包含提取交易 ID、第三方訂單號、確認及通知 API 調用
import requests
import json
import os
import sys
from urllib.parse import urljoin

# 添加項目根目錄到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.config import Config
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
json_file_path = Config.RANDOM_DATA_JSON_PATH  # ✅ 全域不動態化

class DepositRiskProcessor:
    def __init__(self, json_path=json_file_path):
        self.json_path = json_path
        self.token = None
        self.order_id = None
        self.authorization = None
        self._load_token_and_order_id()

    def _load_token_and_order_id(self):
        try:
            with open(self.json_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            self.token = data.get("sc_token")
            self.order_id = data.get("orderId")
            if not self.token:
                raise ValueError("JSON 檔案中缺少 'sc_token' 字段")
            if not self.order_id:
                raise ValueError("JSON 檔案中缺少 'orderId' 字段")

            self.authorization = f"Bearer {self.token}"
        except Exception as e:
            print(f"❌ 初始化錯誤：{str(e)}")

    def dp_risk(self):
        cfg = Config.get_current_config()
        url = urljoin(cfg.BASE_SC_URL, "/api/v1/asset/transaction/getlist")
        headers = {"authorization": self.authorization}
        params = {
            "Category": "Deposit",
            "TenantId": "-1",
            "OrderNum": self.order_id
        }
        try:
            response = requests.get(url, params=params, headers=headers)
            if response.status_code == 200:
                result = response.json()
                trans_id = result['list'][0]['id']
                print("✅ 提取到的交易 ID:", trans_id)
                return trans_id
            else:
                print(f"❌ getlist 請求失敗: {response.status_code}")
        except Exception as e:
            print(f"❌ getlist 發生錯誤: {str(e)}")
        return None

    def dp_risk1(self, trans_id):
        cfg = Config.get_current_config()
        url = urljoin(cfg.BASE_SC_URL, "/api/v1/asset/transaction/depositrecorddetail")
        headers = {"authorization": self.authorization}
        params = {"id": trans_id}
        try:
            response = requests.get(url, params=params, headers=headers)
            if response.status_code == 200:
                result = response.json()
                third_order_num = result['thirdPartOrderNum']
                print("✅ 取得 thirdPartOrderNum:", third_order_num)
                return third_order_num
            else:
                print(f"❌ depositrecorddetail 請求失敗: {response.status_code}")
        except Exception as e:
            print(f"❌ depositrecorddetail 發生錯誤: {str(e)}")
        return None

    def dp_risk2(self, third_order_num):
        # ✅ 保留固定 IP，不動用 cfg
        url = "http://20.198.224.251:8002/api/v1/deposit/confirm"
        headers = {
            "accept": "text/plain",
            "Content-Type": "application/json-patch+json"
        }
        data = {
            "orderID": third_order_num,
            "orderState": 2,
            "timestamp": 0
        }
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            if response.status_code == 200:
                print("✅ 確認成功 (confirm):", response.text)
                return response.text
            else:
                print(f"❌ 確認失敗: {response.status_code}")
                print(response.text)
        except Exception as e:
            print(f"❌ confirm 發生錯誤: {str(e)}")
        return None

    def dp_risk3(self, third_order_num):
        # ✅ 保留固定 IP，不動用 cfg
        url = "http://20.198.224.251:8002/api/v1/deposit/notify"
        headers = {
            "accept": "text/plain",
            "Content-Type": "application/json-patch+json"
        }
        data = {
            "orderID": third_order_num,
            "timestamp": 0
        }
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            if response.status_code == 200:
                print("✅ 通知成功 (notify):", response.text)
                return response.text
            else:
                print(f"❌ 通知失敗: {response.status_code}")
                print(response.text)
        except Exception as e:
            print(f"❌ notify 發生錯誤: {str(e)}")
        return None

    def run(self):
        trans_id = self.dp_risk()
        if not trans_id:
            print("❌ 無法取得交易 ID，流程中止")
            return
        third_order_num = self.dp_risk1(trans_id)
        if not third_order_num:
            print("❌ 無法取得 thirdPartOrderNum，流程中止")
            return
        self.dp_risk2(third_order_num)
        self.dp_risk3(third_order_num)


if __name__ == "__main__":
    processor = DepositRiskProcessor()
    processor.run()
