from ast import parse
from bs4 import BeautifulSoup
from urllib.request import urlopen
import itertools
import re
from py import process
import regex

"""
Hélios Lyons
30/7/22
Innref [-> WanderingStat] (main.py)

"""

# REGEX rule for date extraction (chapter titles)
date_regex = r"(\d{4}/\d{2}/\d{2})"
url_regex = re.compile("(\d{4}/\d{2}/\d{2})")

# Globals
TOC = [] 
urlTOC = 'https://wanderinginn.com/table-of-contents/'
totalWords = 0

# Locals
chapterWords = 0
chapsToPrint = 15 # = DESIRED NUM. OF CHAPS + 1

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

    body = soup3.get_text()
    
    actual_body = soup3.find('div', class_='entry-content').text
    print(actual_body)

    brackets = re.findall(r'\[.*?\]', actual_body)

    # Calculate local chapter number + running sum
    chapterWords = 0
    words = re.findall('\w+', actual_body)
    chapterWords = len(words)
    print(chapterWords, "words")
    global totalWords
    totalWords += chapterWords

    level = soup3.find(string=re.compile("Level"))
    print(level)
        
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
6. Fix extraction of body content to not include comments

11. Improve speed of extraction, currently takes ages 

7. Abstract chapter specific functions (new file) to be able to iterate through all chapters
    DONE Start by collecting all titles, URLs and index for chapters
    DONE Write to some file format or global data structure (CSV?)
    WIP Seperate collection into volumes
    - Fix filename assignment

8. Create chapter specific array of body references. Keep in mind that the indexes for the 
   positions of each reference in the body, as part of sentences and paragraphs, will be 
   essential for eventually parsing Class and Skill content

9. Create a seperate list which contains all references to a specific class in order
    - Could also just sort existing list to find earliest reference (via URL date)

10. Count the number of chapters programatically, add to a seperate 'stats' file, which can 
    average/sum word counts in chapters, as well as providing a providing a 'live' counter of the total
    word limit


Documentation:
https://docs.google.com/document/d/12S1_J-qbng38_hZ9PT89PKkrwl4sMXRMc2Epe10xWfQ/edit 

"""