
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Write-Host "Pushsing..."

git init
git add .
git commit -m "edit flow and add ipc into pipeline"
git push origin main