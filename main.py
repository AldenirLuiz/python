
from tkinter import *
from tkinter import ttk
from table import MyTable
from dataHandler import HandlerDB as Db
from manage import ViewCard
from mainLayout import Layout as Lay
from clockWise import MyClock


class MainWindow:
    """Janela principal da aplicacao"""
    texts: list[str] = ['Tablela', 'Cadastro']
    _handler = Db()
    cards = ViewCard.layers

    def __init__(self):
        self.window = Tk()
        self.window.geometry('800x600')
        self.window.title('Sistema de Gerenciamento de Crediário')
        self.frm_00 = Frame(self.window)
        self._names: dict = self.request_table_names()
        self.table_frame = Frame(self.frm_00)
        self.menu = MainMenu(this=self, master=self.window, table_names=self._names)

        self.frm_labels = Frame(self.frm_00)
        self.label_00 = Label(self.frm_labels, text="Planilha de Cobranca", font=('arial', 12), justify='left')
        self.label_00.pack(side='left', expand=1, fill='x', anchor='ne', padx=4, pady=4, ipady=4, ipadx=4)
        self.label_0 = Label(self.frm_labels, text='', anchor='ne', font=('arial', 12), justify='right', width=30)
        self.label_0.pack(side='right', expand=1, fill='x')

        self.clock = MyClock(self.frm_labels, self.label_0)

        self.frm_labels.pack(expand=1, fill='x', padx=4, pady=4, ipady=4, ipadx=4)
        self.frm_00.pack()

    def request_table_names(self) -> dict:
        """requisitando e formatando os nomes das tableas existentes
        <:return dict column|data"""

        _table_names: list = self._handler.query_request_tables()
        _format_tables: list = self._handler.format_table_names(_table_names)

        dict_table = dict(zip(  # empacotando os dados em chaves:valores
            _table_names, _format_tables))

        return dict_table

    def create_view(self, _table):
        self.table_frame.destroy()
        self.table_frame = Frame(self.frm_00)

        my_table = _table
        data_table: dict = MyTable.ret_query_data(_table=my_table)
        for card in self.cards:  # percorrendo os dados de layout arquivo cellNames.json
            frm = Frame(self.table_frame)
            # filtrando nomes dos cards (adicione ou remova cards na variavel de classe _exclude_cards)
            Lay.creat_lay(frm, self.cards[card], 'label', data=data_table)
            frm.pack(expand=1, fill='both')
        self.table_frame.pack()


class MainMenu:
    def __init__(self, this, master: Tk, table_names: dict):
        self.object = this
        self.menubar = Menu(master)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.editmenu = Menu(self.menubar, tearoff=1)

        self.add_cascade_(self.menubar, 'Tabelas')
        self.add_cascade_(self.menubar, 'Usuarios')

        self.filemenu.add_separator()

        for _table in table_names.keys():
            self.add_commando(self.editmenu, table_names[_table], _table)
            master.configure(menu=self.menubar)
            self.filemenu.add_separator()

    def add_cascade_(self, menu: Menu, text: str):
        """Definindo Nomes no menu da camada superior
        <param> >menu<: objeto Menu a receber a lista
        <param> >text<: texto de exibicao da lista"""

        menu.add_cascade(
            label=text,
            menu=self.filemenu,
            command=lambda: self.add_commando(text),
            activebackground='black',
            activeforeground='green'
        )

    def add_commando(self, context,  nome: str, arg_name=None):
        """Definindo Nomes no menu da camada inferior
        <param> >nome<: texto de exibicao"""
        self.filemenu.add_command(
            label=nome,
            command=lambda x=arg_name:
            # MyTable(arg_name)
            self.object.create_view(x)
        )


class ContainerView(MainWindow):

    def __init__(self):
        super().__init__()

        self.container = Frame(self.frm_00)

        # self.create_combo()
        self.container.pack(expand=1, fill='both')
        self.text_tables = StringVar(self.window)
        self.text_vendors = StringVar(self.window)
        self.diagram = dict()
        # self.create_view()

        self.window.mainloop()

    def create_combo(self):
        # Lay.creat_lay(self.frm_00, self.cards['celNomesL0'], 'label')
        self.text_tables = StringVar()
        self.text_vendors = StringVar()
        list_table = ttk.Combobox(
            self.frm_00,
            textvariable=self.text_tables,
            exportselection=True,
            values=list(self._names.values()),)
        list_table.pack(side='left', expand=True, fill='both')

        list_table.bind('<<ComboboxSelected>>', self.combo_command)
        for table in self._names.values():
            list_table.insert(END, table)

    def combo_command(self, event):
        print(f"texto: {self.text_tables.get()}\nEvento: {event}")



if __name__ == "__main__":
    ContainerView()
