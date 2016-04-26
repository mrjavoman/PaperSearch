import pdb
import sys
import json
import pprint
from multiprocessing.dummy import Pool as ThreadPool
from apiclient.discovery import build
from functools import partial

# Global variables
paperList = []

#--------------------------------------------------------
# Function for querying results
#--------------------------------------------------------
def queryGoogleApi(keywords, customsearchID, service, name) :

    pList = []

    res = service.cse().list(
      q=name,
      cx=customsearchID,
    ).execute()

    pprint.pprint(res['items'][0]['title'])
    pList.append({"researcher": res['items'][0]['title'],"paper": "NotFound", "keyword": "NotFound"})
    # for each paper find search for each keyword
    for paper in res['items'][0]['pagemap']['scholarlyarticle'] :
        for keyword in keywords :
            if keyword.strip().lower() in paper['name'].lower() :
                #pprint.pprint(paper)
                paperTuple = {"researcher": res['items'][0]['title'],"paper": paper, "keyword": keyword.strip()}
                pList.append(paperTuple)
                break

    pList.append({"researcher": "","paper": "", "keyword": "separator"})

    return pList

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
# Callback for collecting results
#--------------------------------------------------------
def collectResults(resrchrPapers)  :
    paperList.extend(resrchrPapers)

#--------------------------------------------------------
# Main
#--------------------------------------------------------
def main(argv) :
    # Get configuration file
    with open('config.json') as data_file:
        config_data = json.load(data_file)

    # Open input files
    namesFile = open(argv[1])
    keywords_input = open(argv[2])

    # Variables
    names = []
    keywords = []
    output_filename = "Results.txt"

    # Open google api service
    service = build(config_data["searchApi"]["type"], config_data["searchApi"]["version"], developerKey=config_data["searchApi"]["developerKey"])

    # Get keywords from input file into a resuable array
    for word in keywords_input :
        keywords.append(word)

    # Create thread pool
    pool=ThreadPool(4)
    # Setup partial function that gets passed to async function
    queryApiPartial = partial(queryGoogleApi, keywords, config_data["searchApi"]["customsearchID"], service)

    # Spawn a python thread for each name in the list and pass do a google search
    for name in namesFile:
        pool.apply_async(queryApiPartial, (name, ), callback=collectResults)

    # Close threads and join them
    pool.close()
    pool.join()

    # Output results
    outputResults(output_filename, paperList)

#--------------------------------------------------------
# Start
#--------------------------------------------------------
if __name__ == "__main__" :
    main(sys.argv)
