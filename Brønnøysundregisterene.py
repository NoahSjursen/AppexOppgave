from tkinter import *
import tkinter.ttk as ttk
import csv
from difflib import SequenceMatcher
import webbrowser
from tkinter import filedialog as fd

root = Tk()
root.title("Brønnøysundregisteret")
root.configure(bg="lightgrey")

def similar(a, b): #Søkemotoren sjekker hvor like (a,b) er og returnerer en float verdi mellom 0,1
    return SequenceMatcher(None, a, b).ratio()  



def search(): # Funksjonen til søkeknappen
    for i in tree.get_children(): #for loop som sletter data fra tidligere søk i treeviewen
        tree.delete(i)

    content = searchContent.get() # henter informasjon fra "searchContent" StringVar | teksten som du skriver inn for å søke 

    with open(filename, "r") as f:  # åpner "filename" (path til filen du har valgt)
        csv_reader = csv.DictReader(f, delimiter=',') # dictionary med all dataen fra .csv filen
                    
        for line in csv_reader: # leser alle linjene i .csv filen
            result = similar(line["Næringskode 1.beskrivelse"], content) # kjører funksjonen "similar(a,b)" a = Næringskoden på gitt rad, b = det du søkte på

            if(result > 0.44):  # sjekker om resultatet fra "similar(a,b)" er større enn 0.44, (44% like)
                
                #lagrer informasjonen i kolonnene på gitt rad
                organisasjonsnummer = line['Organisasjonsnummer']   
                nk = line['Næringskode 1.beskrivelse']
                navn = line['Navn']
                hjemmeside = line["Hjemmeside"]

                #setter verdiene inn i TreeViewen
                tree.insert("", 0, values=(organisasjonsnummer,navn ,nk , hjemmeside))



def saveNotes():    #funksjon som lagrer notatene som du har skrevet etter å ha trykket på "saveNotesBtn"
    notes = infoWindow.get("1.0", END) + "\n ____Notater____\n" +  notesWindow.get("1.0", END) # henter teksten fra infoWindow og lagrer den i Notes stringen
    
    #  åpner en filedialog og lager ett nytt tekst dokument.
    f = fd.asksaveasfile(initialfile= "Untitled.txt", defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Documents","*.txt")])

    #  skriver notatene inn i tekstdokumentet.
    f.write(notes)


#Frame Layout
topFrame = Frame(root, bg="lightgrey")
topFrame.pack(side=TOP,anchor=N, expand=YES, fill=X)

rightFrame = Frame(root, bg="lightgrey")
rightFrame.pack(side=RIGHT, anchor=NW,expand=YES,fill=X)

leftFrame = Frame(root, bg="lightgrey")
leftFrame.pack(side=LEFT,anchor=N)



def openWebPage(url):   #   åpner nettsiden til valgt bedrift (dersom de har en nettside)
    webbrowser.open_new(url)

def openProffPage(organisasjonsnummer): #åpner proff.no med organisasjonsnummeret til bedriften
    webbrowser.open_new("https://proff.no/bransjes%C3%B8k?q=" + str(organisasjonsnummer))

def chooseFile():   #   setter en global variabel til path av dokumentet du har valgt
    global filename
    filename = fd.askopenfilename()
    #   oppdaterer "selectedFileLabel" til å vise hvilket dokument du bruker.
    selectedFileLabel.configure(text=filename)

def selectItem():   #   Funksjon som legger informasjonen til en bedrift inn i øverste tekstboksen 
    for item in tree.selection():
        tree.focus()

        #   henter verdiene fra de forskjellige cellene i Treeview

        item = tree.item(item)
        items = item["values"]
        organisasjonsnummer = items[0]
        hjemmeside = items[3]

    #ADD INFO TO INFO BOARD

    with open(filename, "r") as f:  #   åpner valgt fil og leser gjennom og setter informasjonen fra rett rad inn i tekstboksen
        csv_reader = csv.DictReader(f, delimiter=',')

        for line in csv_reader:

            #   sjekker om organisasjonsnummeret fra valgt bedrift matcher organisasjonsnummeret i csv fil
            if(str(organisasjonsnummer) == str(line["Organisasjonsnummer"])):

                #   sletter allerede eksisterende tekst fra info tekstboksen (infoWindow)
                infoWindow.delete("1.0",END)
                #   åpner tekstboksen slik at den kan endres på
                infoWindow.config(state=NORMAL)


                for key in line:    #   looper gjennom dictionary(line) og legger hver key("Organisasjonsnummer" : "data" inn i tekstboksen linje for linje)
                    infoWindow.insert(INSERT,key + " : " + line[key] + "\n")

                    if(key == "Navn"):  #   dersom key = navnet på bedriften oppdateres labels med navnet

                        #   legger organisasjonsnummeret inn i allInfoLabel line[key] (bedriftsnavn)
                        allInfoLabel.configure(text="Alt Info Om: " + str(organisasjonsnummer) + " | " + line[key])

                        #   sjekker om bedriften har nettside eller ikke og oppdaterer linkToWebsiteLabel
                        if(hjemmeside == ""):
                            linkToWebsiteLabel.configure(text="Ingen nettside")
                        else:
                            linkToWebsiteLabel.configure(text=str(hjemmeside))

                #   låser tekstboksen så den ikke kan redigeres
                infoWindow.config(state=DISABLED)

    #   binder klikk til openWebPage() og openProffPage()
    linkToWebsiteLabel.bind("<Button-1>", lambda e: openWebPage(str(hjemmeside)))
    linkToProffLabel.bind("<Button-1>", lambda e: openProffPage(str(organisasjonsnummer)))


#definisjon av ulike widgets som søkefelt, knapper, og labels
searchContent = StringVar()
searchEntry = ttk.Entry(topFrame,textvariable=searchContent, width=40)
searchEntry.pack(padx=10,pady=10, side=LEFT)

searchBtn = ttk.Button(topFrame, text="Søk", command=search)
searchBtn.pack(padx=10,pady=10, side=LEFT)

selectBtn = ttk.Button(topFrame, text="Velg", command=selectItem)
selectBtn.pack(padx=10,pady=10, side=LEFT)

openFileBtn = ttk.Button(topFrame, text="Åpne fil", command=chooseFile)
openFileBtn.pack(padx=10,pady=10, side=LEFT)

selectedFileLabel = Label(topFrame, text="")
selectedFileLabel.pack(side=LEFT)

allInfoLabel = Label(rightFrame, text="Alt Info Om : N/A", font="ARIAL 17")
allInfoLabel.pack(side=TOP,anchor=NW)

linkToWebsiteLabel = Label(rightFrame, text="Hjemmeside: N/A", font="ARIAl 12", fg="blue", cursor="hand2")
linkToWebsiteLabel.pack(side=TOP, anchor=NW, padx=5,pady=5)

linkToProffLabel = Label(rightFrame, text="proff.no", font="ARIAl 12", fg="blue", cursor="hand2")
linkToProffLabel.pack(side=TOP, anchor=NW, padx=5)

infoWindow = Text(rightFrame, font="ARIAL 12")
infoWindow.pack(side=TOP,anchor=CENTER, fill=X, padx=10,pady=10,ipady=5)



notesLabel = Label(rightFrame, text="Notater: ", font="ARIAL 17")
notesLabel.pack(side=TOP,anchor=W)

notesWindow = Text(rightFrame, font="ARIAL 12", height=15, width=20)
notesWindow.pack(side=TOP,anchor=CENTER, fill=X, padx=10,pady=10,ipady=5)

saveNotesBtn = ttk.Button(rightFrame, text="Lagre", command=saveNotes)
saveNotesBtn.pack(side=TOP, anchor=NW, pady=15,padx=15)

#   definerer tabellen som viser bedrifter fra søket.

TableMargin = Frame(leftFrame, width=500)
TableMargin.pack(padx=10,pady=10)
scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
tree = ttk.Treeview(TableMargin, columns=("Organisasjonsnummer", "Navn", "Næringskode 1", "Hjemmeside"), height=200, selectmode="browse", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)
tree.heading('Organisasjonsnummer', text="Organisasjonsnummer", anchor=W)
tree.heading('Næringskode 1', text="Næringskode Beskrivelse", anchor=W)
tree.heading('Navn', text="Bedrift Navn", anchor=W)
tree.heading('Hjemmeside', text="Hjemmeside")
tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=150)
tree.column('#2', stretch=NO, minwidth=0, width=250)
tree.column('#3', stretch=NO, minwidth=0, width=300)
tree.column('#4', stretch=NO, minwidth=0, width=300)
tree.pack()





#============================INITIALIZATION==============================
if __name__ == '__main__':
    root.mainloop()