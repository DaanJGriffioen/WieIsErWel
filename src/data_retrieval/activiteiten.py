from datetime import date
from const import pd
from models import zaak as act
from db import save
import json
import const 


def update_zaken():
    print('Getting zaken...')
    url = f"https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/Zaak?$filter=year(GewijzigdOp) eq {date.today().year} and month(GewijzigdOp) eq {date.today().month}"
    print(url)
    try:
        r = const.req.get(url)
    except:
        print("Error getting url")
        exit(1)

    content = json.loads(r.content)

    data = act.parse_zaken(content)
    df = pd.DataFrame(data)
    df['date'] = date.today()
    # https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/zaak?$filter= year(Datum) eq 2025 and month(Datum) eq 8 and Status eq %27uitgevoerd%27