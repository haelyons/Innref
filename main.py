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

# GLOBAL VARIABLES
TOC = [] 
date_regex = r"(\d{4}/\d{2}/\d{2})"
url_regex = re.compile("(\d{4}/\d{2}/\d{2})")
urlTOC = 'https://wanderinginn.com/table-of-contents/'
volumeCount = 0
totalWordCount = 0
chapsToPrint = 5


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
    chapter_code = re.findall("\d+\.\d+", title)
    delimited = title.split('|',1)[0]

    return delimited

# Extract the body of a chapter and parse all square-bracketed text
def analyse_body(url):
    print("Analysing chapter body...")
    page = urlopen(url)
    soup3 = BeautifulSoup(page, features="lxml")
    body = soup3.get_text()
    texts = soup3.find('entry-content')

    # Find RE syntax for finding the brackets including
    # the rest of the sentence
    brackets = re.findall(r'\[.*?\]', body)

    wordcount = 0
    words = re.findall('\w+', body)
    wordcount = len(words)
    print(wordcount, "words")
    
    volumeCount =+ wordcount

    #level = soup3.find(string=re.compile("Level"))
    #print(level)
        
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
    # VOLUME 8: 481+

    for chapNum in range(chapsToPrint):
        title = find_title(sortedTOC[chapNum])

        brackets = analyse_body(sortedTOC[chapNum])
        
        fileTitle = '{}.txt'.format(title)
        with open(fileTitle, "w") as writeContent:
            for item in brackets:
                writeContent.write("%s\n" % item)
        print("Processed...%s" % fileTitle)
        print("\n")

    writeContent.close()

    print(volumeCount)
    print(chapNum)

if __name__ == "__main__":
    main()

"""

To-do:-
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