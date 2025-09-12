from datetime import date
from const import pd
from models import activiteit
from db import save
import json
import const 

def parse_activiteiten(content):
    activiteiten_list = []

    for element in content["value"]:
        activiteiten_list.append(
            activiteit.Activiteit(
                id=element["Id"],
                nummer=element["Nummer"],
                soort=element["Soort"],
                titel=element["Titel"],
                status=element["Status"],
                onderwerp=element["Onderwerp"],
                organisatie=element["Organisatie"],
                volgnummer=element["Volgnummer"],
                afgedaan=element["Afgedaan"],
                gewijzigd_op=element["GewijzigdOp"]
            )
        )
    
    print(activiteiten_list)
    save.save_activiteit(activiteiten_list)


def update_activiteiten():
    print('Getting activiteiten...')
    url = f"https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/Zaak?$filter=year(GewijzigdOp) eq {date.today().year} and month(GewijzigdOp) eq {date.today().month} and Soort eq 'Motie'"
    print(url)
    try:
        r = const.req.get(url)
    except:
        print("Error getting url")
        exit(1)

    content = json.loads(r.content)

    data = parse_activiteiten(content)
    df = pd.DataFrame(data)
    df['date'] = date.today()
    # https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/Activiteit?$filter= year(Datum) eq 2025 and month(Datum) eq 8 and Status eq %27uitgevoerd%27