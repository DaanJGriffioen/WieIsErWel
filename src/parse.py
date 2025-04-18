import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import json

debug = False
git = False

# Parse the XML received from the API
def parseXML(verslagen):
    next = False
    kamerleden = ""

    laatste_vers = laatste(verslagen)
    
    if laatste_vers == -1:
        return -1
    
    verslag = verslagen[laatste_vers].content.decode()
    
    try:
        root = ET.fromstring(verslag)
    except:
        raise Exception("Error parsing XML")

    # Parse XML and extract specific element
    ns = {'ns': 'http://www.tweedekamer.nl/ggm/vergaderverslag/v1.0'}
    alinea_elements    = root.findall(".//ns:alineaitem", namespaces=ns)
    if debug:
        print(type(alinea_elements))
        
    for alinea in alinea_elements:
        if next:
            kamerleden = alinea.text
            if debug:
                print("Kamerleden: ", kamerleden)
            break
        if "leden der Kamer, te weten:" in str(alinea.text):
            next = True
            
        if not next or type(kamerleden) == None:
            continue
        if type(kamerleden) == type(None):
            return -1
        # Format and transform into array
        kamerleden = kamerleden.lower().replace(" en ",",").replace(" ","").split(",")
        if debug:
            print(type(kamerleden), kamerleden)
        # Last index is invalid ez fix
        return kamerleden[:len(kamerleden)-1]


def laatste(verslagen):
    tijden = []
    max = 0
    max_element = -1
    for i in range(len(verslagen)):
        verslag = verslagen[i].content.decode()

        try:
            root = ET.fromstring(verslag)
        except:
            raise Exception("Error parsing XML")

        print("root", root[0][1] != "Plenaire zaal")
        if root[0][1].text != "Plenaire zaal" or root.attrib['soort'] == "Voorpublicatie":
            tijden.append(-1)
            continue
        
        tijden.append(root.attrib["Timestamp"].split('T')[1].split(':')[0])

    for j in range(len(tijden)):
        if int(tijden[j]) > max:
            max = int(tijden[j])
            max_element = j

        if debug:
            print(max_element, max)
        return max_element


# Get vergaderID from json
def extractID(content):
    val = json.loads(content)
    vergaderingen = []
    for line in val["value"]:
        if line["Verwijderd"] == False:
            if debug:
                print(line)
            vergaderingen.append(line["Id"])
        return vergaderingen


# Match names from present list (source) to total list (target)
def stringSimilarity(target, source, matched):
    for i in range(len(source)):
        if source[i] in matched:
            continue
        
        for j in range(len(target)):
            if source[i] == target:
                matched.append(source[i])
                if debug:
                    print(f"matched {target} to {source[i]}")
                return True

            # No match found
            return False

# Checking presence
def presentie(aanwezig):
    matched = []
    afwezig = []
    integer = 0
    # Open file with all members
    f = open("files/2dekmrledn2.txt", 'r')
    print("----Afwezig:----")

    # Check who are present at vergaderingen and mark in 'matched' array
    for line in f:
        if stringSimilarity(line.rstrip('\n'), aanwezig, matched):
            integer += 1
        else:
            print(line.rstrip('\n'))
            afwezig.append(line.rstrip('\n'))
            pass
        
        print(integer, "/", len(aanwezig), len(afwezig), "afwezigen")
        # Check if everyone has been matched
        if integer is not len(aanwezig):
            print(f"Aantal Kamerleden matcht niet met het aanwezige aantal is {integer} maar moet zijn {len(aanwezig)}")
        print(afwezig)
        print(aanwezig)
        return aanwezig, afwezig
                                            

# Tel hoevaak mensen afwezig zijn en geef lijst terug met aantal afwezigheden p.p.
def arrayParsing(aanwezig, afwezig):
    afwezig = np.array(afwezig, dtype=object)
    count = np.arange(1, 2*len(afwezig), 0.5, dtype=int)
    afwezig = afwezig.reshape(-1)
    df = pd.DataFrame(data=afwezig, columns=["afwezig"])
    df['counts'] = pd.DataFrame(data=count)
    return df