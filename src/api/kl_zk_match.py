import db.db_connect as dbc

def get_zaak_per_actor(id):
    conn = dbc.get_connection()
    cursor = conn.cursor()
    try:
        statement = f"""
            SELECT zaak_id FROM zaak_actor WHERE pers_id= %s;
        """

        cursor.execute(statement, [id])

        zaak_ids = cursor.fetchall()
        print("Sucessfully fetched zaak_ids")
        
        for z_id in zaak_ids:
            statement = f"""
                SELECT * from zaak WHERE Id = %s;
            """

            cursor.execute(statement, (z_id))

            zaken = cursor.fetchall()
            print(zaken)


    except Exception as e:
        print(f"Exception when getting zaak: {e}")

