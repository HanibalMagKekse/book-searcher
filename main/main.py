import pandas as pd
from tkinter import *


from api import dnb_sru, parse_record_dc
from csvTools import format_data_for_csv, ToCsv

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

    records = dnb_sru(queryString)
        
    output = [parse_record_dc(record) for record in records]


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
                label = Label(master=frame_results,text=info + ": " + string)
                label.grid(row=reihe,column=spalte,padx=5,pady=1)
                myLabels.append(label)
                reihe += 1

            button = Button(master=frame_results, text="Confirm", command=lambda spalte=spalte: ToCsv(df.loc[spalte], contributor_list[spalte]))
            button.grid(row=reihe,column=spalte,padx=20,pady=5)
            buttons.append(button)
            spalte = spalte + 1
        
    print(len(records), 'Ergebnisse')

root = Tk()
root.geometry("1000x500")
root.title("Booksearcher")


frame_inputs = Frame(master=root)
frame_inputs.pack(anchor = NW)

frame_results = Frame(master=root)
frame_results.pack(side = LEFT)


label_tit_ean = Label(master=frame_inputs,text="EAN / Titel")
label_tit_ean.grid(row=0,column=0, padx=10)
tit_ean = Entry(master=frame_inputs)
tit_ean.grid(row=1,column=0, padx=10)

label_autor = Label(master=frame_inputs,text="Autor")
label_autor.grid(row=0,column=1, padx=10)
autor = Entry(master=frame_inputs)
autor.grid(row=1,column=1, padx=10)

label_verlag = Label(master=frame_inputs,text="Verlag")
label_verlag.grid(row=0,column=2, padx=10)
verlag = Entry(master=frame_inputs)
verlag.grid(row=1,column=2, padx=10)

label_erscheinungsjahr = Label(master=frame_inputs,text="Erscheinungsjahr")
label_erscheinungsjahr.grid(row=0,column=3, padx=10)
erscheinungsjahr = Entry(master=frame_inputs)
erscheinungsjahr.grid(row=1,column=3, padx=10)

label_sprachencode = Label(master=frame_inputs,text="Sprachencode")
label_sprachencode.grid(row=0,column=4, padx=10)
sprachencode = Entry(master=frame_inputs)
sprachencode.grid(row=1,column=4, padx=10)

label_format = Label(master=frame_inputs,text="Materialart")
label_format.grid(row=0,column=5, padx=10)
formate = Entry(master=frame_inputs)
formate.grid(row=1,column=5, padx=10)

myLabels = []
buttons = []

# binds the return key to InputEntered
root.bind('<Return>', InputEntered)
myButtons = Button(master=frame_inputs, text="Enter")

# binds the button press to InputEntered
myButtons.bind('<Button-1>', InputEntered)
myButtons.grid(row=2,column=2, pady=20, sticky="ew", columnspan=2)



root.mainloop()