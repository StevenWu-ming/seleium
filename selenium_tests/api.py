# api.py
import logging
import sys
from fastapi import FastAPI, HTTPException
import unittest
import os
from fastapi.middleware.cors import CORSMiddleware
from test_01_registration import registrationPageTest, CleanTextTestResult, CustomTextTestRunner
from test_02_login import LoginPageTest, CleanTextTestResult, CustomTextTestRunner
from test_03deposit import DepositTest, CleanTextTestResult, CustomTextTestRunner
from config import Config, config
import uvicorn

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

# 設置日誌
log_dir = os.path.dirname(__file__)
log_file = os.path.join(log_dir, 'test_log.log')

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - [%(name)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file, mode='w'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("test_logger")

# 確保 Uvicorn 也使用我們的 logging 設定
uvicorn_logger = logging.getLogger("uvicorn")
uvicorn_logger.handlers = logger.handlers
uvicorn_logger.setLevel(logging.INFO)

@app.get("/run-tests")
async def run_tests():
    try:
        logger.info(f"開始運行測試，當前環境: {config.BASE_URL}")
        
        # 每次請求時生成隨機值並更新 config
        config.INVALID_USERNAME_PREFIX = Config.generate_random_username()
        config.INVALID_PHONE_NUMBER = Config.generate_japanese_phone_number()
        config.INVALID_EMAIL = Config.generate_random_email()

        suite = unittest.TestSuite()
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(registrationPageTest))
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(LoginPageTest))
        # suite.addTest(unittest.TestLoader().loadTestsFromTestCase(DepositTest))
                
        runner = CustomTextTestRunner(resultclass=CleanTextTestResult, verbosity=2)
        result = runner.run(suite)
        
        test_results = result.get_results()

        pass_count = test_results["summary"]["pass_count"]
        fail_count = test_results["summary"]["fail_count"]
        failed_tests = [test["test_name"] for test in test_results["failed_tests"]]

        logger.info("測試運行完成")
        return {
            "summary": {
                "pass_count": pass_count,
                "fail_count": fail_count
            },
            "failed_tests": failed_tests
        }
    
    except Exception as e:
        logger.error(f"測試執行過程中發生錯誤: {str(e)}")
        raise HTTPException(status_code=500, detail=f"測試執行過程中發生錯誤: {str(e)}")
    
@app.get("/test")
async def test_endpoint():
    logger.info("測試端點被訪問")
    return {"message": "Test endpoint is working"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=None)