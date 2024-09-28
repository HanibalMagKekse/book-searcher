# book-searcher
Ein Programm welches das aufnehmen von Büchern in eine Datenbank erleichtert.

Quellen:

DNB Katalog:

https://portal.dnb.de/opac/simpleSearch?query=

Tutorial zur Abfrage:

https://www.youtube.com/watch?v=bAenBAfu1po&list=PLiOn8zIQG_S0k5Auvn28Q_Emqtz7ewx40&index=6
https://www.dnb.de/DE/Professionell/Services/WissenschaftundForschung/DNBLab/dnblabTutorials.html?nn=849628

Kürzel für die Abfrage:
https://services.dnb.de/sru/dnb?operation=explain&version=1.1

mögliche Abfrage Daten:

https://www.dnb.de/DE/Professionell/Metadatendienste/Exportformate/DNB-Casual/dnbCasual_node.html#doc186950bodyText1

ToDo (sortiert nach Relevanz):

- richtiges csv format
- relevante informationen anzeigen
- Markierung von unterschieden
- verlauf


Wie nutzt man den book_searcher?

man braucht eine python Umgebung:
z.B.: Visual Studio Code:   https://code.visualstudio.com/

Außerdem ein paar python Bibliotheken.
Diese installiert man in dem den passenden Befehl in Powershell eingibt:
requests:          pip install requests \n
BeautifulSoup:     pip install beautifulsoup4
unicodedata:       pip install unicodedata2
lxml:              pip install lxml
pandas:            pip install pandas
customtkinter:     pip install customtkinter

