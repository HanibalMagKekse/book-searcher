import pandas as pd
import csv


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