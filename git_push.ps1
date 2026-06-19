
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Write-Host "Đang đẩy code lên github"

git init
git add .
git commit -m "Add code init machine run  and edit config_loader"
git push origin main