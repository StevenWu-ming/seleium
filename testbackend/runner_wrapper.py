# runner_wrapper.py
from login_dp import main as login_and_deposit
from sc_login_aeskey_api import run_admin_login_workflow
from sc_dp_risk import DepositRiskProcessor

def run_full_flow(userName: str, user_name: str, password: str, amount: float):
    # print("✅ 執行 login_dp 登入 + 存款流程")
    login_and_deposit(userName=userName, user_name=user_name, password=password, amount=amount)

    # print("✅ 執行 sc_login_aeskey_api 後台登入 AES Key 擷取流程")
    run_admin_login_workflow()

    # print("✅ 執行 sc_dp_risk 風控流程")
    processor = DepositRiskProcessor()
    processor.run()


if __name__ == "__main__":
    # 測試用參數（你可以隨時改）
    #"" , None , " " 都會抓config裡的值 但如果"abc" 就會用abc
    userName =  None
    user_name = None
    password = None
    amount = 0

    run_full_flow(userName=userName, user_name=user_name, password=password, amount=amount)