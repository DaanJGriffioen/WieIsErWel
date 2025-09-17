from datetime import date
from models.zaak_actor import zaakActor as ZA
import json
import const 


def update_zaak_actor():
    print('Getting zaak actors...')

    today = date.today()
    year = today.year
    month = today.month
    
    
    url = "https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/"   + \
            "ZaakActor?$filter="                                    + \
            "Verwijderd eq false and "                              + \
            "functie eq 'Tweede Kamerlid' and "                     + \
            f"year(ApiGewijzigdOp) eq {year} and "                  + \
            f"month(ApiGewijzigdOp) eq {month}"

    print(url)
    try:
        r = const.req.get(url)
    except:
        print("Error getting url")
        exit(1)
    

    content = json.loads(r.content)
    data = ZA.parse_zaak_actor(content)

    # data = ZK.parse_zaken(content)
    # df = pd.DataFrame(data)
    # df['date'] = date.today()
    # https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/zaak?$filter= year(Datum) eq 2025 and month(Datum) eq 8 and Status eq %27uitgevoerd%27