
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Write-Host "Pushsing..."

git init
git add .
git commit -m "detele cache class , delete reportdatadashboard,add ProcessDataDashboard in stage.py "
git push origin main