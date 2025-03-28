import requests
import json
import os
import sys
from urllib.parse import urljoin
from requests.exceptions import RequestException

# 添加項目根目錄到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.config import Config, config  # 導入 Config 和 config

json_file_path = "/Users/steven/deepseek/seleium/config/random_data.json"

def load_encrypt_key(json_path: str = json_file_path) -> tuple[str, str]:
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data["key"], data["encrypted"]

class AdminAPIClient:
    """用於處理管理員API請求的類別"""
    
    def __init__(self, base_url=config.BASE_SC_URL):
        """初始化API客戶端
        
        Args:
            base_url (str): API的基本URL，預設為UAT環境
        """
        self.base_url = base_url
        self.session = requests.Session()
        self.headers = {
            'Content-Type': 'application/json'
        }

    def login(self, username=config.SC_USERNAME, 
             password=load_encrypt_key()[1], 
             password_key=load_encrypt_key()[0]
             ):
        """執行管理員登錄
        
        Args:
            username (str): 用戶名，預設為"QA006"
            password (str): 密碼，預設為加密後的值
            password_key (str): 密碼密鑰
            
        Returns:
            dict: 包含狀態碼和響應數據的字典
            
        Raises:
            RequestException: 當請求失敗時拋出
        """
        endpoint = config.SC_LOGIN_API
        url = urljoin(self.base_url, endpoint)
        
        payload = {
            "userName": username,
            "password": password,
            "passwordKey": password_key
        }
        
        try:
            response = self.session.post(
                url,
                json=payload,
                headers=self.headers,
                verify=False
            )
            response.raise_for_status()
            return {
                "status_code": response.status_code,
                "response": json.loads(response.text)
            }
        except RequestException as e:
            raise RequestException(f"Login failed: {str(e)}")

    def __enter__(self):
        """支援上下文管理器"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """關閉session"""
        self.session.close()

if __name__ == "__main__":
    client = AdminAPIClient()
    try:
        result = client.login()
        print(f"Status Code: {result['status_code']}")
        print(f"Response: {result['response']}")
        
        # 取得回傳的 token，並存入 random_data.json，儲存名稱為 sc_token
        if isinstance(result.get("response"), dict):
            token_value = result["response"].get("token")
            if token_value:
                # 讀取現有的 JSON 檔案
                if os.path.exists(json_file_path):
                    with open(json_file_path, "r", encoding="utf-8") as f:
                        try:
                            existing_data = json.load(f)
                        except json.JSONDecodeError:
                            existing_data = {}
                else:
                    existing_data = {}
                # 更新 sc_token 欄位
                existing_data["sc_token"] = token_value
                # 將更新後的資料寫回 JSON 檔案
                with open(json_file_path, "w", encoding="utf-8") as f:
                    json.dump(existing_data, f, indent=4, ensure_ascii=False)
                print(f"sc_token 已儲存: {token_value}")
            else:
                print("回傳結果中無 token")
    except RequestException as e:
        print(f"An error occurred: {e}")
