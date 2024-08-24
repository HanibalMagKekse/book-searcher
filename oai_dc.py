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
    params = {'recordSchema' : 'oai_dc',
          'operation': 'searchRetrieve',
          'version': '1.1',
          'maximumRecords': '100',
          'query': query
         }
    r = requests.get(base_url, params=params)
    xml = soup(r.content, features="xml")
    records = xml.find_all('record')
    
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



def parse_record_dc(record):
    
    ns = {"dc": "http://purl.org/dc/elements/1.1/", 
          "xsi": "http://www.w3.org/2001/XMLSchema-instance"}
    xml = etree.fromstring(unicodedata.normalize("NFC", str(record)))
    
    #idn
    idn = xml.xpath(".//dc:identifier[@xsi:type='dnb:IDN']", namespaces=ns) #--> Adressiert das Element direkt   
    try:
        idn = idn[0].text
    except:
        idn = 'fail'
    
    #creator:
    creator = xml.xpath('.//dc:creator', namespaces=ns)
    try:
        creator = creator[0].text
    except:
        creator = "N/A"
    
    #titel
    titel = xml.xpath('.//dc:title', namespaces=ns)
    try:
        titel = titel[0].text
    except:
        titel = "N/A"
        
    #date
    date = xml.xpath('.//dc:date', namespaces=ns)
    try:
        date = date[0].text
    except:
        date = "N/A"
    
    
    #publisher
    publ = xml.xpath('.//dc:publisher', namespaces=ns)
    try:
        publ = publ[0].text
    except:
        publ = "N/A"
    
    #type
    type = xml.xpath('.//dc:type', namespaces=ns)
    try:
        type = type[0].text
    except:
        type = "N/A"
        
    #identifier
    ids = xml.xpath('.//dc:identifier[@xsi:type="tel:ISBN"]', namespaces=ns)
    try:
        ids = ids[0].text
    except:
        ids = "N/A"
        
    #urn
    urn = xml.xpath('.//dc:identifier[@xsi:type="tel:URN"]', namespaces=ns)
    try:
        urn = urn[0].text
    except:
        urn = "N/A"
        
        
    meta_dict = {"IDN":idn, "CREATOR":creator, "TITLE":titel, "DATE":date, "PUBLISHER":publ, "URN":urn, "ISBN":ids, "TYPE":type}
    
    return meta_dict

#records = dnb_sru('tit=Faust I and location=onlinefree')
if type_input == "isbn":
    records = dnb_sru(f'isbn={input}')
elif type_input == "titel":
    records = dnb_sru(f'tit={input}')
print(len(records), 'Ergebnisse')

output = [parse_record_dc(record) for record in records]
df = pd.DataFrame(output)
#print(df)

df.to_csv("SRU_Titel.csv", index=False)