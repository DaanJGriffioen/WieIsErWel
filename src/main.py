from datetime import date, datetime, timedelta
from types import NoneType
from get_data import kamerleden
from visuals import makeHTML
from input_handler import aanwezigheid
from parse import debug, git
import argparse


def main():
    bereik = False
    data = []
    aanwezig = ""
    aanwezig_arr = []
    afwezig_arr = []
    
    if git:
        if(date.today().isoweekday() == 1 or date.today().isoweekday() == 7):
            print("In het weekend wordt niet vergaderd")
            exit(0)
        datum = date.today() - timedelta(days=1)
        stri = str(datum)
        aanwezig, afwezig = aanwezigheid(datum, 0)
        data.extend([stri, stri])
        print("aanwezigen: ", aanwezig)
        print("afwezigen: ", afwezig)

        if(type(aanwezig) == NoneType):
            print("geen aanwezigen, er is iets fout gegaan wellicht is er niet vergaderd")
            exit(0)

        makeHTML(aanwezig, afwezig, data)
        return

    stri = input("1: Zelf datum opgeven \n2: Bereik van data:\n")
    if int(stri) == 1:
        stri = input("Geef een datum op (YYYY-MM-DD): ")
        # Check de invoer voor yyyy-mm-dd
        assert stri.split('-')[0].__len__() == 4
        assert stri.split('-')[1].__len__() == 2
        assert stri.split('-')[2].__len__() == 2
        datum = date.fromisoformat(stri)
        if date.today() < datum:
            print("Kan niet in de toekomst kijken")
            exit(0)
        aanwezig, afwezig = aanwezigheid(datum)

        # Als er niemand is, stoppen
        if type(aanwezig) == type(None) or type(afwezig) == type(None):
            print("Geen aanwezigen / afwezigen")
            exit(0)

        data.extend([stri, stri])

    # Bereik van data
    elif int(stri) == 2:
        data = []
        bereik = True
        str1 = input("Geef een eerste datum op (YYYY-MM-DD): ")
        str2 = input("Geef een tweede datum op (YYYY-MM-DD): ")

        assert str1.split('-')[0].__len__() == 4
        assert str1.split('-')[1].__len__() == 2
        assert str1.split('-')[2].__len__() == 2
        datum1 = date.fromisoformat(str1)

        assert str2.split('-')[0].__len__() == 4
        assert str2.split('-')[1].__len__() == 2
        assert str2.split('-')[2].__len__() == 2
        datum2 = date.fromisoformat(str2)
        data.extend([str1, str2])
        

        if date.today() < datum2:
            print("Kan niet in de toekomst kijken, misschien een volgende update :)")
            exit(0)


        # Bereken het verschil tussen de datums
        delta = datum2 - datum1

        # Op zaterdagen en zondagen wordt er niet gedebatteerd
        for _ in range(delta.days):
            datum1 += timedelta(days=1)
            if datum1.isoweekday == 6 or datum1.isoweekday == 7:
                continue

            if(datum1 == date.today()):
                print("Verslag van vandaag is er waarschijnlijk niet, dus deze wordt niet gezocht")
                continue

            aanwezig, afwezig = aanwezigheid(datum1)
            if type(aanwezig) == type(None) or type(afwezig) == type(None):
                continue

            aanwezig_arr += aanwezig
            afwezig_arr += afwezig
        else:
            print("Verkeerde invoer")
        bezig = True
        
        # Wachten op antwoord waar we iets mee kunnen
        
    while bezig:
        stri = input("HTML maken? j/n: \n")
        if stri == "j" or stri == "J":
            if bereik: makeHTML(aanwezig_arr, afwezig_arr, data)
            else: makeHTML(aanwezig, afwezig, data)
            bezig = False
        elif stri == "n" or stri == "N":
            bezig = False
        else:
            print("Invoer is j/n")
        

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Set debug mode for printing")
    parser.add_argument("--debug", default=False, type=bool, metavar=debug,
        help="Set debug to True if you want to see the output of\
        the getting and parsing process")
    parser.add_argument("--git", default=False, type=bool, metavar=debug,
        help="Used when run on github pages to make nice table!")
    args = parser.parse_args()
    debug = args.debug
    git = args.git

    kamerleden()
    main()
