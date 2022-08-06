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
    soup = BeautifulSoup(page, features="lxml")
    soup.prettify()

    # Iterate through TOC and collect chapter URLS
    for anchor in soup.findAll('a', href=True):
        anchor['href']
        TOC.append(anchor['href'])

    # Only take URLS with dates (chapters, glossary) -- most recent is duplicate
    sortedTOC = list(filter(url_regex.search, TOC))
    splitTOC = sortedTOC[sortedTOC.index('https://wanderinginn.com/2016/07/27/1-00/'):]

    return splitTOC

# CHAPTER SPECIFIC FUNCTIONS
# Add logic to delimit output (remove | Wandering Inn)
def find_title(url):
    # Get url, set parser, parse
    chapter_page = urlopen(url)
    html_bytes = chapter_page.read()
    html = html_bytes.decode("utf-8")
    soup2 = BeautifulSoup(html, "html.parser")

    # Extract chapter title
    title = soup2.title.string
    chapter_code = re.findall("\d+\.\d+", title)
    delimited = title.split('|',1)[0]
    
    return delimited

def analyse_body(url):
    page = urlopen(url)
    soup3 = BeautifulSoup(page, features="lxml")
    body = soup3.get_text()

    brackets = re.findall(r'\[.*?\]', body)
    
    content = ''
    for content in soup3.select('article[id^="post-"]'):
        print(content.get_text()) 
        
    return brackets

def main():
    print("Entering main:")
    sortedTOC = process_toc(urlTOC)
    
    title = find_title(sortedTOC[chapter])
    print(title)
    
    chapters = len(sortedTOC)
    print(chapters)

    brackets = analyse_body(sortedTOC[chapter])
    #print(brackets)

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

To-do:-
7. Abstract chapter specific functions (new file) to be able to iterate through all chapters
    - Start by collecting all titles, URLs and index for chapters
    - Write to some file format or global data structure (CSV?)
    - Seperate collection into volumes

8. Expand data structure to include all references to classes (brackets)

9. Create a seperate list which contains all references to a specific class in order
    - Could also just sort existing list to find earliest reference (via URL date)


Documentation:
https://docs.google.com/document/d/12S1_J-qbng38_hZ9PT89PKkrwl4sMXRMc2Epe10xWfQ/edit 

"""