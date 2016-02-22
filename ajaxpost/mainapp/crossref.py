import json
import scholar
from bs4 import BeautifulSoup
import urllib2
import unicodedata
from collections import OrderedDict
from fuzzywuzzy import fuzz
import re

def stringMatching(a,b):
    if fuzz.token_set_ratio(a,b)>=80:
        return True
    return False

class crossRefAPI(object):
    def __init__(self, author = None, keywords = None, ystart = None, yend = None, count = None):
        self.authorList = []
        self.author = author
        self.keywords = keywords
        self.ystart = ystart
        self.yend = yend
        self.count = count
    
    def getAuthorsORG(self):
        queryUrl = "http://api.crossref.org/works?query=" + self.keywords.replace(" ","+") + "+" + self.author.replace(" ","+") + "&rows=" + str(self.count) + "&filter=from-pub-date:" + str(self.ystart) + "-01-01,until-pub-date:" + str(self.yend) + "-12-31"
        response = urllib2.urlopen(queryUrl)
        data = json.loads(response.read())
        authorInArtical = 0
        for i in xrange(0, min(len(data['message']['items']),self.count)):
            try:
                tempList = []
                pubUnicode = data['message']['items'][i]['title'][0]
                pubName = unicodedata.normalize('NFKD', pubUnicode).encode('ascii', 'ignore')
                print str(i)+pubName

                pubName.replace(" ", "+")
                pubSearchUrl = "https://www.researchgate.net/publicliterature.PublicLiterature.search.html?type=keyword&search-keyword=" + pubName.replace(" ", "+") + "&search-abstract=&search=Search"
                searchPage = urllib2.urlopen(pubSearchUrl)
                soupPub = BeautifulSoup(searchPage)
                pubUrl = "https://www.researchgate.net/" + soupPub.select(".ga-publication-item")[0]['href']
                pubPage = urllib2.urlopen(pubUrl)
        
                soupPub = BeautifulSoup(pubPage)
                for j in xrange(0, len(soupPub.select(".ga-top-coauthor-name"))):
                    authorUrl = "https://www.researchgate.net/" + soupPub.select(".ga-top-coauthor-name")[j].a['href']
                    pageAuthor = urllib2.urlopen(authorUrl)
                    soupAuthor = BeautifulSoup(pageAuthor)
                    tempList.append([unicodedata.normalize('NFKD',soupPub.select(".ga-top-coauthor-name")[j].text.strip()).encode('ascii', 'ignore'),unicodedata.normalize('NFKD', soupAuthor.select(".header-institution-name")[0].text.strip()).encode('ascii', 'ignore')])
                    if stringMatching(self.author,unicodedata.normalize('NFKD',soupPub.select(".ga-top-coauthor-name")[j].text.strip()).encode('ascii', 'ignore')):
                        authorInArtical = 1
                    else:
                        print unicodedata.normalize('NFKD',soupPub.select(".ga-top-coauthor-name")[j].text.strip()).encode('ascii', 'ignore')
            except:
                print "Not found"
                continue
            
            if authorInArtical>0:
                authorInArtical = 0
                self.authorList.append(tempList)
                print "In" + str(len(tempList))
            elif authorInArtical<=-10:
                return self.authorList
            else:
                authorInArtical-=1
        return self.authorList

