import os
import requests
from bs4 import BeautifulSoup
from pprint import pprint
import pickle
 
def grab(letter):
    # Grabs spellings from Wikipedia
 
    url = "http://en.wikipedia.org/wiki/Wikipedia:Lists_of_common_misspellings/%s" % letter
    html = requests.get(url).content
    soup = BeautifulSoup(html)
    bullets = soup.findAll('li')
#   print type(bullets)
#   print len(bullets)
    retval ={}
    for bullet in bullets:
        #repr to return a printable str representation of the object bullet
        if 'plainlinks' in repr(bullet):
            values = bullet.text.split('(')
            print bullet.text
            if ' ' in values[1]:
                continue
            if len(values) == 2:
                retval[values[0]] = values[1][:-1]
    return retval
 
def get_spellings():
    if not os.path.exists('words.pkl'):
        retval = {}
        for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            print 'Getting typos for the letter - %s' % c
            retval.update(grab(c))
        print 'Dumping...'
        # use pickle to dump objects to a file
        with open('words.pkl', 'w') as f:
            pickle.dump(retval, f)
 
        return retval
 
    else:
        # open an already stored data
        with open('words.pkl', 'r') as f:
            retval = pickle.load(f)
 
        return retval
