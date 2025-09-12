import os
from models.kamerlid import Kamerlid as kl
from const import docType, kamerleden_dir
import requests as req
import json
from datetime import date, timedelta
            

def get_verslag(vergID, stemmingData):
    data = []
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
def get_url_data(datum):
    year = datum.year
    month = datum.month
    day = datum.day
    
    # Definieer de url van het verslag van de stemming / vergadering
    url = f"https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/{docType}?$filter=year(GewijzigdOp)%20eq%20{year}%20and%20month(GewijzigdOp)%20eq%20{month}%20and%20day(GewijzigdOp)%20eq%20{day}"

    try:
        print(f"Checking {year}/{month}/{day}")
        r = req.get(url)
    except:
        print("Error getting url")
        exit(1)

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
