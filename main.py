from ast import parse
from bs4 import BeautifulSoup

# Open downloaded HTML file from TWI
with open('1.03 | The Wandering Inn.html', 'r') as html_file:
    content = html_file.read()

    # Instantiate new BeautifulSoup library for parsing with LXML
    soup = BeautifulSoup(content, 'lxml')
    class_bell = soup.find_all('p')
    for class_list in class_bell:
        print(class_bell)

    parse('1.03 | The Wandering Inn.html')