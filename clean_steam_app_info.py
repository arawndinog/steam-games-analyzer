import json
import re

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def main():
    src_path = "outputs/app_info.json"
    src_file = open(src_path, 'r')
    src_json = json.load(src_file)

    out_path = "outputs/app_info_cleaned.csv"
    out_file = open(out_path, 'w')
    out_file.write("app_id, is_free, num_dlc, have_in_app_purchase, directx_ver, have_mp, have_win, have_mac, have_linux, is_action, is_adventure, is_casual, is_mmo, is_racing, is_rpg, is_sim, is_sports, is_strat,is_indie, price, metacritic_score, date_of_release, required_age, supported_languages\n")

    i = 0
    for app_id in src_json:
        app = src_json[app_id]
        # exclude unsuccessful parsing
        if "success" in app:
            if not app["success"]:
                continue
        # exclude non-games
        if app["data"]["type"] == "game":

            # free to play?
            is_free = app["data"]["is_free"]

            # parse number of dlc, if there are any
            num_dlc = 0
            if "dlc" in app["data"]:
                num_dlc = len(app["data"]["dlc"])

            # check directx version
            directx_ver = ""
            if "minimum" in app["data"]["pc_requirements"]:
                pc_requirements_str = app["data"]["pc_requirements"]["minimum"]
            elif "recommended" in app["data"]["pc_requirements"]:
                pc_requirements_str = app["data"]["pc_requirements"]["recommended"]
            pc_requirements_str = cleanhtml(pc_requirements_str)
            if "DirectX" in pc_requirements_str:
                directx_index = pc_requirements_str.index("DirectX")
                numbers = "0123456789"
                for pc_requirements_str_i in range(directx_index,len(pc_requirements_str)):
                    if pc_requirements_str[pc_requirements_str_i] in numbers:
                        directx_ver += pc_requirements_str[pc_requirements_str_i]
                    elif directx_ver:
                        break
            if not directx_ver or int(directx_ver) > 12:
                directx_ver = "9"

            # parse categories
            have_in_app_purchase = False
            have_mp = False
            if "categories" in app["data"]:
                app_categories = app["data"]["categories"]
                for cat in app_categories:
                    if cat["description"] == "In-App Purchases":
                        have_in_app_purchase = True
                    if cat["description"] == "Multi-player":
                        have_mp = True

            # parse supported platforms
            have_win = app["data"]["platforms"]["windows"]
            have_mac = app["data"]["platforms"]["mac"]
            have_linux = app["data"]["platforms"]["linux"]
            
            # parse devs; if no devs, skip. devs will be parsed to other files for network generation
            if "developers" not in app["data"]:
                continue

            # parse genres
            is_action = False
            is_adventure = False
            is_casual = False
            is_mmo = False
            is_racing = False
            is_rpg = False
            is_sim = False
            is_sports = False
            is_strat = False
            is_indie = False
            if "genres" in app["data"]:
                app_genres = app["data"]["genres"]
                for genre in app_genres:
                    if genre["description"] == "Indie":
                        is_indie = True
                    if genre["description"] == "Action":
                        is_action = True
                    if genre["description"] == "Adventure":
                        is_adventure = True
                    if genre["description"] == "Casual":
                        is_casual = True
                    if genre["description"] == "Massively Multiplayer":
                        is_mmo = True
                    if genre["description"] == "Racing":
                        is_racing = True
                    if genre["description"] == "RPG":
                        is_rpg = True
                    if genre["description"] == "Simulation":
                        is_sim = True
                    if genre["description"] == "Sports":
                        is_sports = True
                    if genre["description"] == "Strategy":
                        is_strat = True

            # parse price; original price is in cents.
            price = 0
            if "price_overview" in app["data"]:
                price = app["data"]["price_overview"]["initial"]
                price = price/100

            # parse score, if any
            metacritic_score = None
            if "metacritic_score" in app["data"]:
                metacritic_score = app["data"]["metacritic"]["score"]
            # num_recommend = app["data"]["recommendations"]["total"]
            # parse others
            date_of_release = '"' + app["data"]["release_date"]["date"] + '"'
            required_age = app["data"]["required_age"]
            # clean up languages to plain text
            supported_languages = '"' + cleanhtml(app["data"]["supported_languages"]) + '"'
            supported_languages = supported_languages.replace("*", '')
            supported_languages = supported_languages.replace("languages with full audio support", '')
            csv_entry = ",".join([str(app_id), str(is_free), str(num_dlc), str(have_in_app_purchase), str(directx_ver), str(have_mp), str(have_win), str(have_mac), str(have_linux), \
                                str(is_action), str(is_adventure), str(is_casual), str(is_mmo), str(is_racing), str(is_rpg), str(is_sim), str(is_sports), str(is_strat), str(is_indie), \
                                str(price), str(metacritic_score), date_of_release, str(required_age), supported_languages])
            out_file.write(csv_entry + "\n")
        i += 1

    src_file.close()
    out_file.close()

main()
