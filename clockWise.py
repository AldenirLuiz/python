from tkinter import Label, Tk
from datetime import datetime


class MyClock:
    def __init__(self, master, label: Label):
        self.nossaTela = master
        self.lblRelogio = label
        self.alteracao()

    def alteracao(self):
        now = datetime.now()
        self.lblRelogio['text'] = now.strftime('%H:%M:%S - %d/%m/%Y')
        self.nossaTela.after(1000, self.alteracao)


if __name__ == "__main__":
    janelaRaiz = Tk()
    MyClock(janelaRaiz)
    janelaRaiz.mainloop()
