

class Activiteit:
    # Id, onderwerp, soort, datum, status
    def __init__(self, id, onderwerp, soort, datum, kamer, start_t, eind_t, v_id, v_Sid, v_naam, VRS):
        self.id = id
        self.soort = soort
        self.aanvangstijd = start_t
        self.eindtijd = eind_t
        self.onderwerp = onderwerp
        self.datum = datum
        self.kamer = kamer
        self.idVoortouw = v_id
        self.SidVoortouw = v_Sid
        self.voortouwNaam = v_naam
        self.vrs = VRS

        
    def get_kl_activiteit(naam):
        statement_id = f"GET id FROM kamerleden_tabel WHERE naam = {naam}"
        statement = f"GET * FROM activiteiten_tabel WHERE id = {statement_id}"