from db import db_connect as dbc

class zaak:
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


    def save_zaak(data):
        conn = dbc.get_connection()
        cursor = conn.cursor()

        for row in data:

            statement = """
            INSERT INTO zaak
                (Id, 
                Nummer, 
                Soort, 
                Titel, 
                Status, 
                Onderwerp, 
                Organisatie, 
                Volgnummer, 
                Afgedaan, 
                GewijzigdOp
            )
            VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE id = %s;
            """
            cursor.execute(
                statement,
                (
                    row.id,
                    row.nummer,
                    row.soort,
                    row.titel,
                    row.status,
                    row.onderwerp,
                    row.organisatie,
                    row.volgnummer,
                    row.afgedaan,
                    row.gewijzigd_op,
                    row.id
                )
            )
        conn.commit()
        cursor.close()

    def parse_zaken(content):
        zaken_list = []

        for element in content["value"]:
            zaken_list.append(
                zaak(
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
    
        zaak.save_zaak(zaken_list)