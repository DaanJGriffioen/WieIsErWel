import pandas as pd
from const import kamerleden_dir, req
from datetime import timedelta, date
import os
from db import db_connect as dbc


class Kamerlid:
    # Naam, id, interne id en functie
    def __init__(self, naam, id, i_id, functie):
        self.naam = naam
        self.id = id
        self.i_id = i_id
        self.functie = functie
    
    # Haal de vooropgehaalde lijst met kamerleden op
    def laad_kamerleden(datum):
        filename = f"files/kamerleden/{datum}"
        if os.path.exists(filename):
            print("Actuele kamerverdeling gevonden!")
            f = open(filename, "r")
            return f
        else:
            print("Geen actuele zetelverdeling, op zoek naar de dichtsbijzijnde")
            minDelta = -timedelta(weeks=520)
            minDatum = datum
            for file in os.listdir(kamerleden_dir):
                file_datum = date.fromisoformat(file[:-4])
                delta = datum - file_datum
                if delta > minDelta:
                    minDelta = delta
                    minDatum = file_datum

            print(f"Verdeling van {minDatum} wordt gebruikt!")
            f = open(f"{kamerleden_dir}{minDatum}.txt", "r")
            return f


    def save_kamerleden(data):
        conn = dbc.get_connection()

        cursor = conn.cursor()

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
        
