#Import all the necessary modules
import requests
import re
from urlparse import urlparse
from bs4 import BeautifulSoup
from lxml import html
from lxml.html.clean import clean_html
from lxml.html.clean import Cleaner
import urllib2

#Input the user search parameters
name = raw_input("Enter Name: ")
college = raw_input("Enter College: ")
branch = raw_input("Enter Branch: ")
location = raw_input("Enter Loction: ")
email = raw_input("Enter Emaill: ")
phone = raw_input("Enter Phone Number: ")
# DOB = raw_input("Enter DOB: ")
# regno = raw_input("Enter College ID Number: ")

#Convert the name to be searched in the format for bing search
searchstring = re.sub(r'\s',r'+',name)
start=0

#Variable for storing the crawled links
linklist=[]
#Variable for the assessing the factors
factors = [name.lower(),location.lower(),college.lower(),phone.lower(),email.lower(),branch.lower(),phone]
#Variblae for Page Number
p=0
print "Start"

#Method for searching bing and then storing all the crawled links
def search(start):
    i=1
    global p
    p=p+1
    link = "http://www.bing.com/search?q="+searchstring+"&first="+str(start)
    f = requests.get(link)
    data = f.text
    soup = BeautifulSoup(data,'lxml')
    main = soup.find('ol',{'id':'b_results'})
    info = main.find_all('li',{'class':['b_ans','b_algo']})
    for x in info:
        i=i+1
        try:
            links = x.find('a')
            l = links['href']
            if re.search(r'^(http|https)://',l):
                linklist.append(l)
        except ValueError:
            continue
        start = start + 1
        if i==10:
            break
    if p<2:
        search(start)

#Method for retrieving the page source for the each of the pages in the linklist variable
def source():
    #Header for searching through some webpages.
    header = {'User-Agent': 'Mozilla/5.0'}
    for link in linklist:
        #Exception Handling for some links as they turn out to be Bad Requests
        try:
            request = urllib2.Request(link,headers=header)
            tree = html.parse(urllib2.urlopen(request))
            cleaner = Cleaner(scripts=True,javascript=True,style=True,links=True)
        except(ValueError,urllib2.URLError),e:
            print e.url
            print e.reason
            continue
        tree = cleaner.clean_html(tree) #Clean the Page content and remove html,js,css codes
        text = tree.getroot().text_content().encode('utf-8')
        match(text,link)

#Method for checking the factors in the page content.
def match(mtext,mlink):
    fscore = 0
    mtext1 = str(mtext).lower()
    for x in factors:
        if x in mtext1:
            fscore = fscore+1
        else:
            continue
    if fscore>=4:
        print mlink+"        "+"Yes"
    elif fscore>=3:
        print mlink+"        "+"Maybe"
    else:
        print mlink+"        "+"No"

search(0)
source()