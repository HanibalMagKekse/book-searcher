import requests
from bs4 import BeautifulSoup as soup
import unicodedata
from lxml import etree
import pandas as pd
from customTkinter import *
#import csv

infos = list = ["IDN","CREATOR","TITLE","DATE","PUBLISHER","URN","ISBN","TYPE","CONTRIBUTOR"]

def InputEntered():

    # Entfernt bei neuer Eingabe alte Buttons und Labels
    for book in myLabels:
        book.destroy()
    for button in buttons:
        button.destroy()
        
    input_isbn = isbn.get()
    input_autor = autor.get()
    input_verlag = verlag.get()
    input_erscheinungsjahr = erscheinungsjahr.get()
    input_sprachencode = sprachencode.get()
    input_format = formate.get()


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

    
    # build query string and search
    if type_input == "isbn":
        tisbn = "isbn"
    elif type_input == "titel":
        tisbn = "tit"

    quInputs = [input_isbn, input_autor, input_verlag, input_erscheinungsjahr, input_sprachencode, input_format] 
    quLabels = [tisbn, "atr", "vlg", "jhr", "spr", "mat"]
    queryString = f""

    for label, value in enumerate(quInputs):
        if len(value) != 0:
            if queryString == "":
                queryString += f"{quLabels[label]}={value}"
            else:
                queryString += f" and {quLabels[label]}={value}"

    print(queryString)
    records = dnb_sru(queryString)
        
    output = [parse_record_dc(record) for record in records]

    
    df = pd.DataFrame(output)
    
    
    spalte = 0
    reihe = 3
    instantCsv = False
    if len(records) == 0:
        print("Keine Ergebnisse")
    elif len(records) == 1 and instantCsv:
       df.to_csv("SRU_Titel.csv", mode = "a", index = False,header=False)
    else:

        for record in output:
            reihe = 3
            for info in record:
                
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
                label = CTkLabel(root,text=info + ": " + string)
                label.grid(row=reihe,column=spalte,padx=5,pady=1)
                myLabels.append(label)
                reihe += 1
            button = Button(root, text="Confirm", command=lambda spalte=spalte: ToCsv(df.loc[spalte]))
            button.grid(row=reihe,column=spalte,padx=20,pady=5)
            buttons.append(button)
            spalte = spalte + 1
        
    print(len(records), 'Ergebnisse')

root = CTk()
root.geometry("1000x500")

label_isbn = CTkLabel(root,text="ISBN / Titel")
label_isbn.grid(row=0,column=0)
isbn = CTkEntry(root)
isbn.grid(row=1,column=0)

label_autor = CTkLabel(root,text="Autor")
label_autor.grid(row=0,column=1)
autor = CTkEntry(root)
autor.grid(row=1,column=1)

label_verlag = CTkLabel(root,text="Verlag")
label_verlag.grid(row=0,column=2)
verlag = CTkEntry(root)
verlag.grid(row=1,column=2)

label_erscheinungsjahr = CTkLabel(root,text="Erscheinungsjahr")
label_erscheinungsjahr.grid(row=0,column=3)
erscheinungsjahr = CTkEntry(root)
erscheinungsjahr.grid(row=1,column=3)

label_sprachencode = CTkLabel(root,text="Sprachencode")
label_sprachencode.grid(row=0,column=4)
sprachencode = CTkEntry(root)
sprachencode.grid(row=1,column=4)

label_format = CTkLabel(root,text="Materialart")
label_format.grid(row=0,column=5)
formate = CTkEntry(root)
formate.grid(row=1,column=5)

myLabels = []
buttons = []

myButtons = CTkButton(root, text="Enter", command=InputEntered)
myButtons.grid(row=2,column=2)

def ToCsv(df):
    #                                                                                            Größe
    new_meta_dict = {"Bestellnr":"","Autor/ Herausgeber":"","Titel":"","Verlag":"","Einband":"","Format":"","Gewicht in g":"","Auflage":"","Jahr":"","Empty1":"","Ort":"","Zustand (1-4)":"","Sprachennr.":"","Sprache":"","ISBN":"","EAN":"","Seitenzahl/Umfang":"","Ihr Preis in �":"","zvab-Preis":"","Zustand-zvab":"","Illustrator":"","�bersetzer":"","Vor- oder Nachwort":"","Nachwort":"","weitere Mitwirkende":"","Untertitel":"","Originaltitel":"","aus der Reihe":"","Band":"","Schlagworte":"","Beschreibung":"","Zustandsbeschreibung":"","Lieferungsnr":"","Lieferant":"","Einkaufspreis in �":"","Aufgenommen am:":"","Menge":"","3860400644":"","Zustand-amazon":"","Standort":"","Kommission":"","Sparten-Nr.":"","Spartenbezeichnung":"","Einkaufsdatum":"","MwSt.":"","ebay":"","Notizen":"","Bild":"","alte Bestellnummer":"","ASIN":"","versandkennziffer":"","H�he":"","Breite":"","Tiefe":"","Suche":"","ebay-ID":"","Titel-Autor-anzahl":""}
   
    df = df.to_dict()
    for info in new_meta_dict:
        for thing in df:
            try:
                if info == thing:
                    new_meta_dict[info] = df[thing]
                    
                    print("Vergleich klappt")
            except:
                pass
    
    dataframe = pd.DataFrame([new_meta_dict])
   

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
        
    
    meta_dict = {"Autor/ Herausgeber":creator, "Titel":titel, "Jahr":date, "Verlag":publ, "ISBN":ids, "TYPE":type, "CONTRIBUTOR":contributors}
    
    return meta_dict



root.mainloop()