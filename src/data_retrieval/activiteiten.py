from datetime import date
from const import pd
from models import activiteit as act
from db import save
import json
import const 


def update_activiteiten():
    print('Getting activiteiten...')
    url = f"https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/Zaak?$filter=year(GewijzigdOp) eq {date.today().year} and month(GewijzigdOp) eq {date.today().month}"
    print(url)
    try:
        r = const.req.get(url)
    except:
        print("Error getting url")
        exit(1)

    content = json.loads(r.content)

    data = act.parse_activiteiten(content)
    df = pd.DataFrame(data)
    df['date'] = date.today()
    # https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/Activiteit?$filter= year(Datum) eq 2025 and month(Datum) eq 8 and Status eq %27uitgevoerd%27