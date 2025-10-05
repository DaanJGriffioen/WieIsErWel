from .utils import get_url_content
from models.stemming import stemmingActor as SA
import const as cs

def get_besluiten():
    today = cs.date.today()
    year = today.year
    month = today.month -1

    url =   "https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/"     + \
            "Besluit?$filter="                                          + \
            "Verwijderd eq false and "                                  + \
            "StemmingsSoort eq 'Hoofdelijk' and "                       + \
            f"year(ApiGewijzigdOp) eq {year} and "                      + \
            f"month(ApiGewijzigdOp) eq {month}"

    content = get_url_content(url, "Besluiten")
    return content

def get_headcount():
    besluiten = get_besluiten()

    for besluit in besluiten['value']:
        id = besluit['Id']
        url =   "https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/"     + \
                "Stemming?$filter="                                         + \
                "Verwijderd eq false and "                                  + \
                f"Besluit_Id eq {id}"
    
        content = get_url_content(url, "HoofdTelling")
        data = SA.stemmingActorInit(content)
        SA.save_stemming_actor(data)