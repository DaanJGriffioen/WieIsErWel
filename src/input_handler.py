from parse import parse_xml, presentie, parse_json
from get_verslagen import get_url_data, get_verslag
from datetime import date
from const import debug, docType

def aanwezigheid(datum):
    # Check if a date has been passed
    assert type(datum) == date
    # Get the document based on the date
    vergID = get_url_data(datum)
    
    if len(vergID) == 0:
        return None, None

    if debug:
        print(vergID[0])
    # Get verslag corresponding to vergID
    verslagen = get_verslag(vergID, False)

    # Extract the list of members present from the reports
    if docType == "Verslag":
        kamerleden = parse_xml(verslagen)
    elif docType == "Stemming":
        kamerleden = parse_json(verslagen)
        (verslagen)

    # Check if kamerleden has been parsed correctly
    if kamerleden == -1:
        return None, None

    # Get the present and absent members based on the current presence 
    print(f"Er zijn {len(verslagen)} {docType}en gevonden")
    aanwezig, afwezig = presentie(kamerleden, datum)

    # Add to logfile
    f = open(f"files/logs/log_{docType}_{datum}.txt", "w")
    f.write("Aanwezig:\n")
    for stri in aanwezig:
        f.write(stri + '\n')
    f.write("\nAfwezig:\n")
    for stri in afwezig:
        f.write(stri + '\n')
    f.close()

    return aanwezig, afwezig
