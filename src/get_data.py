from ast import match_case
import requests as req
import json
from datetime import date, timedelta

def getVerslag(vergID):
    r = []
    count = 0
    for i in range(len(vergID)):
        url = f"https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/Stemming/{vergID[i]}"
        try:
            r = req.get(url)
        except:
            print("Error getting url")
            exit(1)
        val = json.loads(r.content)
        print(url)
        if val["Persoon_Id"] is not None: #and val["Soort"] == "Niet deelgenomen":
            count += 1
            print(count, val["ActorNaam"], val["Soort"])

        return r


def getURLContent(datum, docType):
    year = datum.year
    month = datum.month
    day = datum.day

    # Select either a vergaderverslag or a stemminguitslag
    match docType:
        case 0:
            url = f"https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/Verslag?$filter=year(GewijzigdOp)%20eq%20{year}%20and%20month(GewijzigdOp)%20eq%20{month}%20and%20day(GewijzigdOp)%20eq%20{day}"
        case 1:
            url = f"https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/Stemming?$filter=year(GewijzigdOp)%20eq%20{year}%20and%20month(GewijzigdOp)%20eq%20{month}%20and%20day(GewijzigdOp)%20eq%20{day}"
            
        case _:
            url = ""

    print(url)

    r = req.get(url)

    val = json.loads(r.content)
    vergaderingen = []
    for line in val["value"]:
        if line["Verwijderd"] == False:
            vergaderingen.append(line["Id"])
            
    return vergaderingen

# Get the names of the members of the parliament
def kamerleden():
    namen = ["Jong", "Bosma", "Dijck", "Dijk", "Groot", "Jansen", "Vries", "Mulder"]
    url = "https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/Persoon?$filter=Verwijderd%20eq%20false%20and%20FractieZetelPersoon/any(a:a/TotEnMet%20eq%20null)"
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
