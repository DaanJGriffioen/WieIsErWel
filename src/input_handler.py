from parse import parseXML, extractID, presentie
from get_data import getURLContent, getVerslag
from datetime import date
from const import  debug

def aanwezigheid(datum):
    # Check if a date has been passed
    assert type(datum) == date
    # Get the document based on the date
    vergID = getURLContent(datum)
    # Haal de vergaderID uit het verslag
    # vergID = extractID(content)
    # If the id is 0, there is no document
    if len(vergID) == 0:
        return None, None

    if debug:
        print(vergID[0])
    # Haal het verslag op a.h.v. de vergaderID
    verslagen = getVerslag(vergID)
    # Haal de lijst met kamerleden uit de verslagen
    kamerleden = parseXML(verslagen)
    # Check of er wel echt iets uitgekomen is
    if kamerleden == -1:
        return None, None
    # Geef de aanwezigen terug aan de bovenliggende functie 
    aanwezig, afwezig = presentie(kamerleden)
    f = open(f"files/logs/log_{datum}.txt", "a")
    f.write("Aanwezig:\n")
    for stri in aanwezig:
        f.write(stri + '\n')
    f.write("\nAfwezig:\n")
    for stri in afwezig:
        f.write(stri + '\n')
    f.close()

    return aanwezig, afwezig
