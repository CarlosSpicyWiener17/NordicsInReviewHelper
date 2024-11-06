from pysmashgg.api import run_query
from json import loads
from queries import TOURNAMENT_ENTRANTS
from pysmashgg.exceptions import *
import time

def sortBySeed(listy):
    return listy[1]

def sortByPlacement(listy):
    return listy[2]

def sortByUpset(listy):
    return listy[3]

#Thanks crov. I changed it slightly but ukno
def SPR(seed, placement):
    """takes player seed and placement as input, gives how much upset factor"""
    import math
    seed = int(seed)
    if seed <= 1:
        seed = 0
    else:
        seed = math.floor(math.log2(seed - 1)) + math.ceil(math.log2(2 * seed / 3))

    if placement <= 1:
        placement = 0
    else:
        placement = math.floor(math.log2(placement - 1)) + math.ceil(math.log2(2 * placement / 3)) 
    
    return seed - placement 

#Filters the json data into easier to work with python data
def entrantFilter(response, infoNeeded: bool):
    event = response["data"]["event"]
    if infoNeeded:
        try:
            tournamentTime = time.localtime(event["startAt"])
        except:
            print("Tournament doesnt have start time. Enter date manually later")
            info = {
                "tournamentName" : event["tournament"]["name"],
                "year" : 2018,
                "month" : 12, 
                "day" : 7,
                "totalPages" : event["entrants"]["pageInfo"]["totalPages"]-1,
            }
        else:
            info = {
                "tournamentName" : event["tournament"]["name"],
                "year" : tournamentTime.tm_year,
                "month" : tournamentTime.tm_mon, 
                "day" : tournamentTime.tm_mday,
                "totalPages" : event["entrants"]["pageInfo"]["totalPages"]-1,
            }
    else:
        info = None
    if not event["entrants"]["nodes"][0]["standing"] == None:
        entrants = {info["name"]: {
            "ID" : info["participants"][0]["user"]["id"],
            "Seed" : info["initialSeedNum"],
            "Placement" : info["standing"]["placement"]
            } for info in event["entrants"]["nodes"]}
    else:
        entrants = {info["name"]: {
            "ID" : info["id"],
            "Seed" : info["initialSeedNum"],
            "Placement" : 0
            } for info in event["entrants"]["nodes"]}
    return entrants,info

#Calls startgg api for json data, filters and converts to python data
def getTournamentEntrants(slug: str, key: str, _auto_retry: bool = True):
    #Query setup
    query = TOURNAMENT_ENTRANTS
    variables = {"eventSlug" : slug, "page" : 1}
    header = {"Authorization" : key}

    #Run query
    try:
        response = run_query(query, variables, header, _auto_retry)
    except RequestError:
        print("Invalid or wrong key, or unknown error")
        input()
        quit()
        
    #Filter
    entrants, extraInfo= entrantFilter(response, True)

    tournamentName: str = extraInfo["tournamentName"]
    date = str(extraInfo["day"])+"/"+str(extraInfo["month"])+"/"+str(extraInfo["year"])
    pagesLeft: int = extraInfo["totalPages"]

    #Repeat till done all
    for i in range(pagesLeft):
        newVariables = {
            "eventSlug" : variables["eventSlug"],
            "page" : i+2,
        }
        response = run_query(query, newVariables, header, _auto_retry)
        new_entrants, extraInfo = entrantFilter(response, False)
        try:
            entrants.update(new_entrants)
        except:
            print("Unknown error updating entrants")
            input()
            quit()    
    
    return tournamentName, date, entrants

#Convert from python data to csv, sorted
def entrantsToCSV(tournamentName: str, date: str, entrants: dict, sortedBy: str):
    result = []

    for name, entrant in entrants.items():
        result.append([name, entrant["Seed"], entrant["Placement"], SPR(entrant["Seed"],entrant["Placement"])])
    
    if sortedBy == "SEED":
        result.sort(key=sortBySeed)
    elif sortedBy == "PLACEMENT":
        result.sort(key=sortByPlacement)
    elif sortedBy == "UPSET":
        result.sort(key=sortByUpset)

    csv = f"Name,{tournamentName},Date,{date},Type\n\nSeed,Name,Placement,Seed Performance\n"
    for listy in result:
        csv += f"{str(listy[1])},{str(listy[0])},{str(listy[2])},{str(listy[3])}\n"

    csv+="\n\n"

    return csv
