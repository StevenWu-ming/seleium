# 提供 FastAPI 服務，支援自動化測試執行、環境與商戶切換、測試結果查詢及存款流程運行
import os
import signal
import subprocess
from multiprocessing import Process, Manager, cpu_count
import time
import threading
import logging
import sys
import unittest
import importlib
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
from config.config import Config
from utils.test_utils import CleanTextTestResult, CustomTextTestRunner

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "testbackend")))
from runner_wrapper import run_full_flow

BASE_TEST_DIR = os.path.join(os.path.dirname(__file__), "tests")

app = FastAPI()

class RunParams(BaseModel):
    userName: str
    user_name: str
    password: str
    amount: float

# app.mount("/static", StaticFiles(directory="static", html=True), name="static")
app.mount("/screenshots", StaticFiles(directory="/Users/steven/deepseek/seleium/screenshots"), name="screenshots")

origins = ["http://localhost", "http://127.0.0.1:8000", "*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    handlers=[log_handler, logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("test_logger")

uvicorn_logger = logging.getLogger("uvicorn")
uvicorn_logger.handlers = logger.handlers
uvicorn_logger.setLevel(logging.INFO)

api_test_results = {"status": "not_started", "data": None}

def discover_test_classes():
    discovered = []
    for filename in os.listdir(BASE_TEST_DIR):
        if filename.startswith("test_") and filename.endswith(".py"):
            module_name = filename[:-3]
            module = importlib.import_module(f"tests.{module_name}")
            for attr in dir(module):
                obj = getattr(module, attr)
                if isinstance(obj, type) and issubclass(obj, unittest.TestCase):
                    discovered.append(obj)
    return discovered

def run_test_in_process(test_class, result_dict, env, merchant):
    Config.ENV = env
    Config.MERCHANT = merchant
    config = Config.get_current_config()
    process_id = os.getpid()
    logger.info(f"開始運行測試類 {test_class.__name__}，進程 ID: {process_id}")
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(test_class))
    runner = CustomTextTestRunner(resultclass=CleanTextTestResult, verbosity=0)
    result = runner.run(suite)
    result_dict[test_class.__name__] = result.get_results()

def run_tests_background():
    global api_test_results
    api_test_results["status"] = "running"
    start_time = time.time()

    try:
        config = Config.get_current_config()
        logger.info(f"開始運行測試，當前環境: {config.BASE_URL}，商戶: {Config.MERCHANT}")

        config.INVALID_USERNAME_PREFIX = Config.generate_random_username()
        config.INVALID_PHONE_NUMBER = Config.generate_japanese_phone_number()
        config.INVALID_EMAIL = Config.generate_random_email()

        test_classes = discover_test_classes()
        with Manager() as manager:
            shared_results = manager.dict()
            max_workers = cpu_count()
            active_processes = []

            for test_class in test_classes:
                while len(active_processes) >= max_workers:
                    for p in active_processes:
                        if not p.is_alive():
                            active_processes.remove(p)
                    time.sleep(0.2)

                # p = Process(target=run_test_in_process, args=(test_class, shared_results))
                p = Process(target=run_test_in_process, args=(test_class, shared_results, Config.ENV, Config.MERCHANT))

                p.start()
                active_processes.append(p)

            for p in active_processes:
                p.join()

            pass_count = 0
            fail_count = 0
            passed_tests = []
            failed_tests = []

            for test_class_name, result in shared_results.items():
                summary = result.get("summary", {})
                pass_count += summary.get("pass_count", 0)
                fail_count += summary.get("fail_count", 0)
                passed_tests.extend(result.get("passed_tests", []))
                failed_tests.extend(result.get("failed_tests", []))

            run_time = time.time() - start_time
            api_test_results["status"] = "completed"
            api_test_results["data"] = {
                "summary": {"pass_count": pass_count, "fail_count": fail_count, "total_count": pass_count + fail_count},
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "run_time": f"{run_time:.2f} 秒"
            }
        logger.info("✅ 測試執行完成")
    except Exception as e:
        api_test_results["status"] = "failed"
        api_test_results["data"] = {"error": str(e)}
        logger.exception("❌ 測試執行失敗")

@app.post("/run-tests")
async def run_tests():
    global api_test_results
    if api_test_results["status"] == "running":
        return {"status": "still_running"}
    thread = threading.Thread(target=run_tests_background)
    thread.start()
    return {"status": "started"}

@app.get("/test-results")
async def get_test_results():
    return api_test_results

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

@app.post("/run-login_deposit")
def run_all(params: RunParams):
    try:
        run_full_flow(userName=params.userName, user_name=params.user_name, password=params.password, amount=params.amount)
        return {"message": "✅ 自動化小工具-存款流程完成"}
    except Exception as e:
        return {"error": "❎" f"執行失敗: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=None)
