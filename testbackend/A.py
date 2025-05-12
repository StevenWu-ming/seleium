# 試錯用的
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64
import getpass
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.config import Config 


config = Config.get_current_config()


def encrypt_password(password: str, public_key_pem: str) -> str:
    rsa_key = RSA.import_key(public_key_pem)
    cipher = PKCS1_v1_5.new(rsa_key)
    encrypted = cipher.encrypt(password.encode("utf-8"))
    return base64.b64encode(encrypted).decode("utf-8")

def main():
    print("🔐 RSA 密碼加密工具 (模擬前端 JSEncrypt)")
    
    # 這裡換成你實際的 rsaPublicKey
    rsa_public_key = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA1lcU5lRpSOqdLicIimSso8wSCTDWdtv3BXGeixALS+bcqOMmV2Tm5F5O3sOAku/a+XxeC+yXkaVrCXpgsl0LEPGVnqO5XoVs4LTeo0zwCJQ+H7TN1ZlqkpfFCL7Mn1+dUXvy+N2p5ijlTZiFsfetc+Jr/JH2Zj62nnc/Vpxne0RsKLwh4Mwp6i/BSv2H9xurablJpz3GPb0qoTniCuxzXvCR9h2tFfbCNacrdpOFVW/A8g27g5em+uqjVB5xAhM1pj0b5PlgR6Oyn5c5mmK1waBx/P+NZJRmGrDbHZMq07v3ma9LTOCGGoG90ReYHxVFRSlAzfl5NGF9nrkfZW4skQIDAQAB
-----END PUBLIC KEY-----"""

    try:
        password = config.VALID_PASSWORD
        encrypted = encrypt_password(password, rsa_public_key)
        print("\n📦 加密後密文 (Base64)：\n", encrypted)
    except Exception as e:
        print("❌ 發生錯誤：", str(e))

if __name__ == "__main__":
    main()
