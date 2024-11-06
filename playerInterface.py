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
        
def csvEntrants(slug, key, sorting, CompetitorIds, CompetitorNames, CompetitorNamesReduced, hasReferences):
    name, date, entrants = getTournamentEntrants(slug,key)

    if hasReferences:
        addToReference = list()
        #Check if the name is in references. Replace as needed
        replacedEntrants = dict()
        for tname, entrant in entrants.items():
            id = int(entrant["ID"])
            reducedEntrant = ''.join(filter(str.isalpha, tname))
            hasName = False
            hasId = False

            for i in range(0, len(CompetitorIds)):
                if hasId == False and (CompetitorIds[i] == id):
                    replacedEntrants.update({CompetitorNames[i]: entrant})
                    hasId = True

            if hasId == False:
                for i in range(0,len(CompetitorNamesReduced)):
                    if hasName == False and (CompetitorNamesReduced[i] in reducedEntrant.lower()):
                        replacedEntrants.update({CompetitorNames[i]: entrant})
                        hasName = True

            if hasId == False and hasName == False:
                print(f"Tournament name: {tname}")
                print(f"Could not match start.gg name to any in references")
                print("Adding new person to reference\nInput their name:")
                nameToAdd = input()
                replacedEntrants.update({nameToAdd: entrant})
                addToReference.append((nameToAdd,id))

                        
                print("\n\n")


    csv = entrantsToCSV(name, date, replacedEntrants, sorting)
    if hasReferences:
        return (csv, addToReference)
    else:
        return (csv, [])