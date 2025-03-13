from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 允許跨域請求（因為前端和後端可能在不同端口運行）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允許所有來源，生產環境應限制為特定域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/run-tests")
async def run_tests():
    # 模擬測試結果
    return {
        "summary": {
            "pass_count": 10,
            "fail_count": 2
        },
        "failed_tests": [
            "test_function_a: 失敗原因...",
            "test_function_b: 失敗原因..."
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
    