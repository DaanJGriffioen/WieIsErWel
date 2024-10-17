import argparse
import string
import pandas as pd
import numpy as np
import array
from cgi import print_form
import sys
from types import NoneType
from numpy import dtype
import requests as req
import xml.etree.ElementTree as ET
import json
from datetime import date, datetime, timedelta

import argparse

debug = False
git = False

def kamerleden():
  namen = ["Jong", "Bosma", "Dijck", "Dijk", "Groot", "Jansen", "Vries", "Mulder"]
  url = "https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/Persoon?$filter=Verwijderd%20eq%20false%20and%20FractieZetelPersoon/any(a:a/TotEnMet%20eq%20null)"
  r = req.get(url)
  content = json.loads(r.content)
  f = open("files/2dekmrledn2.txt", "w")
  for item in content["value"]:
    naam = ""
    if item["Achternaam"] in namen:
      if item["Roepnaam"] != "Jimmy":
        naam += item["Roepnaam"].lower().replace(" ","")
    if item["Tussenvoegsel"] != None:
      naam += item["Tussenvoegsel"].replace(" ","")
    naam += item["Achternaam"].lower().replace(" ","")
    f.write(naam+"\n")
  f.close()


# Get most recent 'vergaderverslag' from tweedekamer API
def getURLContent(datum):
  # Write to log file
  f = open(f"files/logs/log{str(datum)}.txt", "w")
  f.close() 
  year = datum.year
  month = datum.month
  day = datum.day
  url = f"https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/Verslag?$filter=year(GewijzigdOp)%20eq%20{year}%20and%20month(GewijzigdOp)%20eq%20{month}%20and%20day(GewijzigdOp)%20eq%20{day}"
  if debug:
    print(url)
  r = req.get(url)
  return r.content

# Get vergaderID from json
def vergaderID(content):
  val = json.loads(content)
  vergaderingen = []
  for line in val["value"]:
    if line["Verwijderd"] == False:
      if debug:
        print(line)
      vergaderingen.append(line["Id"])
  return vergaderingen
  
# Get 'Vergaderverslagen'
def getVerslag(vergID):
  r = []
  for i in range(len(vergID)):
    url = f"https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/Verslag/{vergID[i]}/resource"
    if debug:
      print(url)
    r.append(req.get(url))
  return r

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

    if root[0][1].text != "Plenaire zaal" or root.attrib['soort'] == "Voorpublicatie":
      tijden.append(0)
      continue
    
    tijden.append(root.attrib["Timestamp"].split('T')[1].split(':')[0])

  for j in range(len(tijden)):
    if int(tijden[j]) > max:
      max = int(tijden[j])
      max_element = j

  if debug:
    print(max_element, max)
  return max_element


# Parse the XML received from the API
def parseXML(verslagen):
  next = False
  kamerleden = ""

  laatste_vers = laatste(verslagen)
  
  if  laatste_vers == -1:
    return -1
  
  verslag = verslagen[laatste_vers].content.decode()
  
  try:
    root = ET.fromstring(verslag)
  except:
    raise Exception("Error parsing XML")

  # Parse XML and extract specific element
  ns = {'ns': 'http://www.tweedekamer.nl/ggm/vergaderverslag/v1.0'}
  alinea_elements  = root.findall(".//ns:alineaitem", namespaces=ns)
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

# Match names from present list (source) to total list (target)
def stringSimilarity(target, source, matched):
  consistent = 0
  for i in range(len(source)):
    if source[i] in matched:
      continue
    consistent = 0
    for j in range(len(target)):

      ### Not needed, quite shit ###
      # If the length of one of the strings has been reached or if enough letters are matched
      # if j >= len(source[i]) or j >= len(target) or consistent >= len(source[i]) - 1:
      #   # If enough letters are matched accept it
      #   if consistent >= len(source[i]) - 1:
      ### ++ ###

      if source[i] == target:
        matched.append(source[i])
        if debug:
          print(f"matched {target} to {source[i]}")
        return True

      ### Not needed, quite shit ###
      # Compare letters
      # if target[j] == source[i][j]:
      #   consistent += 1
      ### ++ ###

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
    

def arrayParsing(aanwezig, afwezig):
  afwezig = np.array(afwezig, dtype=object)
  count = np.arange(1, 2*len(afwezig), 0.5, dtype=int)
  afwezig = afwezig.reshape(-1)
  df = pd.DataFrame(data=afwezig, columns=["afwezig"])
  df['counts'] = pd.DataFrame(data=count)
  # Tel hoevaak mensen afwezig zijn en geef lijst terug met aantal afwezigheden p.p.
  return df

# Make nice graph who is present and who is not
def makeHTML(aanwezig, afwezig, datums):
  data = arrayParsing(aanwezig, afwezig)
  
  data = data["afwezig"].value_counts()
  f = open("index.html", "w")
  f.write("<!DOCTYPE html>\n<html>\n<head>\n<link rel=\"stylesheet\" href=\"style.css\">\n</head>\n<body>")
  f.write("<h1>\nKamerleden Afnwezigheid</h1>\n")
  f.write(f"<h2>Afwezigheid van {datums[0]} tot {datums[1]}</h2>")
  f.write("<table>\n")
  f.write("<th>Naam</th><th>Aantal</th>")
  for entry in data.items():
    f.write("<tr>")
    f.write( "<td>" + entry[0] + "</td><td>" + str(entry[1]) + "</td>")
    f.write("</tr>" + '\n')
  f.write("</table>\n")
  f.write("</body>")



def aanwezigheid(datum):
  # Check of er wel een echte datum doorgegeven is
  assert type(datum) == date
  # Haal het verslag op
  content = getURLContent(datum)
  # Haal de vergaderID uit het verslag
  vergID = vergaderID(content)
  # Als de ID nul is, is er geen vergaderverslag
  if len(vergID) == 0:
    return None, None

  if debug:
    print(vergID[0])
  # Haal het verslag op a.h.v. de vergaderID
  verslagen = getVerslag(vergID)
  # Haal de lijst met kamerleden uit de verslagen
  kamerleden = parseXML(verslagen)
  # Check of er wel echt iets uitgekomen is
  if kamerleden == -1:
    return None, None
  # Geef de aanwezigen terug aan de bovenliggende functie 
  aanwezig, afwezig = presentie(kamerleden)
  f = open(f"files/logs/log_{datum}.txt", "a")
  f.write("Aanwezig:\n")
  for stri in aanwezig:
    f.write(stri + '\n')
  f.write("\nAfwezig:\n")
  for stri in afwezig:
    f.write(stri + '\n')
  f.close()

  return aanwezig, afwezig
  

def main():
  bereik = False
  data = []
  aanwezig = ""
  aanwezig_arr = []
  afwezig_arr = []
  #  Een specifieke datum
  if git:
    datum = date.today() - timedelta(days=1)
    stri = str(datum)
    aanwezig, afwezig = aanwezigheid(datum)
    data.extend([stri, stri])
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
      print("Kan niet in de toekomst kijken, misschien een volgende update ;)")
      exit(0)
    aanwezig, afwezig = aanwezigheid(datum)
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