from db import db_connect as dbc

class zaakActor:
    def __init__(self, zaak_id, actor_naam, relatie, interne_id, pers_id, api_gew):
        
        self.zaak_id =          zaak_id
        self.actor_naam =       actor_naam
        self.relatie =          relatie
        self.interne_id =       interne_id
        self.pers_id =          pers_id
        self.api_gew =          api_gew

    def zaakInit(objects):
        zaak_actor_arr = []
        if objects == None:
            return zaak_actor_arr
        
        for object in objects:
            zaak_actor_arr.append(
                zaakActor(
                    zaak_id=            object[0],
                    actor_naam=         object[1],
                    relatie=            object[2],
                    interne_id=         object[3],
                    pers_id=            object[4],
                    api_gew=            object[5]
                )
            )
        return zaak_actor_arr

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
                    zaak_id=element["Zaak_Id"],
                    actor_naam=element["ActorNaam"],
                    relatie=element["Relatie"],
                    interne_id=element["SidActor"],
                    pers_id=element["Persoon_Id"],
                    api_gew=element["ApiGewijzigdOp"]
                )
            )
        
        zaakActor.save_zaak_actor(zaak_actor_list)
    
    def get_zaak_actor_pers_id(id):
        try:
            conn = dbc.get_connection()
            cursor = conn.cursor()

            statement = f"""
            SELECT * FROM zaak_actor WHERE pers_id = '{id}';
            """

            cursor.execute(statement)
            result = cursor.fetchall()
            cursor.close()
            return result

        except Exception as e:
            print(f"Exception! {e}")