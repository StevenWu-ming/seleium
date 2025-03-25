import requests
import json
import os
import sys
from urllib.parse import urljoin
from requests.exceptions import RequestException

# 添加項目根目錄到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.config import Config, config  # 導入 Config 和 config


file_path = "/Users/steven/deepseek/seleium/config/random_data.json"


class AdminAPIClient:
    """用於處理管理員API請求的類別"""
    
    def __init__(self, base_url="http://uat-admin-api.mxsyl.com:5012"):
        """初始化API客戶端
        
        Args:
            base_url (str): API的基本URL，預設為UAT環境
        """
        self.base_url = base_url
        self.session = requests.Session()
        self.headers = {
            'Content-Type': 'application/json'
        }

    def login(self, username="QA006", 
             password="7FZY2ALzoTxlNGMAfGX4Wg==", 
             password_key="eda8ac3b97a947cc96863548cba26004"):
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
        endpoint = "/api/v1/admin/auth/login"
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

# 使用示例
if __name__ == "__main__":
    # 方法1：普通使用
    client = AdminAPIClient()
    try:
        result = client.login()
        print(f"Status Code: {result['status_code']}")
        print(f"Response: {result['response']}")
    except RequestException as e:
        print(f"An error occurred: {e}")
