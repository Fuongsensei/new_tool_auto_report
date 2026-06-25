
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Write-Host "Pushsing..."

git init
git add .
git commit -m "add try catch and raise , and DI Logger%"
git push origin main