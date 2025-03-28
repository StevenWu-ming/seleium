import requests
import json
import os
import sys
from urllib.parse import urljoin
# 添加項目根目錄到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.config import Config , config  # 導入 Config 和 config

json_file_path = "/Users/steven/deepseek/seleium/config/random_data.json"

# 定義 token 為全局變數
token = None
# 讀取 token
try:
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        
    # 提取 token 值
    token = data.get("token")
    if not token:
        raise ValueError("JSON 檔案中缺少 'token' 字段")
    
    # 構建 authorization 字符串
    authorization = f"Bearer {token}"
    # print("authorization:", authorization)  # 確認 token 是否正確提取
except FileNotFoundError:
    print(f"錯誤：找不到檔案 {json_file_path}")
except json.JSONDecodeError:
    print("錯誤：JSON 檔案格式無效")
except Exception as e:
    print(f"發生錯誤：{str(e)}")

class deposit_api():
    def deposit():
        if token is None:
            print("錯誤：token 未正確初始化")
            return None

        url = urljoin(config.BASE_URL, config.DEPOSIT_API)
        # print("Request URL:", url)  # 打印請求的 URL 以進行調試

        headers = {
            "authorization": authorization,
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
        }
        payload = {
            "amount": 100,
            "currency": "CNY",
            "paymentCode": "C2CBankTransfer",
            "actionType": 1,
            "userName": "小明",
            "bankCode": "CMBC",
            "activityNo": "2607512053222021"
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            # print(authorization)
            print(url)
            print(f"Response status code: {response.status_code}")  # 打印狀態碼
            if response.status_code == 200:
                result = response.json()
                print("Response data:", result)  # 打印成功時的響應數據
                return result
            else:
                print(f"Error {response.status_code}: {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"網路請求失敗：{str(e)}")
            return None

    # 執行並檢查結果
    result = deposit()
    # if result is not None:
    #     print("最終結果:", result)
    # else:
    #     print("請求未成功，沒有返回結果")
