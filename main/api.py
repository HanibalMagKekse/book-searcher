import requests
from bs4 import BeautifulSoup as soup
import unicodedata
from lxml import etree

def dnb_sru(query):
    
    base_url = "https://services.dnb.de/sru/dnb"
    params = {'recordSchema' : 'oai_dc',
          'operation': 'searchRetrieve',
          'version': '1.1',
          'maximumRecords': '5',
          'query': query
         }
    r = requests.get(base_url, params=params)
    xml = soup(r.content, features="xml")
    records = xml.find_all('record')
    
    if len(records) < 5:
        
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
    
    #creator:
    creator = xml.xpath('.//dc:creator', namespaces=ns)

    #contributors:
    contributors = []
    for i in range(0,50):
        try:
            contributors.append(creator[i].text)
        except:
            pass

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
    book_type = xml.xpath('.//dc:type', namespaces=ns)
    try:
        book_type = type[0].text
    except:
        book_type = "N/A"
        
    #identifier
    isbn = xml.xpath('.//dc:identifier[@xsi:type="tel:ISBN"]', namespaces=ns)
    try:
        isbn = isbn[0].text
    except:
        isbn = "N/A"
        
    
    meta_dict = {"Autor/ Herausgeber":creator, "Titel":titel, "Jahr":date, "Verlag":publ, "ISBN":isbn, "TYPE":book_type, "CONTRIBUTOR":contributors}
    
    return meta_dict