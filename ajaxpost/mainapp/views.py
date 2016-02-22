from django.shortcuts import render
from django.http import JsonResponse
import scholar, main
from fuzzywuzzy import fuzz
import crossref


def stringMatching(a,b):
    if fuzz.token_set_ratio(a,b)>=80:
        return True
    return False



def home(request):
    if request.method == 'POST':
        #POST goes here . is_ajax is must to capture ajax requests. Beginner's pit.
        if request.is_ajax():
            #Always use get on request.POST. Correct way of querying a QueryDict.
            author = request.POST.get('author')
            keywords = request.POST.get('keywords')
            ystart = request.POST.get('ystart')
            yend = request.POST.get('yend')
            count = request.POST.get('count')
            org = crossref.crossRefAPI(author,keywords,ystart,yend,count)
            authorList = org.getAuthorsORG()
            data = {}
            aolist = []
            for i in authorList:
                for k in i:
                    dup = False
                    print k[0],k[1]
                    for j in aolist:
                        if stringMatching(j['author'],k[0]):
                            print "dups"
                            dup = True
                            j['no']+=1
                            break
                    if not dup:
                        aolist.append({"author": k[0], "org" : k[1].replace("...", ""), "no" : 1})
            for i in xrange(len(aolist)):
                if (stringMatching(aolist[i]['author'],author)):
                    temp = aolist[i]
                    del aolist[i]
                    aolist.insert(0, temp)
            data["data"] = aolist
            print data
            
            
            #data = {"author":"fat" , "keywords" : keywords}
            #Returning same data back to browser.It is not possible with Normal submit
            return JsonResponse(data)
    return render(request,'index.html')


