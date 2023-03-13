from tkinter import *
from tkinter.ttk import *

window = Tk()

list_header = ['Nome', 'Sexo', 'Telefone', 'Email']
treeview = Treeview(window, selectmode='extended', columns=list_header, show='headings')
count = 0
for head in list_header:
    treeview.heading(count, text=head, anchor='n')
    count+=1
treeview.pack(expand=0, fill=None)


window.mainloop()