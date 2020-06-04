# verified_online
Invoke-WebRequest -Uri "http://data.phishtank.com/data/online-valid.csv" -OutFile .\verified_online.csv

# top10milliondomains
Invoke-WebRequest -Uri "https://www.domcop.com/files/top/top10milliondomains.csv.zip" -OutFile .\top10milliondomains.csv.zip
Expand-Archive -Path .\top10milliondomains.csv.zip -DestinationPath .
Remove-Item .\top10milliondomains.csv.zip