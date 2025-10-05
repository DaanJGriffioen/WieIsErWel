from db import db_connect as dbc

class stemmingActor:
    def __init__(self, besluit_id, actorNaam, stem, pers_id, api_gew):
        self.besluit_id = besluit_id
        self.actorNaam = actorNaam
        self.stem = stem
        self.pers_id = pers_id
        self.api_gew = api_gew
    
    def stemmingActorInit(objects):
        return [stemmingActor(
            obj.get('Besluit_Id'),
            obj.get('ActorNaam'),
            obj.get('Soort'),
            obj.get('Persoon_Id'),
            obj.get('ApiGewijzigdOp')
        ) for obj in objects["value"]]


    def save_stemming_actor(data):
        conn = dbc.get_connection()
        cursor = conn.cursor()

        for row in data:
            try:
                statement = """
                    INSERT INTO stemming_actor
                    (
                        besluit_id,
                        actor_naam,
                        stem,
                        pers_id,
                        api_gew
                    )
                    VALUES (%s,%s,%s,%s,%s)
                """

                cursor.execute(
                    statement,
                    (
                        row.besluit_id,
                        row.actorNaam,
                        row.stem,
                        row.pers_id,
                        row.api_gew
                    )
                )
            except Exception as e:
                print(f"Exception saving! {e}")
        
        conn.commit()
        cursor.close()