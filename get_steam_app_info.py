import urllib.request
import json
import time

# app_list = get_steam_appid.retrieve_appid()
app_list = []
app_list_src_path = "outputs/app_concurrent_players.txt"
app_list_src = open(app_list_src_path, 'r')
app_list_src.readline()
while True:
    app_line = app_list_src.readline()
    if not app_line:
        break
    app_line_list = app_line.strip().split(",")
    app_id = app_line_list[0]
    app_name = app_line_list[1]
    app = (app_id, app_name)
    app_list.append(app)

result_dict = dict()
for app_i in range(len(app_list)):
    app = app_list[app_i]
    print("Parsing", app, "Progress", app_i, "/", len(app_list))
    app_id = app[0]
    app_info_site = "https://store.steampowered.com/api/appdetails?appids=" + str(app_id)
    page = urllib.request.urlopen(app_info_site)
    content = json.load(page)
    if content[app_id]["success"]:
        print("     Success")
        if "success" in content[app_id]:
            del content[app_id]["success"]
        if "detailed_description" in content[app_id]["data"]:
            del content[app_id]["data"]["detailed_description"]
        if "about_the_game" in content[app_id]["data"]:
            del content[app_id]["data"]["about_the_game"]
        if "header_image" in content[app_id]["data"]:
            del content[app_id]["data"]["header_image"]
        if "website" in content[app_id]["data"]:
            del content[app_id]["data"]["website"]
        if "package_groups" in content[app_id]["data"]:
            del content[app_id]["data"]["package_groups"]
        if "screenshots" in content[app_id]["data"]:
            del content[app_id]["data"]["screenshots"]
        if "movies" in content[app_id]["data"]:
            del content[app_id]["data"]["movies"]
        if "achievements" in content[app_id]["data"]:
            del content[app_id]["data"]["achievements"]
        if "support_info" in content[app_id]["data"]:
            del content[app_id]["data"]["support_info"]
        if "background" in content[app_id]["data"]:
            del content[app_id]["data"]["background"]
    else:
        print("     Failed")
    result_dict[app_id] = content[app_id]
    time.sleep(2)

result_file = open("outputs/app_info.json", 'w')
json.dump(result_dict, result_file)
result_file.close()