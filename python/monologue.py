import re
import requests
import random
from bs4 import BeautifulSoup

def main():
    response = requests.get("http://shakespeare.mit.edu/macbeth/full.html")
    content = response.content.replace("\n", "")
    soup = BeautifulSoup(content, "html.parser")
    all_quotes = soup.find_all('a', {"name": re.compile("speech[0-9]{1,}")})
    monologues = []
    for name in all_quotes:
        quote = name.next_sibling
        if (len(quote.findChildren()) > 4):
            text = name.text.upper() + "\n"
            for line in quote.findChildren():
                if line.name == "a":
                    text += line.text + "\n"
            monologues.append(text)

    print monologues[random.randint(0, len(monologues))]

if __name__ == '__main__':
    main()
