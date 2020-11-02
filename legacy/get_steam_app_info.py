# obsolete due to steamspy being unreliable
import json
import get_steam_appid
from selenium import webdriver

# driver_path = "C:\\Users\\arawn\\Downloads\\chromedriver.exe"
driver_path = "/home/adrianwong/Downloads/chromedriver"
options = webdriver.ChromeOptions() 
# options.add_argument("user-data-dir=C:\\Users\\arawn\\AppData\\Local\\Google\\Chrome\\User Data")
options.add_argument("user-data-dir=/home/adrianwong/.config/google-chrome")
driver = webdriver.Chrome(driver_path, chrome_options=options)

# app_list = get_steam_appid.retrieve_appid()
app_list = []
app_list_src_path = "outputs/app_concurrent_players.txt"
app_list_src = open(app_list_src_path, 'r')
while True:
    app_line = app_list_src.readline()
    if not app_line:
        break
    app_line_list = app_line.strip().split(",")
    app_id = app_line_list[0]
    app_name = app_line_list[1]
    app = (app_id, app_name)
    app_list.append(app)

for app_i in range(len(app_list)):
    app = app_list[app_i]
    print("Parsing", app, "Progress", app_i, "/", len(app_list))
    # app_id = app["appid"]
    app_id = app[0]
    app_info_site = "https://steamspy.com/api.php?request=appdetails&appid=" + str(app_id)
    driver.get(app_info_site)
    app_info = driver.find_element_by_tag_name("pre")
    print(app_info.text)
    assert False
    time.sleep(2)

driver.quit()