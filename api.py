import logging
from fastapi import FastAPI, HTTPException, Body
import unittest
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from tests.test_01_registration import registrationPageTest 
from tests.test_02_login import LoginPageTest
from tests.test_03deposit import DepositTest
from config.config import Config
import uvicorn
from utils.test_utils import CleanTextTestResult, CustomTextTestRunner
import time
from fastapi.staticfiles import StaticFiles
import sys
import os
import traceback

app = FastAPI()

# 掛載 static 目錄，提供靜態檔案
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

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

uvicorn_logger = logging.getLogger("uvicorn")
uvicorn_logger.handlers = logger.handlers
uvicorn_logger.setLevel(logging.INFO)

@app.post("/set-env")
async def set_env(env: str = Body(..., embed=True)):
    valid_envs = ["TestEnv", "ProdEnv", "DevEnv"]
    if env not in valid_envs:
        raise HTTPException(status_code=400, detail=f"無效的環境名稱，請使用: {valid_envs}")
    Config.ENV = env
    logger.info(f"✅ 環境變更為: {Config.ENV}")
    return {"message": f"成功切換到環境: {env}"}

@app.post("/set-merchant")
async def set_merchant(merchant: str = Body(..., embed=True)):
    valid_merchants = ["Merchant1", "Merchant2", "Merchant5", "Merchant7"]
    if merchant not in valid_merchants:
        raise HTTPException(status_code=400, detail=f"無效的商戶，請使用: {valid_merchants}")
    Config.MERCHANT = merchant
    logger.info(f"✅ 商戶變更為: {Config.MERCHANT}")
    return {"message": f"成功切換到商戶: {merchant}"}


# 測試執行函數
def run_test_in_process(test_class, shared_results):
    process_id = os.getpid()
    logger.info(f"開始運行測試類 {test_class.__name__}，進程 ID: {process_id}")

    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(test_class))
    runner = CustomTextTestRunner(resultclass=CleanTextTestResult, verbosity=0)
    result = runner.run(suite)
    test_results = result.get_results()
    shared_results[test_class.__name__] = test_results

@app.get("/run-tests")
async def run_tests():
    start_time = time.time()
    try:
        config = Config.get_current_config()
        logger.info(f"開始運行測試，當前環境: {config.BASE_URL}")

        config.INVALID_USERNAME_PREFIX = Config.generate_random_username()
        config.INVALID_PHONE_NUMBER = Config.generate_japanese_phone_number()
        config.INVALID_EMAIL = Config.generate_random_email()

        test_classes = [registrationPageTest, DepositTest, LoginPageTest]
        shared_results = {}

        for test_class in test_classes:
            run_test_in_process(test_class, shared_results)

        pass_count = 0
        fail_count = 0
        passed_tests = []
        failed_tests = []

        for test_class_name, test_results in shared_results.items():
            if "summary" not in test_results:
                logger.error(f"測試類 {test_class_name} 結果缺少 'summary' 鍵，跳過處理")
                continue
            pass_count += test_results["summary"]["pass_count"]
            fail_count += test_results["summary"]["fail_count"]
            passed_tests.extend(test_results["passed_tests"])
            failed_tests.extend(test_results["failed_tests"])

        total_count = pass_count + fail_count
        logger.info("\n📌測試結果摘要:")
        logger.info(f"✅ 通過測試數: {pass_count}")
        logger.info(f"❌ 失敗測試數: {fail_count}")
        logger.info(f"📊 總測試數: {total_count}")

        end_time = time.time()
        run_time = end_time - start_time

        response_data = {
            "summary": {
                "pass_count": pass_count,
                "fail_count": fail_count,
                "total_count": total_count
            },
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "run_time": f"{run_time:.2f} 秒"
        }

        logger.info("測試運行完成")
        return JSONResponse(
            content=response_data,
            status_code=200,
            media_type="application/json;charset=utf-8"
        )

    except Exception as e:
        logger.error(f"測試執行過程中發生錯誤: {str(e)}\n堆棧跟踪: {traceback.format_exc()}")
        error_response = {
            "error": str(e),
            "detail": "測試執行失敗",
            "run_time": f"{time.time() - start_time:.2f} 秒"
        }
        return JSONResponse(
            content=error_response,
            status_code=500,
            media_type="application/json;charset=utf-8"
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=None)
