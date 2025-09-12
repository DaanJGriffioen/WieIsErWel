

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

        
    def get_kl_activiteit(naam):
        statement_id = f"GET id FROM kamerleden WHERE naam = {naam}"
        statement = f"GET * FROM zaak WHERE id = {statement_id}"