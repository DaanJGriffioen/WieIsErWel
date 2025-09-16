import const 
from models import kamerlid as kl
from const import pd
import json
from datetime import date

def parse_names(content):
    kamerleden_list = []
    # Vervelende namen die speciaal gecontroleerd moeten worden omdat ze verkeerd geparsed worden
    namen = ["Jong", "Bosma", "Dijck", "Dijk", "Groot", "Jansen", "Vries", "Mulder"]
    for _, item in enumerate(content["value"], 0):
        naam = ""
        achternaam = item["Achternaam"]
        
        # Make sure the name is formatted correctly
        if achternaam in namen:
            # Problems for Jimmy Dijk, registered as dijk
            if item["Roepnaam"] != "Jimmy":
                # Add the first name for parliamentarian if necessary
                naam += item["Roepnaam"].lower().replace(" ","")
                
        if item["Tussenvoegsel"] != None:
            # add tussenvoegsel (van / van der, etc.) if present
            naam += item["Tussenvoegsel"].replace(" ","")

        # Add last name
        naam += achternaam.lower().replace(" ","").replace("ć", "c")

        # Add ID
        naam_id = naam + " " + item["Id"]
        
        kamerleden_list.append(kl.Kamerlid(naam, item["Id"], item["Nummer"], item["Functie"]))
    
    return kamerleden_list

def write_to_logs(filename, kl_list):
    f = open(filename, 'w', encoding='utf-8')
    for kl in kl_list:
        f.write(str(kl.naam) + '\n')
    f.close()

def update_kamerleden():
    
    print("Kamerleden lijst ophalen en verwerken...")
    url = "https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/Persoon?$filter=Verwijderd%20eq%20false%20and%20FractieZetelPersoon/any(a:a/TotEnMet%20eq%20null)"
    filename = f"files/kamerleden/{date.today()}.txt"
    print(url)

    try:
        r = const.req.get(url)
    except:
        print("Error getting url")
        exit(1)

    content = json.loads(r.content)
    # if os.path.exists(filename):
    #     return

    kamerleden_list = parse_names(content)

    write_to_logs(filename, kamerleden_list)
    today = date.today()
    # Convert Kamerlid objects to dictionaries for DataFrame
    kamerleden_dicts = [
        {
            'naam': k.naam,
            'id': k.id,
            'interne id': k.i_id,
            'functie': k.functie,
            'actief': True,
            'datum': today
        }
        for k in kamerleden_list
    ]
    
    kl.Kamerlid.save_kamerleden(kamerleden_dicts)
    