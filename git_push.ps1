
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Write-Host "Pushsing..."

git init
git add .
git commit -m "Run Done On Real Enviroment and Already Big Update "
git push origin main