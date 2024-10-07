from NIRext import *

def convertToSlug(eventLink: str):
    """Converts an entire link to a usable event slug for start.gg"""

    startOfSlug: int = eventLink.find("start.gg/") + 9
    eventMark: int = eventLink.find("/event/") + 7
    endOfSlug: int = eventLink.find("/",eventMark)
    if endOfSlug == -1:
        endOfSlug = len(eventLink) + 1

    if startOfSlug == -1 or eventMark == -1:
        return None
    return eventLink[startOfSlug:endOfSlug]

def getKey():
    #Was planning to have a file with .txt to input into
    print("Insert key:")
    key = input()
    return f'Bearer {key}'

def getLink():
    ##Simply
    linkSuccess = False
    while not linkSuccess:
        print('Input tournament link, or type "done" to finish:')
        tournamentLink : str = input().lower()
        if tournamentLink == "done":
            return False
        slug = convertToSlug(tournamentLink)
        if slug == None:
            print("Not a valid link. Try again")
        elif isinstance(slug,str):
            print("Success")
            return slug
        
def csvEntrants(slug, key, sorting):
    name, date, entrants = getTournamentEntrants(slug,key)
    
    csv = entrantsToCSV(name, date, entrants, sorting)

    return csv