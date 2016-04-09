#try:
import urllib.request as urllib
#except ImportError:
#    import urllib2
from multiprocessing.dummy import Pool as ThreadPool
from html.parser import HTMLParser
import pdb

from lxml import html
import requests
import sys

#from oauth2client.client import flow_from_clientsecrets

#flow = flow_from_clientsecrets('./client_secrets.json',
#                               scope='https://www.googleapis.com/auth/calendar',
#                               redirect_uri='http://example.com/auth_return')

#auth_uri = flow.step1_get_authorize_url()

#auth_response = requests.get(auth_uri)
import pprint

from apiclient.discovery import build

namesFile = open(sys.argv[1])
keywords_input = open(sys.argv[2])
keywords = []

for word in keywords_input :
    keywords.append(word)


# Open file for writing the results
filename = "Results.txt"
target = open(filename, 'w')

paperList = []

for name in namesFile:
    print(name)
    target.write(name.strip())
    target.write("\nResearch Papers:")
    service = build("customsearch", "v1", developerKey="AIzaSyCbyFJHL8l2p-DdCGnd92rAhVF9SQzdjoI")

    res = service.cse().list(
      q=name,
      cx='018078494062619471299:7nycalkac1w',
    ).execute()

    #cx='017576662512468239146:omuauf_lfve',
    #pdb.set_trace()
    pprint.pprint(res['items'][0]['title'])

    # for each paper find search for each keyword
    #pdb.set_trace()
    for paper in res['items'][0]['pagemap']['scholarlyarticle'] :

        for keyword in keywords :
            #print(keyword)
        #    pdb.set_trace()
            if keyword.strip().lower() in paper['name'].lower() :
                pprint.pprint(paper)
                paperTuple = [paper, keyword]
                paperList.append(paperTuple)
                target.write(paper['name'])
                target.write("\n")
                #pdb.set_trace()
                break

    target.write("\n")

target.close()

pdb.set_trace()

#page = requests.get('http://dblp.uni-trier.de/pers/hd/l/Liu:Tongping')
#tree = html.fromstring(page.content)
# Get paper names
#paperTitles = tree.xpath('//span[@class="title"]/text()')

#import webbrowser
#import os

#webbrowser.open('file://' + os.path.realpath("results.html"));

#pdb.set_trace()


# Make the Pool of workers
#pool = ThreadPool(4)
# Open the urls in their own threads
# and return the results
#results = pool.map(urllib.urlopen, urls)
#close the pool and wait for the work to finish
#pool.close()
#pool.join()
