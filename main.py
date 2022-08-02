from ast import parse
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
from py import process
import regex

""" 
Hélios Lyons
30/7/22
Innref [-> WanderingStat] (main.py)

"""

# GLOBAL VARIABLES
TOC = [] 
date_regex = r"(\d{4}/\d{2}/\d{2})"
url_regex = re.compile("(\d{4}/\d{2}/\d{2})")
urlTOC = 'https://wanderinginn.com/table-of-contents/'
chapter = 400

def process_toc(url):
    print("Beginning data processing...")
    page = urlopen(urlTOC).read()
    soup = BeautifulSoup(page)
    soup.prettify()

    # Iterate through TOC and collect chapter URLS
    for anchor in soup.findAll('a', href=True):
        anchor['href']
        TOC.append(anchor['href'])

    # Only take URLS with dates (chapters, glossary) -- most recent is duplicate
    sortedTOC = list(filter(url_regex.search, TOC))
    print(sortedTOC)

    return sortedTOC

# Add logic to delimit output (remove | Wandering Inn)
def find_title(url):
    # Get url find page title
    chapter_page = urlopen(url)
    html_bytes = chapter_page.read()
    html = html_bytes.decode("utf-8")
    soup2 = BeautifulSoup(html, "html.parser")

    # Extract chapter code programatically
    title = soup2.title.string
    chapter_code = re.findall("\d+\.\d+", title)

    delimited = title.split('|')

    return delimited

def main():
    print("Entering main:")
    sortedTOC = process_toc(urlTOC)
    title = find_title(sortedTOC[chapter])
    print(title)

if __name__ == "__main__":
    main()

"""
body = soup2.get_text()
brackets = re.findall(r'\[.*?\]', body)
#print(brackets)

level = soup2.find(string=re.compile("Level"))
#print(level)

# WIP BODY: Add logic to only take chapter body (defined within article id="post-2226" for chapter 2.34)
content = soup2.find_all(id='post-2226')
# filteredContent = content.get_text()
# print(content)'


To-do:-
1. DONE: Read TOC into dynamic data structure (python is fucking confusing)
2. DONE: Fetch url from TOC data-structure (equivalent of structs in python?)
3. DONE: Extract text from limited body (only chapter content)
4. 

Documentation:
https://docs.google.com/document/d/12S1_J-qbng38_hZ9PT89PKkrwl4sMXRMc2Epe10xWfQ/edit 

"""