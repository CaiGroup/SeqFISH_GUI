def printtext():
    global e
    string = e.get() 
    text.insert(INSERT, string)   

from tkinter import *
root = Tk()
root.title('Name')
text = Text(root)
e = Entry(root) 
e.pack()
e.focus_set()
b = Button(root,text='okay',command=printtext)
text.pack()
b.pack(side='bottom')
root.mainloop()
