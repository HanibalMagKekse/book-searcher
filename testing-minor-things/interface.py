from tkinter import *

root = Tk()

e = Entry(root, width=50)
e.pack()
e.insert(0, "Enter:")

def myClick():
    hello = e.get()
    myLabel = Label(root,text=hello)
    myLabel.pack()

myButtons = Button(root, text="Enter", command=myClick)
myButtons.pack()

root.mainloop()