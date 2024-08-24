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

#records = dnb_sru('tit=Faust I and location=onlinefree')
if type_input == "isbn":
    records = dnb_sru(f'isbn={input}')
elif type_input == "titel":
    records = dnb_sru(f'tit={input}')
print(len(records), 'Ergebnisse')

output = [parse_record(record) for record in records]
df = pd.DataFrame(output)
#print(df)

df.to_csv("SRU_Titel.csv", index=False)