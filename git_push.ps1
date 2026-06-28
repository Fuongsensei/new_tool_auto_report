
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Write-Host "Pushsing..."

git init
git add .
git commit -m "Build Exe"
git push origin main