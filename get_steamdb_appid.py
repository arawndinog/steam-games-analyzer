# Obsolete as SteamDB is angry and Steam actually has API to do this.
import time
import csv
from selenium import webdriver
import random

data_out_path = "outputs/app_id.csv"
data_out_file = open(data_out_path, 'w')

driver_path = "C:\\Users\\arawn\\Downloads\\chromedriver.exe"
options = webdriver.ChromeOptions() 
options.add_argument("user-data-dir=C:\\Users\\arawn\\AppData\\Local\\Google\\Chrome\\User Data")
driver = webdriver.Chrome(driver_path, chrome_options=options)

for page_i in range(1, 3):
    driver.get("https://steamdb.info/apps/page" + str(page_i))
    print("Parsing page", page_i)
    app_info_list = driver.find_elements_by_class_name("app")
    for app_info_raw in app_info_list:
        if "Unknown App" in app_info_raw.text:
            continue
        app_info = app_info_raw.text.split("\n")
        app_id = app_info[0]
        app_name = app_info[1].encode("ascii", errors="ignore").decode()
        if "," in app_name:
            app_name = '"' + app_name + '"'
        app_type = app_info[2]
        app_info_str = ",".join([app_id, app_name, app_type])
        print("Parsing", app_info_str)
        data_out_file.write(app_info_str + "\n")
    time.sleep(random.randint(5,10))

driver.quit()
data_out_file.close()