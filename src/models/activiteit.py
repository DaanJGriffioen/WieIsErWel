from db import save

class Activiteit:
    # Id, Nummer, Soort, Titel, Status, Onderwerp, Organisatie, Volgnummer, Afgedaan, GewijzigdOp
    def __init__(self, id, nummer, soort, titel, status, onderwerp, organisatie, volgnummer, afgedaan, gewijzigd_op):
        self.id = id
        self.nummer = nummer
        self.soort = soort
        self.titel = titel
        self.status = status
        self.onderwerp = onderwerp
        self.organisatie = organisatie
        self.volgnummer = volgnummer
        self.afgedaan = afgedaan
        self.gewijzigd_op = gewijzigd_op

    def parse_activiteiten(content):
        activiteiten_list = []

        for element in content["value"]:
            activiteiten_list.append(
                Activiteit(
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

        
    def get_kl_activiteit(naam):
        statement_id = f"GET id FROM kamerleden WHERE naam = {naam}"
        statement = f"GET * FROM zaak WHERE id = {statement_id}"