#!/usr/bin/python3
# Script to scrape the weather network for its pollen levels over the next three days and email it to a user.
from urllib.request import urlopen
from bs4 import BeautifulSoup
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import calendar

# Date
my_date = datetime.now()
day_of_week = calendar.day_name[my_date.weekday()]
month = my_date.strftime("%B")

# Email settings
fromaddrUsername = "programtesthiro"
addrPassword = "erasmus613"
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddrUsername, addrPassword)
fromaddr = "programtesthiro@gmail.com"
toaddr = input()
user_name = "Pollen Reminder"
msg = MIMEMultipart()
msg['From'] = user_name
msg['To'] = toaddr

# Website Scraping
my_url = 'https://www.theweathernetwork.com/ca/forecasts/pollen/ontario/ottawa'
uClient = urlopen(my_url)
page_html = uClient.read()
uClient.close()
pageSoup = BeautifulSoup(page_html, "html.parser")
last_updated_list = pageSoup.body.find(
    "div", {"class": "pollen_outlook"}).findAll("p")
currentInfo = pageSoup.body.findAll("div", {"class": "column"})
body = ""
for i in range(len(currentInfo)):
    pollen_level = currentInfo[i].find("span", {"class": "date-level"}).text
    date_info = currentInfo[i].find("span").text
    body = body + date_info + ": " + pollen_level + "\n"

body = body + last_updated_list[1].text + "\n\n"
body = body + "Do not reply. This message was sent to you by an automated program."
msg['Subject'] = "Pollen Levels are " + currentInfo[0].find(
    "span", {"class": "date-level"}).text + " | " + day_of_week + ", " + month + " %d" % my_date.day + ", %d" % my_date.year
msg.attach(MIMEText(body, 'plain'))
text = msg.as_string()

server.sendmail(fromaddr, toaddr, text)
server.quit()
