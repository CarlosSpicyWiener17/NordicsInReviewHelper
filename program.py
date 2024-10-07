from playerInterface import *
    


if __name__ == "__main__":
    key: str = getKey()
    doneSlugs = False
    slugs = []
    entrantText = ""
    
    #Prompt user for link. Puts the slug in a list
    while not doneSlugs:
        linkCheck = getLink()
        if not linkCheck:
            doneSlugs = True
            break
        else:
            slugs.append(linkCheck)

    print("What would you like to sort by?\n1:\tSeed\n2:\tPlacement\n3:\tSeed Performance")
    check = None

    #Get users choice. Define sorting accordingly
    while True:
        try:
            check = int(input())
        except:
            print("Try again")
        else:
            if check > 3 or check < 1:
                print("try again")
            else:
                if check == 1:
                    sorting = "SEED"
                elif check == 2:
                    sorting = "PLACEMENT"
                elif check == 3:
                    sorting = "UPSET"
                break
    
    #Iterate through all slugs and get all tournament info
    for slug in slugs:
        print("Getting tournament info...")
        entrantText += csvEntrants(slug, key, sorting)
        print("Completed")

    #Save to file
    try:
        file = open("tournamentResults.txt", "w", encoding="utf-8")
    except (IOError, OSError):
        print("Failed to create file")
    else:
        print("Saving to file...")

        try:
            file.write(entrantText)
        except:
            print("Failed to write to file")
        else:
            print("Saving file")
            try:
                file.close()
            except:
                print("Error saving")
    print("Complete!")
    input()


