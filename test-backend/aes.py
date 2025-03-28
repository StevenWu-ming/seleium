from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
import sys
import os
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.config import Config, config  # 導入 Config 和 config

file_path = "/Users/steven/deepseek/seleium/config/random_data.json"


# 從 random_data.json 讀取 encyptKey 的函數
def load_encrypt_key(json_path: str) -> str:
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data["encyptKey"]

# 將密文存入 random_data.json 的函數
def save_encrypted_to_json(json_path: str, encrypted: str):
    # 讀取現有的 JSON 文件
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 添加密文到 JSON 數據中（假設你想用 "encrypted" 作為鍵）
    data["encrypted"] = encrypted
    
    # 將更新後的數據寫回文件
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 定義全局參數
PLAINTEXT = config.SC_PASSWORD  # 從 config.py 獲取明文
JSON_PATH = "/Users/steven/deepseek/seleium/config/random_data.json"
KEY = load_encrypt_key(JSON_PATH)  # 從 random_data.json 獲取密鑰


class encrypt_by_ae:
    def encrypt_by_aes(plaintext: str, key: str) -> str:
        """
        使用 AES-128 ECB 模式加密明文，並返回 Base64 編碼的密文。
        
        參數:
            plaintext (str): 要加密的明文，例如 "QA006"。
            key (str): 加密密鑰，例如 "csexp3EsVWE7nEj3"（16 字節）。
        
        返回:
            str: Base64 編碼的密文。
        """
        # 確保密鑰是 16 字節（AES-128）
        key_bytes = key.encode('utf-8')  # 將密鑰轉為 UTF-8 字節
        if len(key_bytes) != 16:
            raise ValueError("密鑰長度必須為 16 字節 (128 位)")

        # 將明文轉為字節
        plaintext_bytes = plaintext.encode('utf-8')

        # 初始化 AES 加密器（ECB 模式）
        cipher = AES.new(key_bytes, AES.MODE_ECB)

        # 應用 PKCS7 填充（塊大小為 16 字節）
        padded_bytes = pad(plaintext_bytes, AES.block_size, style='pkcs7')

        # 執行加密
        ciphertext_bytes = cipher.encrypt(padded_bytes)

        # 將密文轉為 Base64 編碼
        ciphertext_base64 = base64.b64encode(ciphertext_bytes).decode('utf-8')
        # 打印結果
        print(f"明文: {PLAINTEXT}")
        print(f"密鑰: {KEY}")
        print(f"密文: {encrypted}")
        
        # 將密文存入 JSON 文件
        save_encrypted_to_json(JSON_PATH, encrypted)
        print(f"密文已存入 {JSON_PATH}")
        return ciphertext_base64




# 測試函數
    # 加密明文
    encrypted = encrypt_by_aes(PLAINTEXT, KEY)
    
