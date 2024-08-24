import requests
from bs4 import BeautifulSoup as soup
import unicodedata
from lxml import etree
import pandas as pd
from tkinter import *
#import csv

infos = list = ["IDN","CREATOR","TITLE","DATE","PUBLISHER","URN","ISBN","TYPE","CONTRIBUTOR"]

def InputEntered():
    for book in myLabels:
        book.destroy()
    for button in buttons:
        button.destroy()
    input_isbn = isbn.get()
    input_autor = autor.get()
    #myLabel = Label(root,text="hello")
    #myLabel.grid()
    try:
        int(input_isbn[0])
        type_input = "isbn"
        print("ISBN: " + input_isbn)
    except:
        type_input = "titel"
        print("Titel: " + input_isbn)

    if type_input == "isbn":
            records = dnb_sru(f'isbn={input_isbn}')
    elif type_input == "titel":
            records = dnb_sru(f'tit={input_isbn}')

    #records = dnb_sru('tit=Faust I and location=onlinefree')
    if len(input_autor) != 0 and len(input_isbn) != 0:
        if type_input == "isbn":
            records = dnb_sru(f'isbn={input_isbn} and creator={input_autor}')
        elif type_input == "titel":
            records = dnb_sru(f'tit={input_isbn} and creator={input_autor}')
    elif len(input_isbn) != 0:
        if type_input == "isbn":
            records = dnb_sru(f'isbn={input_isbn}')
        elif type_input == "titel":
            records = dnb_sru(f'tit={input_isbn}')
    elif len(input_autor) != 0:
        print("Check")
        records = dnb_sru(f'creator={input_autor}')
        
    output = [parse_record_dc(record) for record in records]

    #print(output)
    df = pd.DataFrame(output)
    #for i in df.loc[1]:

     #   print(i)

    #df.loc[spalte].to_frame()
    
    spalte = 0
    reihe = 3
    instantCsv = False
    if len(records) == 0:
        print("Keine Ergebnisse")
    elif len(records) == 1 and instantCsv:
       df.to_csv("SRU_Titel.csv", mode = "a", index = False,header=False)
    else:
        """
        for record in output:
            reihe = 2
            for info in record:
                #print(record[info])
                label = Label(root,bg="red",text=info + ": " + record[info])
                label.grid(row=reihe,column=spalte,padx=5,pady=1)
                myLabels.append(label)
                reihe += 1
            button = Button(root, text="Confirm", command=lambda spalte=spalte: ToCsv(df.loc[spalte]))
            button.grid(row=reihe,column=spalte,padx=20,pady=5)
            buttons.append(button)
            spalte = spalte + 1
        """
        for record in output:
            reihe = 3
            for info in record:
                #print(record[info])
                
                string = record[info]
                if info == "CONTRIBUTOR":
                    
                    if len(string) == 0:
                        string = "N/A"
                    else:
                        string = "".join(string)
                if len(string) > 50:
                    row_counter = 1
                    for char in range(1, len(string)):
                        if char % 50 == 0:
                            string = string[:50*row_counter] + "\n" + string[50*row_counter:]
                            row_counter += 1
                    #string = string[:int(len(string)/2)] + "\n" + string[int(len(string)/2):]
                    #firstpart, secondpart = string[:len(string)/2], string[len(string)/2:]
                label = Label(root,text=info + ": " + string)
                label.grid(row=reihe,column=spalte,padx=5,pady=1)
                myLabels.append(label)
                reihe += 1
            button = Button(root, text="Confirm", command=lambda spalte=spalte: ToCsv(df.loc[spalte]))
            button.grid(row=reihe,column=spalte,padx=20,pady=5)
            buttons.append(button)
            spalte = spalte + 1
        
    print(len(records), 'Ergebnisse')

root = Tk()
root.geometry("500x500")

label_isbn = Label(root,text="ISBN / Titel")
label_isbn.grid(row=0,column=0)

isbn = Entry(root)
isbn.grid(row=1,column=0)

label_autor = Label(root,text="Autor")
label_autor.grid(row=0,column=1)

autor = Entry(root)
autor.grid(row=1,column=1)

myLabels = []
buttons = []

myButtons = Button(root, text="Enter", command=InputEntered)
myButtons.grid(row=2,column=1)

#e.insert(0, "Enter:")
def ToCsv(df):
    
    new_meta_dict = {"Bestellnr":"","Autor/ Herausgeber":"","Titel":"","Verlag":"","Einband":"","Format":"","Gewicht in g":"","Auflage":"","Jahr":"","Empty1":"","Ort":"","Zustand (1-4)":"","Sprachennr.":"","Sprache":"","ISBN":"","EAN":"","Seitenzahl/Umfang":"","Ihr Preis in �":"","zvab-Preis":"","Zustand-zvab":"","Illustrator":"","�bersetzer":"","Vor- oder Nachwort":"","Nachwort":"","weitere Mitwirkende":"","Untertitel":"","Originaltitel":"","aus der Reihe":"","Band":"","Schlagworte":"","Beschreibung":"","Zustandsbeschreibung":"","Lieferungsnr":"","Lieferant":"","Einkaufspreis in �":"","Aufgenommen am:":"","Menge":"","3860400644":"","Zustand-amazon":"","Standort":"","Kommission":"","Sparten-Nr.":"","Spartenbezeichnung":"","Einkaufsdatum":"","MwSt.":"","ebay":"","Notizen":"","Bild":"","alte Bestellnummer":"","ASIN":"","versandkennziffer":"","H�he":"","Breite":"","Tiefe":"","Suche":"","ebay-ID":"","Titel-Autor-anzahl":""}
    meta_dict = {"CREATOR":"", "TITLE":"", "DATE":"", "PUBLISHER":"", "ISBN":"", "TYPE":""}#,"CONTRIBUTOR":"CONTRIBUTOR"}
   
    df = df.to_dict()
    for info in meta_dict:
        print(info)
        for thing in df:
            try:
                if meta_dict[info] == meta_dict[thing]:
                    meta_dict[info] = df[thing]
                    print("Vergleich klappt")
            except:
                pass
    
    dataframe = pd.DataFrame([meta_dict])
   

    print("Added to csv")
    
    dataframe.to_csv("test.csv", mode = "a", index = False,header=False)


    




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
        
        
    meta_dict = {"CREATOR":creator, "TITLE":titel, "DATE":date, "PUBLISHER":publ, "ISBN":ids, "TYPE":type, "CONTRIBUTOR":contributors}
    
    return meta_dict



root.mainloop()