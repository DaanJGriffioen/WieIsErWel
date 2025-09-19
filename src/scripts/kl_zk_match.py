from models.zaak_actor import zaakActor as ZA

def get_ZA_Pid(id):
    kamerlid = ZA.get_zaak_actor_pers_id(id)
    array = ZA.zaakInit(kamerlid)
    print(array)