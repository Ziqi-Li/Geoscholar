#! /usr/bin/env python

import scholar
from bs4 import BeautifulSoup
import urllib2
import unicodedata
from collections import OrderedDict
from fuzzywuzzy import fuzz

def stringMatching(a,b):
    if fuzz.token_set_ratio(a,b)>=80:
        return True
    return False

def merge_two_dicts(x, y):
    '''Given two dicts, merge them into a new dict as a shallow copy.'''
    z = x.copy()
    z.update(y)
    return z

class ScholarOrg(object):
    def __init__(self, author = None, keywords = None, ystart = None, yend = None, count = None):
        self.authorList = []
        self.author = author
        self.keywords = keywords
        self.ystart = ystart
        self.yend = yend
        self.count = count
    
    def getAuthorsORG(self):
        query = scholar.SearchScholarQuery()
        query.set_author(self.author)
        query.set_phrase(self.keywords)
        query.set_timeframe(self.ystart, self.yend)
        query.set_num_page_results(self.count)
        query.set_include_patents(False)
        query.set_include_citations(False)
        query.set_scope(True)
        querier = scholar.ScholarQuerier()
        settings = scholar.ScholarSettings()
        settings.set_citation_format(scholar.ScholarSettings.CITFORM_BIBTEX)
        querier.apply_settings(settings)
        querier.send_query(query)
        print "Query Sent"
        for i in xrange(0, min(len(querier.articles),self.count)):
            tempList = []
            print str(i)+"processed"
            pubUnicode = querier.articles[i].attrs['title'][0]
            pubName = unicodedata.normalize('NFKD', pubUnicode).encode('ascii', 'ignore')
            pubName.replace(" ", "+")
            pubSearchUrl = "https://www.researchgate.net/publicliterature.PublicLiterature.search.html?type=keyword&search-keyword=" + pubName.replace(" ", "+") + "&search-abstract=&search=Search"
            searchPage = urllib2.urlopen(pubSearchUrl)
            soupPub = BeautifulSoup(searchPage)
            pubUrl = "https://www.researchgate.net/" + soupPub.select(".ga-publication-item")[0]['href']
            pubPage = urllib2.urlopen(pubUrl)
            soupPub = BeautifulSoup(pubPage)
            authorInArtical = False
            for j in range(0, len(soupPub.select(".ga-top-coauthor-name"))):
                authorUrl = "https://www.researchgate.net/" + soupPub.select(".ga-top-coauthor-name")[j].a['href']
                pageAuthor = urllib2.urlopen(authorUrl)
                soupAuthor = BeautifulSoup(pageAuthor)
                tempList.append([unicodedata.normalize('NFKD',soupPub.select(".ga-top-coauthor-name")[j].text.strip()).encode('ascii', 'ignore'),unicodedata.normalize('NFKD', soupAuthor.select(".header-institution-name")[0].text.strip()).encode('ascii', 'ignore')])
                if stringMatching(self.author,unicodedata.normalize('NFKD',soupPub.select(".ga-top-coauthor-name")[j].text.strip()).encode('ascii', 'ignore')):
                    authorInArtical = True
                else:
                	print unicodedata.normalize('NFKD',soupPub.select(".ga-top-coauthor-name")[j].text.strip()).encode('ascii', 'ignore')
            if authorInArtical:
                self.authorList.append(tempList)
                print "In" + str(len(tempList))
        return self.authorList