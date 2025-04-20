from curses.ascii import BEL
from types import NoneType
from const import docType
import requests as req
import json
from datetime import date, timedelta
            

def getVerslag(vergID, stemmingData):
    data = []
    count = 0
    for id in vergID:
        if docType == "Verslag":
            url = f"https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/{docType}/{id}/resource"
        elif docType == "Stemming":
            url = f"https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/Stemming?$filter=Besluit_Id%20eq%20{id}"

        print(url)
        try:
            data.append(req.get(url))
        except:
            print("Error getting url")
            exit(1)

    return data

# Gets data for docType from date `datum`
def getUrlData(datum):
    year = datum.year
    month = datum.month
    day = datum.day
    
    url = f"https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/{docType}?$filter=year(GewijzigdOp)%20eq%20{year}%20and%20month(GewijzigdOp)%20eq%20{month}%20and%20day(GewijzigdOp)%20eq%20{day}"

    try:
        r = req.get(url)
    except:
        print("Error getting url")
        exit(1)

    print(url)
    val = json.loads(r.content)

    vergaderingen = []
    for line in val["value"]:
        if docType == "Stemming" and line["Persoon_Id"] is None:
            continue
        if docType == "Verslag" and line["Verwijderd"] == False:
            vergaderingen.append(line["Id"])
        elif docType == "Stemming" and line["Verwijderd"] == False:
            if line["Besluit_Id"] not in vergaderingen:
                vergaderingen.append(line["Besluit_Id"])
            
    return vergaderingen


# Get the names of the members of the parliament
def kamerleden():
    namen = ["Jong", "Bosma", "Dijck", "Dijk", "Groot", "Jansen", "Vries", "Mulder"]
    url = "https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/Persoon?$filter=Verwijderd%20eq%20false%20and%20FractieZetelPersoon/any(a:a/TotEnMet%20eq%20null)"
    print(url)
    r = req.get(url)
    content = json.loads(r.content)
    f = open("files/2dekmrledn2.txt", "w")
    for item in content["value"]:
        naam = ""
        if item["Achternaam"] in namen:
            if item["Roepnaam"] != "Jimmy":
                naam += item["Roepnaam"].lower().replace(" ","")
        if item["Tussenvoegsel"] != None:
            naam += item["Tussenvoegsel"].replace(" ","")
        naam += item["Achternaam"].lower().replace(" ","")
        f.write(naam+"\n")
    f.close()
