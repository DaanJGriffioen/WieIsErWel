from db import db_connect as dbc

class zaakActor:
    def __init__(self, actor_id, zaak_id, actor_naam, relatie, intern_id, pers_id, api_gew):
        self.actor_id = actor_id
        
        self.zaak_id = zaak_id
        self.actor_naam = actor_naam
        self.relatie = relatie
        self.interne_id = intern_id
        self.pers_id = pers_id
        self.api_gew = api_gew


    def save_zaak_actor(data):
        conn = dbc.get_connection()
        cursor = conn.cursor()
        for row in data:
            try:
                statement = """
                INSERT INTO zaak_actor 
                (
                    zaak_id,
                    actor_naam,
                    relatie,
                    interne_id,
                    pers_id,
                    api_gew
                )
                VALUES (%s,%s,%s,%s,%s,%s)
                ON DUPLICATE KEY UPDATE zaak_id = %s;
                """
                cursor.execute(
                    statement,
                    (
                        row.zaak_id,
                        row.actor_naam,
                        row.relatie,
                        row.interne_id,
                        row.pers_id,
                        row.api_gew,
                        row.zaak_id
                    )
                )
            except Exception as e:
                print(f"Exception! {e}")

        conn.commit()
        cursor.close()

    def parse_zaak_actor(content):
        zaak_actor_list = []

        for element in content["value"]:
            
            zaak_actor_list.append(
                zaakActor(
                    actor_id=element["Id"],
                    zaak_id=element["Zaak_Id"],
                    actor_naam=element["ActorNaam"],
                    relatie=element["Relatie"],
                    intern_id=element["SidActor"],
                    pers_id=element["Persoon_Id"],
                    api_gew=element["ApiGewijzigdOp"]
                )
            )
        
        zaakActor.save_zaak_actor(zaak_actor_list)