
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Write-Host "Pushsing..."

git init
git add .
git commit -m "add cache class"
git push origin main