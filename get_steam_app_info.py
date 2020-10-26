import json
import get_steam_appid
from selenium import webdriver

driver_path = "C:\\Users\\arawn\\Downloads\\chromedriver.exe"
options = webdriver.ChromeOptions() 
options.add_argument("user-data-dir=C:\\Users\\arawn\\AppData\\Local\\Google\\Chrome\\User Data")
driver = webdriver.Chrome(driver_path, chrome_options=options)

app_list = get_steam_appid.retrieve_appid()

for app_i in range(len(app_list)):
    app = app_list[app_i]
    print("Parsing", app, "Progress", app_i, "/", len(app_list))
    app_id = app["appid"]
    app_info_site = "https://steamspy.com/api.php?request=appdetails&appid=" + str(app_id)
    driver.get(app_info_site)
    app_info = driver.find_element_by_tag_name("pre")
    print(app_info.text)
    time.sleep(2)

driver.quit()