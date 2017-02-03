#!/usr/bin/env python

from __future__ import print_function
import re
import requests
import random
from bs4 import BeautifulSoup

PLAY_URIS = [
    "http://shakespeare.mit.edu/macbeth/full.html",
    "http://shakespeare.mit.edu/hamlet/full.html",
    "http://shakespeare.mit.edu/allswell/full.html",
    "http://shakespeare.mit.edu/measure/full.html",
    "http://shakespeare.mit.edu/merchant/full.html",
    "http://shakespeare.mit.edu/merry_wives/full.html",
    "http://shakespeare.mit.edu/much_ado/full.html",
    "http://shakespeare.mit.edu/taming_shrew/full.html",
    "http://shakespeare.mit.edu/twelfth_night/full.html"
]

def main():
    uri = random.choice(PLAY_URIS)
    response = requests.get(uri)
    content = response.content.replace("\n", "")
    soup = BeautifulSoup(content, "html.parser")
    all_quotes = soup.find_all('a', {"name": re.compile("speech[0-9]{1,}")})
    monologues = []
    for name in all_quotes:
        quote = name.next_sibling
        if (len(quote.findChildren()) > 8):
            text = name.text.upper() + "\n"
            for line in quote.findChildren():
                if line.name == "a":
                    text += line.text + "\n"
            monologues.append(text)

    print(monologues[random.randint(0, len(monologues))])

if __name__ == '__main__':
    main()
