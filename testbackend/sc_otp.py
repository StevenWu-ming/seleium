import requests
import json
import os
import sys
from urllib.parse import urljoin


# 添加項目根目錄到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.config import Config
from .sc_login_aeskey_api import run_admin_login_workflow

json_file_path = Config.RANDOM_DATA_JSON_PATH
run_admin_login_workflow()
class DepositRiskProcessor:
    pass
    def __init__(self, json_path=json_file_path):
        self.json_path = json_path
        self.authorization = None
        self._load_token_and_order_id()

    def _load_token_and_order_id(self):
        try:
            with open(self.json_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            self.token = data.get("sc_token")
            if not self.token:
                raise ValueError("JSON 檔案中缺少 'sc_token' 字段")
            self.authorization = f"Bearer {self.token}"
        except Exception as e:
            print(f"❌ 初始化錯誤：{str(e)}")

    def otp(self):
        cfg = Config.get_current_config()
        url = urljoin(cfg.BASE_SC_URL, "/api/v1/resource/otpmanage/getlist")
        headers = {"authorization": self.authorization}
        params = {
            "TenantId": "1",
            "Page": "1",
            "PageSize": 5
        }
        try:
            response = requests.get(url, params=params, headers=headers)
            if response.status_code == 200:
                result = response.json()
                # 過濾 mobileNo 為 +8613100****** 的記錄
                target_mobile = cfg.PHONE_OTP
                verify_codes = [item["verifyCode"] for item in result.get("list", []) if item["mobileNo"] == target_mobile]
                if verify_codes:
                    # 印出 verifyCode 值
                    for code in verify_codes:
                        print(code)
                else:
                    print(f"❌ 沒有找到 mobileNo 為 {target_mobile} 的記錄")
                return verify_codes  # 回傳 verifyCode 列表
            else:
                print(f"❌ getlist 請求失敗: {response.status_code}")
        except Exception as e:
            print(f"❌ getlist 發生錯誤: {str(e)}")
        return []

    def run(self):
        return self.otp()  # 修正筆誤：selfsubjec -> self

if __name__ == "__main__":
    processor = DepositRiskProcessor()
    processor.run()