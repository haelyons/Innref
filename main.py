from ast import parse
from bs4 import BeautifulSoup
from urllib.request import urlopen
from matplotlib.pyplot import table
import mechanicalsoup
import re
import regex

""" 
Hélios Lyons
30/7/22
Innref [change to WanderingStat] (main.py)

To-do:-
1. WIP: Read TOC and create key-value pairs
2. Fetch url from TOC data-structure (equivalent of structs in python?)
3. WIP: Extract text from limited body (only chapter content)

Documentation:
https://docs.google.com/document/d/12S1_J-qbng38_hZ9PT89PKkrwl4sMXRMc2Epe10xWfQ/edit 

"""
# To-do TOC: Add logic to sort chapters in TOC into key value pairs with URL
page = urlopen('https://wanderinginn.com/table-of-contents/').read()
soup = BeautifulSoup(page)
soup.prettify()

tableOfContents = []
date_regex = r"(\d{4}/\d{2}/\d{2})"
regexURL = "http://wanderinginn.com/2017/07/04/2-34/"
url_regex = re.compile("(\d{4}/\d{2}/\d{2})")
counter = 0

for anchor in soup.findAll('a', href=True):
    print(anchor['href'])
    tableOfContents.append(anchor['href'])
    counter += 1

sortedContents = list(filter(url_regex.search, tableOfContents))
print(sortedContents)
print(counter)

# Get url find page title
url = "http://wanderinginn.com/2017/07/04/2-34/"
chapter_page = urlopen(url)
html_bytes = chapter_page.read()
html = html_bytes.decode("utf-8")
soup2 = BeautifulSoup(html, "html.parser")
# <article class ="post-1910 page type-page status-publish hentry" id="post-1910"> = $0

# To-do URL: Logic for fetching url from TOC data structure

# Extract chapter code (1.03)
title = soup2.title.string
chapter_code = re.findall("\d+\.\d+", title)
#print(chapter_code)

# Extract class references
body = soup2.get_text()
brackets = re.findall(r'\[.*?\]', body)
#print(brackets)

level = soup2.find(string=re.compile("Level"))
#print(level)

# WIP BODY: Add logic to only take chapter body (defined within article id="post-2226" for chapter 2.34)
content = soup2.find_all(id='post-2226')
# filteredContent = content.get_text()
# print(content)'