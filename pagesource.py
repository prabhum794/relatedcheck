from lxml import html
from lxml.html.clean import clean_html
from lxml.html.clean import Cleaner
import urllib2
def source(link):
    header = {'User-Agent': 'Mozilla/5.0'}
    request = urllib2.Request(link,headers=header)
    tree = html.parse(urllib2.urlopen(request))
    cleaner = Cleaner(scripts=True,javascript=True,style=True,links=True)
    tree = cleaner.clean_html(tree)
    text = tree.getroot().text_content().encode('utf-8')
    print text

source('https://www.linkedin.com/in/prabhumarappan')
