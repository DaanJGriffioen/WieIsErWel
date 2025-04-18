from const import docType
import requests as req
import json
from datetime import date, timedelta


def getVerslag(vergID):
    r = []
    count = 0
    for i in range(len(vergID)):
        url = f"https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/{docType}/{vergID[i]}/resource"
        print(url)
        try:
            r.append(req.get(url))
        except:
            print("Error getting url")
            exit(1)

    return r


def getURLContent(datum):
    year = datum.year
    month = datum.month
    day = datum.day

    url = f"https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/{docType}?$filter=year(GewijzigdOp)%20eq%20{year}%20and%20month(GewijzigdOp)%20eq%20{month}%20and%20day(GewijzigdOp)%20eq%20{day}"


    r = req.get(url)

    val = json.loads(r.content)
    vergaderingen = []
    for line in val["value"]:
        if line["Verwijderd"] == False:
            vergaderingen.append(line["Id"])
    
    print(vergaderingen)
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
