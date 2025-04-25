import requests
import json
from requests.auth import HTTPBasicAuth

class TestRailClient:
    def __init__(self, base_url, username, api_key):
        self.base_url = base_url
        self.auth = HTTPBasicAuth(username, api_key)
        self.headers = {
            "Content-Type": "application/json"
        }

    def add_result(self, run_id, case_id, status_id, comment=""):
        url = f"{self.base_url}/index.php?/api/v2/add_result_for_case/{run_id}/{case_id}"
        data = {
            "status_id": status_id,
            "comment": comment
        }

        # 使用 json= 保留中文與 emoji 正確處理
        response = requests.post(
            url,
            headers=self.headers,
            auth=self.auth,
            json=json.loads(json.dumps(data, ensure_ascii=False))
        )

        # ✅ 把 print 移到 response 拿到後
        print(f"回傳內容: {response.text}")

        response.raise_for_status()
        return response.json()
