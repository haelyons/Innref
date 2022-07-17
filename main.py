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


# Get link from a specific page and find title
url = "https://wanderinginn.com/2016/08/07/1-03/"
chapter_page = urlopen(url)
html_bytes = chapter_page.read()
html = html_bytes.decode("utf-8")
soup = BeautifulSoup(html, "html.parser")
# <article class ="post-1910 page type-page status-publish hentry" id="post-1910"> = $0


# Extract chapter code (1.03)
title = soup.title.string
chapter_code = re.findall("\d+\.\d+", title)
print(chapter_code)


# Extract class references
body = soup.get_text()
classes = re.findall(r'\[.*?\]', body)
print(classes)


"""
# DEFAULT PARSER IMPLEMENTATION
title_index = html.find("<h1 class=\"entry-title\">")
start_title_index = title_index + len("<h1 class=\"entry-title\">")
end_title_index = html.find("</h1>")
title = html[start_title_index:end_title_index]

print(title)

body_index = html.find("<div class=\"entry-content\">")
start_body_index = body_index + len("<div class=\"entry-content\">")
end_body_index = html.find("</div>")
body = html[start_body_index:end_body_index]

print(body)
"""

# Open downloaded HTML file from TWI
#with open('1.03 | The Wandering Inn.html', 'r') as html_file:
#    content = html_file.read()
#
#    # Instantiate new BeautifulSoup library for parsing with LXML
#    soup = BeautifulSoup(content, 'lxml')
#    class_bell = soup.find_all('p')
#    for class_list in class_bell:
#        print(class_bell)
#
#    parse('1.03 | The Wandering Inn.html')