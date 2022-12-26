from ast import parse
from bs4 import BeautifulSoup
from urllib.request import urlopen
import itertools
import re
from py import process
import regex

"""
Hélios Lyons
27/12/22
Innref [-> WonderingIn] (main.py)

"""

# REGEX
date_regex = r"(\d{4}/\d{2}/\d{2})"
url_regex = re.compile("(\d{4}/\d{2}/\d{2})")

# GLOBALS
TOC = [] 
urlTOC = 'https://wanderinginn.com/table-of-contents/'
totalWords = 0
chapsToPrint = 15 # = DESIRED NUM. OF CHAPS + 1

# LOCALS
chapterWords = 0

# Parse table of contents to only include chapters and write to file
def process_toc(url):
    print("Processing TOC (Table of Contents)...")
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

    cleanTOC = [x for x in splitTOC if "glossary" not in x]

    with open("TOC.txt", "w") as writeTOC:
        for item in cleanTOC:
            writeTOC.write("%s\n" % item)
        print("Wrote sorted URLs to TOC...")

    writeTOC.close()

    return cleanTOC

# Parse the title of a chapter (code or interlude title) and write to string
def find_title(url):
    # Get url, set parser, parse
    chapter_page = urlopen(url)
    html_bytes = chapter_page.read()
    html = html_bytes.decode("utf-8")
    soup2 = BeautifulSoup(html, "html.parser")

    # Extract chapter title
    title = soup2.title.string
    # chapter_code = re.findall("\d+\.\d+", title)
    delimited = title.split('|',1)[0]

    return delimited

# Extract the body of a chapter, parse all square-bracketed text
def analyse_body(url):
    print("Analysing chapter body...")
    page = urlopen(url)
    soup3 = BeautifulSoup(page, features="lxml")
    
    '''
    Title is stored in the header class "entry header"
    Body is stored in the div class "entry content"
    '''
    
    body = soup3.find('div', class_='entry-content').text
    print(body)

    brackets = re.findall(r'\[.*?\]', body)

    # Calculate local chapter number + running sum
    chapterWords = 0
    words = re.findall('\w+', body)
    chapterWords = len(words)
    print(chapterWords, "words")
    global totalWords
    totalWords += chapterWords

    level = soup3.find(string=re.compile("Level"))
    print(level)

    # Source for finding out how to extract body text
    # https://stackoverflow.com/questions/49205608/how-can-i-extract-the-text-part-of-a-blog-page-while-web-scraping-using-beautifu
        
    return brackets

def main():
    print("Entering main...")
    sortedTOC = process_toc(urlTOC)
    print("\n")

    chapters = len(sortedTOC)

    # VOLUME 1: 1 - 66 
    # VOLUME 2: 67 - 122
    # VOLUME 3: 123 - 174
    # VOLUME 4: 175 - 236 
    # VOLUME 5: 237 - 308
    # VOLUME 6: 309 - 385
    # VOLUME 7: 386 - 480
    # VOLUME 8: 481 - 584
    # VOLUME 9: 585 - 628+

    # Extract data and write to fule
    for chapNum in range(chapsToPrint):
        title = find_title(sortedTOC[chapNum]) # Extract title

        brackets = analyse_body(sortedTOC[chapNum]) # Extract brackets
        
        fileTitle = '{}.txt'.format(title) # Add title to text file
        with open(fileTitle, "w") as writeContent:
            for item in brackets: # Iterate through chapter specific array of bracketed text
                writeContent.write("%s\n" % item)
        print("Processed...%s" % fileTitle)
        print("\n")

    writeContent.close()

    print(totalWords)
    print(chapNum)

if __name__ == "__main__":
    main()

"""

To-do:

END FEATURE SET GOALS:
- Index of character specific Classes, Levels, and Skills with chapter references
- Live total-word counter, per chapter word counter

SYSTEM VIEW:
- Training a named entity recognition model based on the data extracted here
  seems most feasible
- Add feature set to README with a checklist on what is included

ITERATING ON CURRENT FEATURE SET:
1. Speed up process of getting chapter information. The sooner this is done,
   the easier it will be to implement

2. Improve collection of Levelling data -- is "Level" always capitalised? What are 
   the different sentence structures in which this word occurs, is it problematic
   that in-world characters discuss levels for this approach.

Documentation:
https://docs.google.com/document/d/12S1_J-qbng38_hZ9PT89PKkrwl4sMXRMc2Epe10xWfQ/edit 

"""