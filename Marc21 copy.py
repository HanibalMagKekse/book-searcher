import requests
from bs4 import BeautifulSoup as soup
import unicodedata
from lxml import etree
import pandas as pd
print("Waiting...")
input = input("Enter: ")
try:
    int(input[0])
    type_input = "isbn"
except:
    type_input = "titel"
print(input)
print(type_input)
print("Top")
def dnb_sru(query):
    
    base_url = "https://services.dnb.de/sru/dnb"
    params = {'recordSchema' : 'MARC21-xml',
          'operation': 'searchRetrieve',
          'version': '1.1',
          'maximumRecords': '100',
          'query': query
         }
    r = requests.get(base_url, params=params)
    xml = soup(r.content, features="xml")
    records = xml.find_all('record', {'type':'Bibliographic'})
    
    if len(records) < 100:
        
        return records
    
    else:
        
        num_results = 100
        i = 101
        while num_results == 100:
            
            params.update({'startRecord': i})
            r = requests.get(base_url, params=params)
            xml = soup(r.content, features="xml")
            new_records = xml.find_all('record', {'type':'Bibliographic'})
            records+=new_records
            i+=100
            num_results = len(new_records)
            
        return records



def parse_record(record):
    
    ns = {"marc":"http://www.loc.gov/MARC21/slim"}
    xml = etree.fromstring(unicodedata.normalize("NFC", str(record)))
    print(xml)
    #idn
    idn = xml.xpath("marc:controlfield[@tag = '001']", namespaces=ns)
    print(idn)
    try:
        idn = idn[0].text
    except:
        idn = 'fail'
    
    # titel
    titel = xml.xpath("marc:datafield[@tag = '245']/marc:subfield[@code = 'a']", namespaces=ns)
    
    try:
        titel = titel[0].text
        #titel = unicodedata.normalize("NFC", titel)
    except:
        titel = "unkown"
        
    meta_dict = {"idn":idn,
                 "titel":titel}
    
    return meta_dict
#Function für Titeldaten in MARC21
def parse_record_marc(item):

    ns = {"marc":"http://www.loc.gov/MARC21/slim"}
    xml = etree.fromstring(unicodedata.normalize("NFC", str(item)))
    
    
    #idn
    idn = xml.findall("marc:controlfield[@tag = '001']", namespaces=ns)
    try:
        idn = idn[0].text
    except:
        idn = 'N/A' 
        
    
    #creator
    creator1 = xml.findall("marc:datafield[@tag = '100']/marc:subfield[@code = 'a']", namespaces=ns)
    creator2 = xml.findall("marc:datafield[@tag = '110']/marc:subfield[@code = 'a']", namespaces=ns)
    subfield = xml.findall("marc:datafield[@tag = '110']/marc:subfield[@code = 'e']", namespaces=ns)
    
    if creator1:
        creator = creator1[0].text
    elif creator2:
        creator = creator2[0].text
        if subfield:
            creator = creator + " [" + subfield[0].text + "]"
    else:
        creator = "N/A"
    
    #Titel $a
    title = xml.findall("marc:datafield[@tag = '245']/marc:subfield[@code = 'a']", namespaces=ns)
    title2 = xml.findall("marc:datafield[@tag = '245']/marc:subfield[@code = 'b']", namespaces=ns)
    
    if title and not title2:
        titletext = title[0].text
    elif title and title2:     
        titletext = title[0].text + ": " + title2[0].text
    else:
        titletext = "N/A"
    
    
    #date
    date = xml.findall("marc:datafield[@tag = '264']/marc:subfield[@code = 'c']", namespaces=ns)
    try:
        date = date[0].text
    except:    
        date = 'N/A'
    
    
    #publisher
    publ = xml.findall("marc:datafield[@tag = '264']/marc:subfield[@code = 'b']", namespaces=ns)
    try:
        publ = publ[0].text
    except:    
        publ = 'N/A'
        
        
    #URN
    testurn = xml.findall("marc:datafield[@tag = '856']/marc:subfield[@code = 'x']", namespaces=ns)
    urn = xml.findall("marc:datafield[@tag = '856']/marc:subfield[@code = 'u']", namespaces=ns)
    
    if testurn:
        urn = urn[0].text
    else:    
        urn = 'N/A'
        
        
    #ISBN
    isbn_new = xml.findall("marc:datafield[@tag = '020']/marc:subfield[@code = 'a']", namespaces=ns)
    isbn_old = xml.findall("marc:datafield[@tag = '024']/marc:subfield[@code = 'a']", namespaces=ns)
    if isbn_new:
        isbn = isbn_new[0].text
    elif isbn_old: 
        isbn = isbn_old[0].text
    else:    
        isbn = 'N/A'
    

    
    meta_dict = {"IDN":idn, "CREATOR":creator, "TITLE": titletext, "DATE":date, 
                 "PUBLISHER":publ, "URN":urn, "ISBN":isbn}
    
    return meta_dict
    
#records = dnb_sru('tit=Faust I and location=onlinefree')
if type_input == "isbn":
    records = dnb_sru(f'isbn={input}')
elif type_input == "titel":
    records = dnb_sru(f'tit={input}')
print(len(records), 'Ergebnisse')

output = [parse_record_marc(record) for record in records]
df = pd.DataFrame(output)
#print(df)

df.to_csv("SRU_Titel.csv", index=False)