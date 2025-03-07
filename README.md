# unittest
openvpn
Username: cooper
Password: rVf75qEX2ffmwiP7gT3lcZ7VwinGXCd8

＃git指令
git add .
git commit -m "更新內容"
git push origin main

git branch #查看所有分支
如果你在 feature-branch，但要合并到 main，需要先切换到 main：
git checkout main
git switch main
确保 main 分支是最新的：
git pull origin main
如果你想把 feature-branch 合并到 main：
git merge feature-branch
合并后，推送到 GitHub：
git push origin main
(可选) 删除合并后的分支
如果 feature-branch 已经不需要，可以删除：
git branch -d feature-branch
如果远程也要删除：
git push origin --delete feature-branch

＃創建虛擬環境
python3 -m venv 虛擬環境名稱 #創建虛擬環境
source 虛擬環境名稱/bin/activate ＃啟動虛擬環境
deactivate ＃退出虛擬環境
rm -rf 虛擬環境名稱 #刪除虛擬環境

