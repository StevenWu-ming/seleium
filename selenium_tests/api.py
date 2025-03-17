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

# 設置日誌（單一文件，支援多進程安全寫入）
log_dir = os.path.dirname(__file__)
log_file = os.path.join(log_dir, 'test_log.log')

# 使用 ConcurrentRotatingFileHandler 來支援多進程安全寫入
try:
    from concurrent_log_handler import ConcurrentRotatingFileHandler
    log_handler = ConcurrentRotatingFileHandler(log_file, mode='a', maxBytes=10*1024*1024, backupCount=1, encoding='utf-8')
except ImportError:
    from logging.handlers import RotatingFileHandler
    log_handler = RotatingFileHandler(log_file, mode='a', maxBytes=10*1024*1024, backupCount=1, encoding='utf-8')

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - [%(name)s] %(message)s",
    handlers=[
        log_handler,
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("test_logger")

# 同步 Uvicorn 的日誌設定
uvicorn_logger = logging.getLogger("uvicorn")
uvicorn_logger.handlers = logger.handlers
uvicorn_logger.setLevel(logging.INFO)

# 測試運行函數（用於多進程）
def run_test_in_process(test_class, shared_results):
    process_id = os.getpid()
    logger.info(f"開始運行測試類 {test_class.__name__}，進程 ID: {process_id}")
    
    suite = unittest.TestSuite()
    # 加載整個測試類中的所有測試用例
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(test_class))
    
    # 使用 CustomTextTestRunner，但禁止打印結果
    runner = CustomTextTestRunner(resultclass=CleanTextTestResult, verbosity=0)  # 設置 verbosity=0，避免打印
    result = runner.run(suite)
    
    test_results = result.get_results()
    shared_results[test_class.__name__] = test_results

@app.get("/run-tests")
async def run_tests():
    try:
        logger.info(f"開始運行測試，當前環境: {config.BASE_URL}")
        
        # 每次請求時生成隨機值並更新 config
        config.INVALID_USERNAME_PREFIX = Config.generate_random_username()
        config.INVALID_PHONE_NUMBER = Config.generate_japanese_phone_number()
        config.INVALID_EMAIL = Config.generate_random_email()

        # 準備測試類（不再指定單一測試方法）
        test_classes = [
            registrationPageTest,
            LoginPageTest,
            DepositTest,
        ]

        # 使用 Manager 來共享結果
        manager = Manager()
        shared_results = manager.dict()

        # 使用多進程運行測試
        with Pool(processes=4) as pool:  # 設置進程數，可根據 CPU 核心數調整
            pool.starmap(
                partial(run_test_in_process, shared_results=shared_results),
                [(test_class,) for test_class in test_classes]
            )

        # 合併測試結果
        pass_count = 0
        fail_count = 0
        passed_tests = []
        failed_tests = []

        for test_class_name, test_results in shared_results.items():
            if "summary" not in test_results:
                logger.error(f"測試類 {test_class_name} 結果缺少 'summary' 鍵")
                raise HTTPException(status_code=500, detail=f"測試類 {test_class_name} 結果結構不完整，缺少 'summary' 鍵")
            if "passed_tests" not in test_results:
                logger.error(f"測試類 {test_class_name} 結果缺少 'passed_tests' 鍵")
                raise HTTPException(status_code=500, detail=f"測試類 {test_class_name} 結果結構不完整，缺少 'passed_tests' 鍵")
            if "failed_tests" not in test_results:
                logger.error(f"測試類 {test_class_name} 結果缺少 'failed_tests' 鍵")
                raise HTTPException(status_code=500, detail=f"測試類 {test_class_name} 結果結構不完整，缺少 'failed_tests' 鍵")

            pass_count += test_results["summary"]["pass_count"]
            fail_count += test_results["summary"]["fail_count"]
            passed_tests.extend(test_results["passed_tests"])
            failed_tests.extend(test_results["failed_tests"])

        # 打印總結（只在主進程中打印）
        total_count = pass_count + fail_count
        logger.info("\n📌測試結果摘要:")
        logger.info(f"^^通過測試數: {pass_count}")
        logger.info(f"❌失敗測試數: {fail_count}")
        logger.info(f"📊總測試數: {total_count}")

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
    logger.info("測試端點被訪問")
    return JSONResponse(
        content={"message": "Test endpoint is working"},
        media_type="application/json;charset=utf-8"
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=None)