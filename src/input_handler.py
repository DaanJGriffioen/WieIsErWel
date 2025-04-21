from parse import parseXML, presentie, parseJson
from get_data import getUrlData, getVerslag
from datetime import date
from const import debug, docType

def aanwezigheid(datum):
    # Check if a date has been passed
    assert type(datum) == date
    # Get the document based on the date
    vergID = getUrlData(datum)
    
    if len(vergID) == 0:
        return None, None

    if debug:
        print(vergID[0])
    # Get verslag corresponding to vergID
    verslagen = getVerslag(vergID, False)

    # Extract the list of members present from the reports
    if docType == "Verslag":
        kamerleden = parseXML(verslagen)
    elif docType == "Stemming":
        kamerleden = parseJson(verslagen)

    # Check if kamerleden has been parsed correctly
    if kamerleden == -1:
        return None, None

    # Get the present and absent members based on the current presence 
    aanwezig, afwezig = presentie(kamerleden)

    # Add to logfile
    f = open(f"files/logs/log_{docType}_{datum}.txt", "a")
    f.write("Aanwezig:\n")
    for stri in aanwezig:
        f.write(stri + '\n')
    f.write("\nAfwezig:\n")
    for stri in afwezig:
        f.write(stri + '\n')
    f.close()

    return aanwezig, afwezig
