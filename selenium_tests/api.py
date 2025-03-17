import logging
import sys
from fastapi import FastAPI, HTTPException
import unittest
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from test_01_registration import registrationPageTest
from test_02_login import LoginPageTest
from test_03deposit import DepositTest
from config import Config, config
import uvicorn
from test_utils import CleanTextTestResult, CustomTextTestRunner
from multiprocessing import Pool, Manager
from functools import partial

app = FastAPI()

# 設置 CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 設置日誌（每個進程獨立日誌）
def setup_logging(process_id):
    log_dir = os.path.dirname(__file__)
    log_file = os.path.join(log_dir, f'test_log_{process_id}.log')  # 每個進程獨立日誌文件
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - [%(name)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file, mode='w', encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(f"test_logger_{process_id}")

# 測試運行函數（用於多進程）
def run_test_in_process(test_class, test_name, shared_results):
    process_id = os.getpid()
    logger = setup_logging(process_id)
    logger.info(f"開始運行測試 {test_name}，進程 ID: {process_id}")
    
    suite = unittest.TestSuite()
    suite.addTest(test_class(test_name))
    runner = CustomTextTestRunner(resultclass=CleanTextTestResult, verbosity=2)
    result = runner.run(suite)
    
    test_results = result.get_results()
    shared_results[test_name] = test_results

@app.get("/run-tests")
async def run_tests():
    try:
        logger = setup_logging("main")
        logger.info(f"開始運行測試，當前環境: {config.BASE_URL}")
        
        # 每次請求時生成隨機值並更新 config
        config.INVALID_USERNAME_PREFIX = Config.generate_random_username()
        config.INVALID_PHONE_NUMBER = Config.generate_japanese_phone_number()
        config.INVALID_EMAIL = Config.generate_random_email()

        # 準備測試用例
        test_cases = [
            (registrationPageTest, "test_01_01check_registration_button_enabled_after_username_and_password"),
            (registrationPageTest, "test_01_02_registration"),
            (registrationPageTest, "test_01_03_registration_duplicate"),
            (LoginPageTest, "test_01_01_phonenumber_login"),
            (LoginPageTest, "test_01_02_phonenumber__wronglogin"),
            (LoginPageTest, "test_02_01check_login_button_enabled_after_username_and_password"),
            (LoginPageTest, "test_02_02_successful_login"),
            (LoginPageTest, "test_02_03_invalid_credentials"),
            (LoginPageTest, "test_03_01_mail_login"),
            (LoginPageTest, "test_03_02_mail_wronglogin"),
            (DepositTest, "test_01_01_deposit"),
            # 添加更多測試用例...
        ]

        # 使用 Manager 來共享結果
        manager = Manager()
        shared_results = manager.dict()

        # 使用多進程運行測試
        with Pool(processes=4) as pool:  # 設置進程數，可根據 CPU 核心數調整
            pool.starmap(
                partial(run_test_in_process, shared_results=shared_results),
                [(test_class, test_name) for test_class, test_name in test_cases]
            )

        # 合併測試結果
        pass_count = 0
        fail_count = 0
        passed_tests = []
        failed_tests = []

        for test_name, test_results in shared_results.items():
            if "summary" not in test_results:
                logger.error(f"測試 {test_name} 結果缺少 'summary' 鍵")
                raise HTTPException(status_code=500, detail=f"測試 {test_name} 結果結構不完整，缺少 'summary' 鍵")
            if "passed_tests" not in test_results:
                logger.error(f"測試 {test_name} 結果缺少 'passed_tests' 鍵")
                raise HTTPException(status_code=500, detail=f"測試 {test_name} 結果結構不完整，缺少 'passed_tests' 鍵")
            if "failed_tests" not in test_results:
                logger.error(f"測試 {test_name} 結果缺少 'failed_tests' 鍵")
                raise HTTPException(status_code=500, detail=f"測試 {test_name} 結果結構不完整，缺少 'failed_tests' 鍵")

            pass_count += test_results["summary"]["pass_count"]
            fail_count += test_results["summary"]["fail_count"]
            passed_tests.extend(test_results["passed_tests"])
            failed_tests.extend(test_results["failed_tests"])

        response_data = {
            "summary": {
                "pass_count": pass_count,
                "fail_count": fail_count
            },
            "passed_tests": passed_tests,
            "failed_tests": failed_tests
        }

        logger.info("測試運行完成")
        return JSONResponse(
            content=response_data,
            media_type="application/json;charset=utf-8"
        )
    
    except Exception as e:
        logger.error(f"測試執行過程中發生錯誤: {str(e)}")
        raise HTTPException(status_code=500, detail=f"測試執行過程中發生錯誤: {str(e)}")

@app.get("/test")
async def test_endpoint():
    logger = setup_logging("main")
    logger.info("測試端點被訪問")
    return JSONResponse(
        content={"message": "Test endpoint is working"},
        media_type="application/json;charset=utf-8"
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=None)