
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Write-Host "Đang đẩy code lên github"

git init
git add .
git commit -m "Chỉnh sửa mạnh thằng excel_manager.py"
git push origin main