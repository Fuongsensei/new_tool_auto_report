
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Write-Host "Đang đẩy code lên github"

git init
git add .
git commit -m "Chỉnh sửa lại data_ingestor một chút"
git push origin main