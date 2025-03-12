




# unittest
openvpn
Username: cooper
Password: rVf75qEX2ffmwiP7gT3lcZ7VwinGXCd8

# 登入自動化 優化
手機地區號登入
判斷郵箱是否符合規範
# 註冊自動化 優化
用戶名/郵箱/密碼是否符合規範
優化增加判斷chackbox取消勾選後 註冊按鈕是否為disabled


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

# 創建虛擬環境
python3 -m venv 虛擬環境名稱 
# 啟動虛擬環境
source 虛擬環境名稱/bin/activate 
# 啟動虛擬環境
deactivate
# 刪除虛擬環境
rm -rf 虛擬環境名稱 

