import requests
import json
import os
import sys
from urllib.parse import urljoin

# 添加項目根目錄到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.config import config

json_file_path = "/Users/steven/deepseek/seleium/config/random_data.json"

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
        url = "http://uat-admin-api.mxsyl.com:5012/api/v1/asset/transaction/getlist"
        headers = {"authorization": self.authorization}
        params = {"OrderNum": self.order_id}
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
        url = "http://uat-admin-api.mxsyl.com:5012/api/v1/asset/transaction/depositrecorddetail"
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
