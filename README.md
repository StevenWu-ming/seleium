1
1️⃣ 安裝 Python
請同事到 Python 官方網站 安裝 Python，並確保 pip 可用：

sh
python --version
pip --version

2️⃣ 安裝 Git 並拉取倉庫
sh
git clone https://github.com/yourusername/your-repo.git
cd your-repo

3️⃣ 建立虛擬環境並安裝套件
sh
python -m venv venv
source venv/bin/activate  # Windows 用 `venv\Scripts\activate`
pip install --upgrade pip  # 確保 pip 是最新版本
pip install -r requirements.txt  # 安裝所需的套件

4️⃣ 安裝 Selenium 需要的 WebDriver
若測試 Chrome，需安裝 ChromeDriver。
若測試 Firefox，需安裝 GeckoDriver。

5️⃣ 執行測試
sh
python -m unittest discover tests
或執行 run_tests.py：
sh
python run_tests.py

# unittest
openvpn
Username: cooper
Password: rVf75qEX2ffmwiP7gT3lcZ7VwinGXCd8
cooper-ios	MG1NWtJb8tMOIWhPPTdBD0BOL0Spz+bY
cooper-android	Ws4oBNPCEvH%I9Ry5P5LbJ0Y6wkKonQh
cooper-tao	Lb5CxnOkWXCxF9+r5nFS6ACHwalqU9Ql

# 登入自動化 優化
手機地區號登入
判斷郵箱是否符合規範
# 註冊自動化 優化
用戶名/郵箱/密碼是否符合規範
優化增加判斷chackbox取消勾選後 註冊按鈕是否為disabled

1
================================================================================================================================
# 建立 Docker 映像
docker build -t my-fastapi-app .
# 運行容器（將 8000 端口映射到本機）
docker run -d -p 8000:8000 my-fastapi-app:latest
# 進入容器
docker exec -it my-fastapi-app /bin/bash
# 停止 & 刪除容器
docker stop my-fastapi-app
docker rm my-fastapi-app
# 檢視當前運行中的容器
docker ps
# 確保已經成功建立 Docker 映像
docker images
# 刪除映像檔
docker rmi my-fastapi-app:latest
================================================================================================================================
# 查詢進程
lsof -i :8000
netstat -aon | findstr :8000 # Windows
taskkill /IM 進程名稱 /F
taskkill /IM python.exe /F

# 殺進程
kill -9 {PID}
pkill -9 -f python


ifconfig 
# 後端api
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
uvicorn api:app --host 0.0.0.0 --port 8000 --workers 4
python -m uvicorn api:app --host 0.0.0.0 --port 8000 --workers 2


curl http://localhost:8000/run-tests #本地
tests #區域網路IP
# 前端HTML
python3 -m http.server 8000
python3 -m http.server 8000 --bind 0.0.0.0
& C:/Users/d1031/AppData/Local/Programs/Python/Python313/python.exe -m http.server 8000 --bind 0.0.0.0
http://localhost:8000/index.html #本地
http://192.168.0.202:8001/index.html #區域網路IP

================================================================================================================================
# git指令
git add .
git commit -m "更新內容"
git push origin main

# 如果你的專案還沒有 Git，可以在 VSCode 的終端 (Terminal) 中執行：
git init
# 檢查倉庫狀態：
git status
# 檢查遠端連線
git remote -v

# 創建一個新的分支
git branch feature-branch
# 查看所有分支
git branch 
# 切換到新分支：
git checkout feature-branch
git switch feature-branch
# 如果你在 feature-branch，但要合并到 main，需要先切换到 main：
git checkout main
git switch main
# 确保 main 分支是最新的：
git pull origin main
# 如果你想把 feature-branch 合并到 main：
git merge feature-branch
# 合并后，推送到 GitHub：
git push origin main
# 删除合并后的分支
# 如果 feature-branch 已经不需要，可以删除：
git branch -d feature-branch
# 如果远程也要删除：
git push origin --delete feature-branch

# 流程
確認你當前在哪個分支 >>> 創建一個新的分支 >>> 切換到新分支 >>> 確認當前分支 >>> 新分支開發並提交變更 >>> 新分支推送到遠端 
>>> 切換回 main 分支 >>> 合併分支 >>> 沒有衝突,可以直接提交推送到遠端 >>> 有衝突：VSCode 會標記衝突的文件，然後你需要手動編輯這些檔案,解決後重新提交推送
>>> 刪除已合併的分支
================================================================================================================================
# 創建虛擬環境
python3 -m venv 虛擬環境名稱 
# 啟動虛擬環境
source 虛擬環境名稱/bin/activate 
# 退出虛擬環境
deactivate
# 刪除虛擬環境
rm -rf 虛擬環境名稱 
================================================================================================================================

