from ast import parse
from bs4 import BeautifulSoup
from urllib.request import urlopen
import mechanicalsoup
import re

# Logic to print chapters and links from table of contents
browser = mechanicalsoup.Browser()
toc_url = "https://wanderinginn.com/table-of-contents/"
toc_page = browser.get(toc_url)
links = toc_page.soup.select("a")

for link in links:
    address = link["href"]
    text = link.text
    #print(f"{text}: {address}")

# To-do TOC: Add logic to sort chapters in TOC into key value pairs with URL

# Get url find page title
url = "http://wanderinginn.com/2017/07/04/2-34/"
chapter_page = urlopen(url)
html_bytes = chapter_page.read()
html = html_bytes.decode("utf-8")
soup = BeautifulSoup(html, "html.parser")
# <article class ="post-1910 page type-page status-publish hentry" id="post-1910"> = $0

# To-do URL: Logic for fetching url from TOC data structure

# Extract chapter code (1.03)
title = soup.title.string
chapter_code = re.findall("\d+\.\d+", title)
print(chapter_code)

# Extract class references
body = soup.get_text()
brackets = re.findall(r'\[.*?\]', body)
print(brackets)

level = soup.find(string=re.compile("Level"))
print(level)

# To-do BODY: Add logic to only take chapter body (defined within article id="post-2226")