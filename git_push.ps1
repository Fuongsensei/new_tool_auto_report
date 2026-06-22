
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Write-Host "Đang đẩy code lên github"

git init
git add .
git commit -m "Add code to state.py and class processStep"
git push origin main