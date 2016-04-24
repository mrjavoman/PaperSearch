import pdb
import sys
import json
import pprint
from multiprocessing.dummy import Pool as ThreadPool
from apiclient.discovery import build

#--------------------------------------------------------
# Function for querying results
#--------------------------------------------------------
def queryGoogleApi(name, service) :

    paperList = []

    res = service.cse().list(
      q=name,
      cx=config_data["searchApi"]["customsearchID"],
    ).execute()

    #pdb.set_trace()
    pprint.pprint(res['items'][0]['title'])
    paperList.append({"researcher": res['items'][0]['title'],"paper": "NotFound", "keyword": "NotFound"})
    # for each paper find search for each keyword
    for paper in res['items'][0]['pagemap']['scholarlyarticle'] :
        for keyword in keywords :
            if keyword.strip().lower() in paper['name'].lower() :
                pprint.pprint(paper)
                paperTuple = {"researcher": res['items'][0]['title'],"paper": paper, "keyword": keyword.strip()}
                paperList.append(paperTuple)
                break

    paperList.append({"researcher": "","paper": "", "keyword": "separator"})

    return paperList

#--------------------------------------------------------
# Function for outputing results
#--------------------------------------------------------
def outputResults(output_filename, paperList) :

    target = open(output_filename, 'w')
    currResearcher = ""

    for entry in paperList :
        if entry["paper"] == "" :
            target.write("---------------------------------------------------------\n")
        else :
            if(currResearcher != entry["researcher"]) :
                currResearcher = entry["researcher"]
                target.write(entry["researcher"] + "\n")
                target.write("---------------------------------------------------------\n")

            if(entry['paper'] != "NotFound" ) :
                target.write("Article: " + entry['paper']['name'] + "\n")
                target.write("Keyword: " + entry['keyword'] + "\n\n")


    target.close()

#--------------------------------------------------------
# Main
#--------------------------------------------------------
# Get configuration file
with open('config.json') as data_file:
    config_data = json.load(data_file)

# Open input files
namesFile = open(sys.argv[1])
keywords_input = open(sys.argv[2])

# Variables
keywords = []
paperList = []
output_filename = "Results.txt"

# Get keywords from input file into a resuable array
for word in keywords_input :
    keywords.append(word)

# Open google api service
service = build(config_data["searchApi"]["type"], config_data["searchApi"]["version"], developerKey=config_data["searchApi"]["developerKey"])

# Process each researcher name and call google api
for name in namesFile:
    paperList.extend(queryGoogleApi(name, service))

# Output results
outputResults(output_filename, paperList)

#page = requests.get('http://dblp.uni-trier.de/pers/hd/l/Liu:Tongping')
#tree = html.fromstring(page.content)
# Get paper names
#paperTitles = tree.xpath('//span[@class="title"]/text()')

#webbrowser.open('file://' + os.path.realpath("results.html"));


# Make the Pool of workers
#pool = ThreadPool(4)
# Open the urls in their own threads
# and return the results
#results = pool.map(urllib.urlopen, urls)
#close the pool and wait for the work to finish
#pool.close()
#pool.join()
