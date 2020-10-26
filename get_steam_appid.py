import urllib.request
import json

def retrieve_appid():
    site = "https://api.steampowered.com/ISteamApps/GetAppList/v2"
    response = urllib.request.urlopen(site)
    content = response.read()
    app_list = json.loads(content)["applist"]["apps"]
    return app_list

if __name__ == "__main__":
    csv_out_path = "outputs/app_id.txt"
    csv_out = open(csv_out_path, 'w')
    app_list = retrieve_appid()
    for app in app_list:
        app_id = app["appid"]
        app_name = app["name"].encode("ascii", errors="ignore").decode()
        csv_out.write(str(app_id) + " " + app_name + "\n")
    csv_out.close()