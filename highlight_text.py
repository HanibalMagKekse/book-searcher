# Import the required library
from tkinter import *

# Create an instance of tkinter frame or window
win = Tk()

# set the size of the window
win.geometry("700x350")

# Create a new frame
frame= Frame(win)

# Add a text widget
text= Text(frame)

# insert a new text
text.insert(INSERT, "Hello, Welcome to TutorialsPoint.com")
text.pack()

# Add a tag to the specified text
text.tag_add("start", "1.0", "1.9")
text.tag_configure("start", background= "black", foreground= "yellow")
frame.pack()

win.mainloop()