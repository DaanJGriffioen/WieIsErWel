from db.db_connect import get_connection

def save_kamerleden(data):
    conn = get_connection()

    cursor = conn.cursor()
    # print("got connection!")

    statement = "SELECT id FROM kamerleden"

    cursor.execute(statement)
    existing_ids = [row[0] for row in cursor.fetchall()]

    for row in data:
        try:
            if row['id'] in existing_ids:
                continue
            statement = """
            INSERT INTO kamerleden
                (id, naam, i_id, functie)
            VALUES
                (%s, %s, %s, %s)
            """

            cursor.execute(
                statement,
                (
                    row['id'],
                    row['naam'],
                    row['interne id'],
                    row['functie']
                )
            )
        except Exception as e:
            print(f"Exception! {e}")
        
    conn.commit()
    cursor.close()

def save_activiteit(data):
    conn = get_connection()

    cursor = conn.cursor()
    for row in data:
        statement = """
        INSERT INTO zaak
            (Id, Nummer, Soort, Titel, Status, Onderwerp, Organisatie, Volgnummer, Afgedaan, GewijzigdOp)
        VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
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
                row.gewijzigd_op
            )
        )
    conn.commit()
    cursor.close()