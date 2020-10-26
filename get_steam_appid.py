import urllib.request
import json

csv_out_path = "outputs/app_id.txt"
csv_out = open(csv_out_path, 'w')
site = "https://api.steampowered.com/ISteamApps/GetAppList/v2"
response = urllib.request.urlopen(site)
content = response.read()

app_list = json.loads(content)["applist"]["apps"]
for app in app_list:
    app_id = app["appid"]
    app_name = app["name"].encode("ascii", errors="ignore").decode()
    csv_out.write(str(app_id) + " " + app_name + "\n")
csv_out.close()