import requests
from bs4 import BeautifulSoup as soup
import unicodedata
from lxml import etree
import pandas as pd
from customtkinter import *
import csv

infos = list = ["IDN","CREATOR","TITLE","DATE","PUBLISHER","URN","ISBN","TYPE","CONTRIBUTOR"]

def InputEntered(event = None):

    # Entfernt bei neuer Eingabe alte Buttons und Labels
    for book in myLabels:
        book.destroy()
    for button in buttons:
        button.destroy()
        
    input_tit_ean = tit_ean.get()
    input_autor = autor.get()
    input_verlag = verlag.get()
    input_erscheinungsjahr = erscheinungsjahr.get()
    input_sprachencode = sprachencode.get()
    input_format = formate.get()


    try:
        int(input_tit_ean[0:8])
        type_input = "ean"
        print("EAN: " + input_tit_ean)
    except:
        type_input = "titel"
        print("Titel: " + input_tit_ean)

    # build query string and search
    if type_input == "ean":
        records = dnb_sru(f'num={input_tit_ean}')
        tisbn = "num"
    elif type_input == "titel":
        records = dnb_sru(f'tit={input_tit_ean}')
        tisbn = "tit"

    quInputs = [input_tit_ean, input_autor, input_verlag, input_erscheinungsjahr, input_sprachencode, input_format] 
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
    print(output)


    output, contributor_list = format_data_for_csv(output)
    df = pd.DataFrame(output)
    
    
    spalte = 0
    reihe = 0
    instantCsv = False
    if len(records) == 0:
        print("Keine Ergebnisse")
    elif len(records) == 1 and instantCsv:
       df.to_csv("SRU_Titel.csv", mode = "a", index = False,header=False)
    else:

        for record in output:
            reihe = 0
            for info in record:
                
                string = record[info]
                if info == "CONTRIBUTOR":
                    
                    if len(string) == 0:
                        string = "N/A"
                    else:
                        string = "".join(string)
                if len(string) > 40:
                    row_counter = 1
                    for char in range(1, len(string)):
                        if char % 40 == 0:
                            string = string[:40*row_counter] + "\n" + string[40*row_counter:]
                            row_counter += 1
                label = CTkLabel(master=frame_results,text=info + ": " + string)
                label.grid(row=reihe,column=spalte,padx=5,pady=1)
                myLabels.append(label)
                reihe += 1

            button = CTkButton(master=frame_results, text="Confirm", command=lambda spalte=spalte: ToCsv(df.loc[spalte], contributor_list[spalte]))
            button.grid(row=reihe,column=spalte,padx=20,pady=5)
            buttons.append(button)
            spalte = spalte + 1
        
    print(len(records), 'Ergebnisse')

root = CTk()
root.geometry("1000x500")
root.title("Booksearcher")


frame_inputs = CTkFrame(master=root)
frame_inputs.pack(anchor = NW)

frame_results = CTkFrame(master=root)
frame_results.pack(side = LEFT)


label_tit_ean = CTkLabel(master=frame_inputs,text="EAN / Titel")
label_tit_ean.grid(row=0,column=0, padx=10)
tit_ean = CTkEntry(master=frame_inputs)
tit_ean.grid(row=1,column=0, padx=10)

label_autor = CTkLabel(master=frame_inputs,text="Autor")
label_autor.grid(row=0,column=1, padx=10)
autor = CTkEntry(master=frame_inputs)
autor.grid(row=1,column=1, padx=10)

label_verlag = CTkLabel(master=frame_inputs,text="Verlag")
label_verlag.grid(row=0,column=2, padx=10)
verlag = CTkEntry(master=frame_inputs)
verlag.grid(row=1,column=2, padx=10)

label_erscheinungsjahr = CTkLabel(master=frame_inputs,text="Erscheinungsjahr")
label_erscheinungsjahr.grid(row=0,column=3, padx=10)
erscheinungsjahr = CTkEntry(master=frame_inputs)
erscheinungsjahr.grid(row=1,column=3, padx=10)

label_sprachencode = CTkLabel(master=frame_inputs,text="Sprachencode")
label_sprachencode.grid(row=0,column=4, padx=10)
sprachencode = CTkEntry(master=frame_inputs)
sprachencode.grid(row=1,column=4, padx=10)

label_format = CTkLabel(master=frame_inputs,text="Materialart")
label_format.grid(row=0,column=5, padx=10)
formate = CTkEntry(master=frame_inputs)
formate.grid(row=1,column=5, padx=10)

myLabels = []
buttons = []

# binds the return key to InputEntered
root.bind('<Return>', InputEntered)
myButtons = CTkButton(master=frame_inputs, text="Enter")

# binds the button press to InputEntered
myButtons.bind('<Button-1>', InputEntered)
myButtons.grid(row=2,column=2, pady=20, sticky="ew", columnspan=2)

def format_data_for_csv(data):
    # should filter different groups out of contributors
    object_counter = 0
    contributor_list = []
    contributors = {"verfasser": [], "herausgeber": [], "künstler": [], "illustrator": [], "übersetzer": [], "mitwirkende": [], "vorwort": [], "nachwort": [], "adressat": [], "komponist": []}

    for object in data:
        contributors = {"verfasser": [], "herausgeber": [], "künstler": [], "illustrator": [], "übersetzer": [], "mitwirkende": [], "vorwort": [], "nachwort": [], "adressat": [], "komponist": []}
        for person in object["CONTRIBUTOR"]:
            if "[Verfasser]" in person:
                new_string = person.replace("[Verfasser]", "")
                contributors["verfasser"].append(new_string)
            elif "[Herausgeber]" in person:
                new_string = person.replace("[Herausgeber]", "")
                contributors["herausgeber"].append(new_string)
            elif "[Künstler]" in person:
                new_string = person.replace("[Künstler]", "")
                contributors["künstler"].append(new_string)
            elif "[Übersetzer]" in person:
                new_string = person.replace("[Übersetzer]", "")
                contributors["übersetzer"].append(new_string)
            elif "[Adressat]" in person:
                new_string = person.replace("[Adressat]", "")
                contributors["adressat"].append(new_string)
            elif "[Komponist]" in person:
                new_string = person.replace("[Komponist]", "")
                contributors["komponist"].append(new_string)
            elif "[Mitwirkender]" in person:
                new_string = person.replace("[Mitwirkender]", "")
                contributors["mitwirkende"].append(new_string)
            elif "[Illustrator]" in person:
                new_string = person.replace("[Illustrator]", "")
                contributors["illustrator"].append(new_string)
            elif "(Vorwort)" in person:
                new_string = person.replace("(Vorwort)", "")
                contributors["vorwort"].append(new_string)
            elif "(Nachwort)" in person:
                new_string = person.replace("(Nachwort)", "")
                contributors["nachwort"].append(new_string)

        new_contributors = contributors.copy()
        for person_type in contributors:
            print(person_type)
            if len(contributors[person_type]) == 0:
                del new_contributors[person_type]
        data[object_counter]['CONTRIBUTOR'] = str(new_contributors)
        contributor_list.append(new_contributors)
        object_counter += 1
    
    
    #data = contributors
    return data, contributor_list

def ToCsv(df, contributors):
     
    # Open the CSV file 
    with open('export.csv', 'r') as file: 
        # Create a CSV reader 
        reader = csv.reader(file) 
         
        # Initialize a variable to store the last row 
        last_row = None 
         
        # Iterate through the rows 
        for last_row in reader: 
            pass  # This will keep updating last_row until the last one 

    bestellnr_alt = last_row[0]
    print(f"bestellnr: {bestellnr_alt}")
    try:
        if int(bestellnr_alt) < 40000:
            bestellnr = int(bestellnr_alt) +1
        else:
            bestellnr = ""
            print("bestellnr zu groß")
    except:
        bestellnr = ""
        print("bestellnr not found")

    for c_type in contributors:
        new_string = ""
        for person in contributors[c_type]:
            new_string += str(person)
            new_string += "+ "
        new_string = new_string[:len(new_string)-2]
        contributors[c_type] = new_string

    try:
        illustrator = contributors["illustrator"]
    except:
        illustrator = ""
    try:
        übersetzer = str(contributors["übersetzer"])
    except:
        übersetzer = ""
    try:
        vorwort = str(contributors["vorwort"])
    except:
        vorwort = ""
    try:
        nachwort = str(contributors["nachwort"])
    except:
        nachwort = ""
    try:
        mitwirkende = str(contributors["mitwirkende"])
    except:
        mitwirkende = ""
    #                                                                                                   Größe
    new_meta_dict = {"Bestellnr":bestellnr,"Autor/ Herausgeber":"","Titel":"","Verlag":"","Einband":"","Format":"","Gewicht in g":"","Auflage":"","Jahr":"","Empty1":"","Ort":"","Zustand (1-4)":"","Sprachennr.":"","Sprache":"","ISBN":"","EAN":"","Seitenzahl/Umfang":"","Ihr Preis in �":"","zvab-Preis":"","Zustand-zvab":"","Illustrator":illustrator,"�bersetzer":übersetzer,"Vor- oder Nachwort":vorwort,"Nachwort":nachwort,"weitere Mitwirkende":mitwirkende,"Untertitel":"","Originaltitel":"","aus der Reihe":"","Band":"","Schlagworte":"","Beschreibung":"","Zustandsbeschreibung":"","Lieferungsnr":"","Lieferant":"","Einkaufspreis in �":"","Aufgenommen am:":"","Menge":"","3860400644":"","Zustand-amazon":"","Standort":"","Kommission":"","Sparten-Nr.":"","Spartenbezeichnung":"","Einkaufsdatum":"","MwSt.":"","ebay":"","Notizen":"","Bild":"","alte Bestellnummer":"","ASIN":"","versandkennziffer":"","H�he":"","Breite":"","Tiefe":"","Suche":"","ebay-ID":"","Titel-Autor-anzahl":""}
   
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
    
    dataframe.to_csv("export.csv", mode = "a", index = False,header=False)


    




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
    isbn = xml.xpath('.//dc:identifier[@xsi:type="tel:ISBN"]', namespaces=ns)
    try:
        isbn = isbn[0].text
    except:
        isbn = "N/A"
        
    
    meta_dict = {"Autor/ Herausgeber":creator, "Titel":titel, "Jahr":date, "Verlag":publ, "ISBN":isbn, "TYPE":type, "CONTRIBUTOR":contributors}
    
    return meta_dict



root.mainloop()