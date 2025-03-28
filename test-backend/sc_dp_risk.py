import requests
import json
import os
import sys
from urllib.parse import urljoin

# 添加項目根目錄到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.config import Config, config  # 導入 Config 和 config

json_file_path = "/Users/steven/deepseek/seleium/config/random_data.json"

# 定義全局變數
token = None
orderId = None

# 讀取 token 與 orderId
try:
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        
    token = data.get("sc_token")
    orderId = data.get("orderId")
    if not token:
        raise ValueError("JSON 檔案中缺少 'sc_token' 字段")
    if not orderId:
        raise ValueError("JSON 檔案中缺少 'orderId' 字段")
    
    authorization = f"Bearer {token}"
except FileNotFoundError:
    print(f"錯誤：找不到檔案 {json_file_path}")
except json.JSONDecodeError:
    print("錯誤：JSON 檔案格式無效")
except Exception as e:
    print(f"發生錯誤：{str(e)}")

def dp_risk():
    """
    發送請求取得交易列表，並提取第一筆資料中的 id 值
    """
    if token is None:
        print("錯誤：token 未正確初始化")
        return None

    url = "http://uat-admin-api.mxsyl.com:5012/api/v1/asset/transaction/getlist"
    headers = {"authorization": authorization}
    params = {
        "OrderNum": orderId
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        # print("Request URL:", url)
        # print(f"Response status code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            # print("Response data:", result)
            # 嘗試從回傳資料中提取 id
            try:
                trans_id = result['list'][0]['id']
                print("提取到的 id:", trans_id)
            except (KeyError, IndexError) as e:
                print("無法提取 id:", e)
                trans_id = None
            return trans_id
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"網路請求失敗：{str(e)}")
        return None

def dp_risk1(trans_id):
   
    print("在下一個函式中使用 id:", trans_id)

    if token is None:
        print("錯誤：token 未正確初始化")
        return None

    url = "http://uat-admin-api.mxsyl.com:5012/api/v1/asset/transaction/depositrecorddetail"
    headers = {"authorization": authorization}
    params = {
        "id": trans_id
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        # print("Request URL:", url)
        print(f"Response status code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("Response data:", result)
            # 嘗試從回傳資料中提取 id
            try:
                thirdPartOrderNum = result['thirdPartOrderNum']
                print("提取到的 thirdPartOrderNum:", thirdPartOrderNum)
            except (KeyError, IndexError) as e:
                print("無法提取 id:", e)
                thirdPartOrderNum = None
            return thirdPartOrderNum
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"網路請求失敗：{str(e)}")
        return None

def dp_risk2(thirdPartOrderNum):
   
    print("在下一個函式中使用 id:", thirdPartOrderNum)
    
    if thirdPartOrderNum is None:
        print("沒有有效的 id 可供使用")
        return
    
    url = "http://20.198.224.251:8002/api/v1/deposit/confirm"
    headers = {
        "accept": "text/plain",
        "Content-Type": "application/json-patch+json"
    }
    data = {
        "orderID": thirdPartOrderNum,
        "orderState": 2,
        "timestamp": 0
    }
    json_data = json.dumps(data)
    try:
        response = requests.post(url, headers=headers, data=json_data)
        if response.status_code == 200:
            print(f"請求成功:狀態碼{response.status_code}")
            return response.text
        else:
            print(f"請求失敗，狀態碼 {response.status_code}:")
            print(response.text)
            return None
    except requests.exceptions.RequestException as e:
        print("網路請求發生錯誤:", e)
        return None

def dp_risk3(thirdPartOrderNum):
   
    print("在下一個函式中使用 id:", thirdPartOrderNum)
    
    if thirdPartOrderNum is None:
        print("沒有有效的 id 可供使用")
        return
    
    url = "http://20.198.224.251:8002/api/v1/deposit/notify"
    headers = {
        "accept": "text/plain",
        "Content-Type": "application/json-patch+json"
    }
    data = {
        "orderID": thirdPartOrderNum,
        "timestamp": 0
    }
    json_data = json.dumps(data)
    try:
        response = requests.post(url, headers=headers, data=json_data)
        if response.status_code == 200:
            print(f"請求成功:狀態碼{response.status_code}")
            return response.text
        else:
            print(f"請求失敗，狀態碼 {response.status_code}:")
            print(response.text)
            return None
    except requests.exceptions.RequestException as e:
        print("網路請求發生錯誤:", e)
        return None






if __name__ == "__main__":
    # 先獲取 id
    id_value = dp_risk()
    # 將 id 傳給下一個函式進行處理
    thirdPartOrderNum = dp_risk1(id_value)
    # 將 thirdPartOrderNum 傳給下一個函式進行處理
    dp_risk2(thirdPartOrderNum)
    dp_risk3(thirdPartOrderNum)