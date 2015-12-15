import requests
import re
from urlparse import urlparse
from bs4 import BeautifulSoup
import HTMLParser
pars = HTMLParser.HTMLParser()
def match(plink):
    f = requests.get(plink)
    data = f.text
    name = 'Prabhu Marappan'.lower()
    soup = BeautifulSoup(data,'lxml')
    data = pars.unescape(soup)
    print data
    if 'prabhu marappan' in str(soup).lower():
        print "True"
    else:
        print "False"

match('https://www.linkedin.com/in/prabhumarappan')
