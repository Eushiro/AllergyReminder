# Script to scrape the weather network for its pollen levels over the next three days and place it into a .csv file.
from urllib.request import urlopen
from bs4 import BeautifulSoup

# Opening URL and storing HTML contents
my_url = 'https://www.theweathernetwork.com/ca/forecasts/pollen/ontario/ottawa'
uClient = urlopen(my_url)
page_html = uClient.read()
uClient.close()
pageSoup = BeautifulSoup(page_html, "html.parser")
# Creating file with headers
filename = "Pollen_Information.csv"
f = open(filename, "w")
last_updated_list = pageSoup.body.find("div", {"class": "pollen_outlook"}).findAll("p")
headers = "Date, Pollen Level, " + last_updated_list[1].text.replace(",", " ") + "\n"
f.write(headers)
currentInfo = pageSoup.body.findAll("div", {"class": "column"})
# Scrape information
for i in range(len(currentInfo)):
    pollen_level = currentInfo[i].find("span", {"class": "date-level"}).text
    date_info = currentInfo[i].find("span").text
    f.write(date_info + "," + pollen_level + "\n")
# Save file
f.close()
