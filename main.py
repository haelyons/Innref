from bs4 import BeautifulSoup
from urllib.request import urlopen

import re

"""

Hélios Lyons
27/12/22
Innref [-> WonderingInn] (main.py)

"""

"""

[Universal Data Tool](https://universaldatatool.com/app/) -- data annotation for images, text, etc
[CoreNLP](http://corenlp.run) -- demo for part of speech and named entity extraction
[Regular Expressions 101](https://regex101.com/) -- tool and debugger for regex expressions
[Regexplained](https://www.regexplained.co.uk/) -- Visual explanation of regex explanations (great diagrams)

GOALS:
- Index of character specific Classes, Levels, and Skills with chapter references
- Live total-stat counter for: total current word count, average count per chapter, 
  number of chapters

CURRENT TO-DO:
1. Speed up process of getting chapter information. The sooner this is done,
   the easier it will be to implement

2. Need to distinguish between types of bracketed references. There seem to be 2:
    - As part of a paragraph, often spoken by a character or narrated
    - Received as level-ups 'in their head' - not as part of a paragraph.
   
   The distinction here is not huge, because character level-ups are not always received
   'on screen', so both paragraph and independent references can reveal information about 
   characters not previously known. The distinction is mainly for training purposes, where
   for paragraph references we present the sentence, and for independent references we have
   the same label and example.

Documentation:
https://docs.google.com/document/d/12S1_J-qbng38_hZ9PT89PKkrwl4sMXRMc2Epe10xWfQ/edit 

"""

# REGEX
date_regex = r"(\d{4}/\d{2}/\d{2})"
url_regex = re.compile("(\d{4}/\d{2}/\d{2})")

# GLOBALS
TOC = [] 
urlTOC = 'https://wanderinginn.com/table-of-contents/'
totalWords = 0
chapsToPrint = 15 # = desired number of chapters to analyse + 1
bracketList = []

# LOCALS
chapterWords = 0
body = "stripped chapter body"

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

# Extract the body of a chapter, parse [], word-count, 'level' references, return brackets
def initial_body_anaysis(url):
    print("Analysing chapter body...")
    page = urlopen(url)
    soup3 = BeautifulSoup(page, features="lxml")
    
    # Title is stored in entry-header, body is stored in entry-content
    global body
    body = soup3.find('div', class_='entry-content').text # Extract body and remove tags

    brackets = re.findall(r'\[.*?\]', body) # Extract bracketed text from body
    
    #level = soup3.find(string=re.compile("levels")) # Extract sentences containing word 'level'
    #print(level)

    # Calculate local chapter number + running sum
    chapterWords = 0
    words = re.findall('\w+', body)
    chapterWords = len(words)
    print(chapterWords, "words")
    global totalWords
    totalWords += chapterWords

    # Source for finding out how to extract body text
    # https://stackoverflow.com/questions/49205608/how-can-i-extract-the-text-part-of-a-blog-page-while-web-scraping-using-beautifu
        
    return brackets

# Extract the body of a chapter, get sentences with [], return
def training_data_extraction(url):
    print("Extract training data...\n")
    
    global body

    bracketReferences = re.findall(r"([^!?.]*\[.*?\][^.!?]*\.)", body)
    for ref in bracketReferences:
        print("%s\n", ref)

    """ Libraries, Training Data, Examples
    Stanford includes job title recognition, but this looks a bit rough (no real occupation support):
    http://corenlp.run/ -- soldier is recognised, but Mage is not, nor Necromancer, though they are also
    both recognised as Proper Nouns (NNP in Stanford NLP)

    Spacy demo:
    https://demos.explosion.ai/displacy-ent?text=Erin%20stood%20in%20front%20of%20the%20cupboard%20and%20sighed.%20Loudly.%0A%0A%E2%80%9CMen.%E2%80%9D%0A%0AErin%20paused%20and%20thought%20about%20that%20word.%0A%0A%E2%80%9CMales.%20They%20eat%20and%20eat%2C%20and%20eat.%20And%20then%20I%20have%20to%20clean%20up%20the%20dishes.%20Typical.%E2%80%9D%0A%0ATrue%2C%20she%20was%20an%20innkeeper.%20Or%20at%20least%2C%20she%20kept%20an%20inn%20relatively%20clean.%20But%20that%20didn%E2%80%99t%20make%20her%20feel%20better.%0A%0A%E2%80%9CPantry%3F%20Pantry%20is%20empty.%20Food%3F%20Food%20is%20gone.%20And%20money%E2%80%94%E2%80%9D%0A%0AErin%20glanced%20at%20the%20pile%20of%20coins%20on%20the%20kitchen%20counter.%0A%0A%E2%80%9CMoney%20is%20shiny.%20But%20uh%2C%20inedible.%20And%20it%E2%80%99s%20good%20to%20have%20money%2C%20but%20starvation%20is%20an%20issue.%E2%80%9D%0A%0AErin%20stared%20at%20the%20empty%20pantry.%20Starvation%20was%20a%20major%20issue.%0A%0A%E2%80%9CAren%E2%80%99t%20there%20some%20more%20blue%20fruits%20around%20here%3F%20Here%3F%20No%E2%80%A6here%3F%20Yep.%20Nice%20and%20wrinkled.%20Lovely.%E2%80%9D%0A%0AShe%20could%20always%20get%20more%20blue%20fruits%2C%20of%20course.%20But%20there%20was%20a%20limit%20on%20how%20many%20those%20trees%20had%20left.%20And%20there%20was%20also%20a%20limit%20to%20how%20many%20Erin%20was%20willing%20to%20keep%20hauling%20back.%0A%0A%E2%80%9CAnd%20I%E2%80%99m%20out%20of%20ingredients.%E2%80%9D%0A%0AThe%20flour%20was%20gone.%20The%20butter%20was%20gone.%20The%20salt%E2%80%94okay%2C%20there%20was%20some%20salt%20left%2C%20and%20some%20sugar%20too.%20But%20they%20were%20running%20low%20in%20their%20bags%20and%20with%20the%20lovely%20preservation-spell-thing%20gone%20they%E2%80%99d%20probably%20turn%20rotten%20sometime%20soon.%0A%0A%E2%80%9CSo%20I%E2%80%99m%20in%20trouble.%E2%80%9D%0A%0A%E2%80%9CSo%20it%20would%20appear.%E2%80%9D%0A%0AErin%20was%20sure%20her%20heart%20stopped%20for%20a%20good%20few%20seconds.%20She%20turned%20around%20and%20looked%20at%20Pisces.%0A%0A%E2%80%9CIf%20I%20had%20a%20knife%20in%20my%20hand%2C%20I%E2%80%99d%20stab%20you.%E2%80%9D%0A%0AHe%20smirked%20at%20her.%20It%20seemed%20to%20be%20his%20default%20mode%20of%20face.%0A%0A%E2%80%9CAh%2C%20but%20what%20good%20innkeeper%20would%20deprive%20herself%20of%20such%20a%20magnificent%20guest%3F%E2%80%9D%0A%0AErin%20reached%20for%20a%20knife.%0A%0A%E2%80%9CPlease%2C%20please%20good%20mistress%2C%20let%E2%80%99s%20not%20be%20hasty!%E2%80%9D%0A%0APisces%20raised%20his%20hands%20quickly%20and%20took%20a%20few%20steps%20back.%20Erin%20glared%20at%20him.%20He%20looked%20dusty.%20And%20dirty.%20And%20sweaty.%0A%0A%E2%80%9CWhere%20did%20you%20come%20from%3F%20I%20didn%E2%80%99t%20hear%20you%20come%20in%20through%20the%20door.%E2%80%9D%0A%0A%E2%80%9CI%20was%2C%20in%20fact%2C%20upstairs%20the%20entire%20time.%20It%20was%20the%20simplest%20solution%20given%20the%20intelligence%20of%20those%20two%20brutish%20guardsmen.%E2%80%9D%0A%0AErin%20blinked.%0A%0A%E2%80%9CGood%20job%2C%20I%20guess.%20But%20they%E2%80%99re%20still%20going%20to%20find%20you.%20You%E2%80%99re%20a%20criminal%20and%20you%E2%80%99ve%20got%20nowhere%20to%20hide.%E2%80%9D%0A%0A%E2%80%9CExcept%20here.%E2%80%9D%0A%0AHe%20raised%20a%20hand%20before%20Erin%20could%20say%20anything.%0A%0A%E2%80%9CPlease%2C%20hear%20me%20out.%20Rest%20assured%2C%20I%20bear%20you%20no%20ill%20will%20for%20reporting%20my%20actions%20to%20the%20guard.%20I%20fully%20appreciate%20the%20severity%20of%20my%20crimes%2C%20however%E2%80%94%E2%80%9D%0A%0A%E2%80%9CYou%20want%20something.%20What%3F%20To%20stay%20here%3F%20No.%20Nope.%20No%20way%20in%20hell.%E2%80%9D%0A%0A%E2%80%9CI%20assure%20you%20I%20would%20be%20a%20quite%20convivial%20guest.%20And%20I%20wouldn%E2%80%99t%20ask%20for%20much.%20In%20fact%2C%20you%20may%20be%20interested%20to%20know%20I%20am%20proficient%20in%20multiple%20schools%20of%20spellcasting.%20While%20Necromancy%20is%20a%E2%80%94passion%20of%20mine%2C%20I%20have%20extensively%20studied%20the%20elementalist%2C%20alchemical%20and%20enchanting%20schools%20of%20magic.%20My%20level%2

    Inclusion of custom training data:
    https://stackoverflow.com/questions/41400920/search-for-job-titles-in-an-article-using-spacy-or-nltk
    
    NER wishlist:
    - Names
    - Classes 
    - Skills
    - Levels
    - Approximate Location
    - Races
    - Organisations

    Spacy sample data with a custom named entity for jobs:

    TRAINING_DATA = [
        ('Who is Shaka Khan?', {
            'entities': [(7, 17, 'PERSON')]
        }),
        ('I like London and Berlin.', {
            'entities': [(7, 13, 'LOC'), (18, 24, 'LOC')]
        }),
        ('I work as software engineer.', {
            'entities': [(9, 18, 'JOBTITLE')]
        }),

    ]

    """
    
    return bracketReferences

def main():
    print("Entering main...\n")
    sortedTOC = process_toc(urlTOC)

    chapters = len(sortedTOC)
    print("Current number of chapters: ", chapters, "\n")

    """ VOLUME CHAPTER NUMBERS:
    VOLUME 1: 1 - 66 
    VOLUME 2: 67 - 122
    VOLUME 3: 123 - 174
    VOLUME 4: 175 - 236 
    VOLUME 5: 237 - 308
    VOLUME 6: 309 - 385
    VOLUME 7: 386 - 480
    VOLUME 8: 481 - 584
    VOLUME 9: 585 - 628+
    """

    # Run extraction functions and write to file
    for chapNum in range(chapsToPrint):
        title = find_title(sortedTOC[chapNum]) # Extract title

        brackets = initial_body_anaysis(sortedTOC[chapNum]) # Extract brackets
        bracketSentences = training_data_extraction(sortedTOC[chapNum]) # Extract sentences with brackets

        fileTitle = '{}.txt'.format(title) # Add title to text file
        with open(fileTitle, "w") as writeContent:
            for bracket in brackets:
                writeContent.write("%s\n" % bracket)

            for sentence in bracketSentences:
                writeContent.write("%s\n" % sentence)
            
            """
            for single, sentence in zip(brackets, bracketSentences):
                print(single, sentence)
                bracketList.append(single, sentence)
                writeContent.write("%s" % single, "%s" % sentence, "\n")
            """

        print("Processed...%s\n" % fileTitle)

    writeContent.close()
    print("Processed", chapNum, "chapters.")

    print(totalWords)
    print(bracketList)

if __name__ == "__main__":
    main()