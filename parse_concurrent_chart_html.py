from bs4 import BeautifulSoup

csv_out_path = "outputs/app_concurrent_players.txt"
csv_out = open(csv_out_path, 'w', encoding="utf8")
csv_out.write("app_id, app_name, current, peak24, peakalltime\n")

html_src_path = "C:\\Users\\arawn\\Downloads\\steam_chart_concurrent_players_temp.html"
html_src_file = open(html_src_path, 'r', encoding="utf8")
html_src = html_src_file.read()

soup = BeautifulSoup(html_src, 'html.parser')
app_list = soup(attrs={"class": "app"})
for app in app_list:
    app_id = app.get("data-appid")
    app_name = app.find_all("a")[1].get_text()
    if "," in app_name:
        app_name = '"' + app_name + '"'
    current = app.find_all("td")[4].get("data-sort")
    peak24 = app.find_all("td")[5].get("data-sort")
    peakalltime = app.find_all("td")[6].get("data-sort")
    csv_str = ",".join([app_id, app_name, current, peak24, peakalltime])
    csv_out.write(csv_str + "\n")
csv_out.close()