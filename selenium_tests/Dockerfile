# 使用 Python 3.9 作為基礎映像
FROM python:3.9

# 設定工作目錄
WORKDIR /app

# 複製專案所有檔案到容器內
COPY . /app

# 安裝依賴
RUN pip install --no-cache-dir -r requirements.txt

# 設定 FastAPI 運行指令
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]

