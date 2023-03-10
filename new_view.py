from tkinter import *
from tkinter import ttk
from dataHandler import HandlerDB as Db
from table import MyTable
from mainLayout import Layout as Lay
from manage import ViewCard
from clockWise import MyClock

class NewView:
    _handler = Db()
    cards = ViewCard.layers
    list_headers = ['Rota', 'Data', 'Retorno']
    def __init__(self) -> None:
        super().__init__()

        self.window = Tk()
        
        self._names: dict = self.request_table_names()
        self.text_tables_routes = StringVar(self.window)
        self.text_tables_vendor = StringVar(self.window)
        self.menu = MainMenu(this=self, master=self.window, table_names=self._names)
        self.img_add_user = PhotoImage(file='add_user.png')

        self.frm_primary_rows = Frame(self.window, relief='ridge', bd=2)
        self.frm_secondary_rows = Frame(self.window,)
        self.frm_primary_rows.pack(side='top', expand=1, fill='both')
        self.frm_secondary_rows.pack(side='bottom', expand=1, fill='both')

        self.frm_labels = Frame(self.frm_primary_rows)
        self.label_0 = Label(self.frm_labels, text='', anchor='ne', font=('arial', 12), justify='right', width=30)
        self.label_0.pack(side='right', expand=1, fill='x')
        self.clock = MyClock(self.frm_labels, self.label_0)
        self.frm_labels.pack()

        self.frm_row01_column_00 = Frame(self.frm_secondary_rows)
        self.frm_row01_column_01 = Frame(self.frm_secondary_rows) # side='left'
        self.frm_row01_column_00.pack(side='left', expand=1, fill='both')
        self.frm_row01_column_01.pack(side='right', expand=1, fill='both')

        # view quadro geral de rotas
        self.frm_rw00_cln00  = Frame(self.frm_row01_column_00, relief='ridge', bd=2) #linha p/ combobox
        self.frm_rw01_cln00  = Frame(self.frm_row01_column_00, relief='ridge', bd=2) # linha p/ tabela
        self.frm_rw00_cln00.pack(side='top', expand=1, fill='both')
        self.frm_rw01_cln00.pack(side='bottom', expand=1, fill='both')

        # view quadro de visualizacao da planilha
        self.frm_rw00_cln01  = Frame(self.frm_row01_column_01, relief='ridge', bd=2)
        self.frm_rw00_cln01.pack(expand=1, fill='both')

        self.label_hist = Label(self.frm_rw00_cln00, text='Corro Variedades', font=('times new roman', 52))
        self.label_hist.pack(expand=1, fill='x', padx=4, ipadx=4, anchor='n')

        self.label_desc_route = Label(self.frm_rw00_cln00, text='Vendedor:', font=('arial', 14))
        self.label_desc_route.pack(side='left', padx=4, ipadx=4)
        self.create_combo(
            ttk.Combobox(
            self.frm_rw00_cln00, textvariable=self.text_tables_routes, 
            values=list(self._names.values())))
        
        self.label_desc_vendor = Label(self.frm_rw00_cln00, text='Rota:', font=('arial', 14))
        self.label_desc_vendor.pack(side='left', padx=4, ipadx=4)
        self.create_combo(
            ttk.Combobox(
            self.frm_rw00_cln00, textvariable=self.text_tables_vendor, 
            values=list(self._names.values())))
        
        self.main_table = ttk.Treeview(
                    self.frm_rw01_cln00,
                    selectmode='extended', columns=self.list_headers, show='headings')
        self.main_table.pack(expand=1, fill='both')

        # self.create_view('Campina_23_6_2023')
        self.table_frame = Frame(self.frm_rw00_cln01)
        for card in self.cards.keys():
            row = Frame(self.table_frame)
            Lay.creat_lay(row, self.cards[card], 'label', font=('arial', 8))
            row.pack(expand=1, fill='both')

        count = 0
        for head in self.list_headers:
            self.main_table.heading(count, text=head, anchor='n')
            self.main_table.column(count, width=120, anchor='n')
            count+=1
    
        self.table_frame.pack()
        self.window.mainloop()


    def command(self):
        print('hello')

    def request_table_names(self, _user=None, _route=None) -> dict:
        """requisitando e formatando os nomes das tableas existentes
        <:return dict column|data"""

        _table_names: list = self._handler.query_request_tables()
        _format_tables: list = self._handler.format_table_names(_table_names)

        dict_table = dict(zip(  # empacotando os dados em chaves:valores
            _table_names, _format_tables))
        return dict_table
        
    
    def create_combo(self, combo:ttk.Combobox):
        combo.pack(side='left', padx=4, pady=4, ipadx=4, ipady=4)
        combo.bind('<<ComboboxSelected>>', self.command)
        for table in self._names.values():
            combo.insert(END, table)
    
    def create_view(self, _table):
        self.table_frame.destroy()
        self.table_frame = Frame(self.frm_rw00_cln01)

        my_table = _table
        data_table: dict = MyTable.ret_query_data(_table=my_table)
        for card in self.cards:  # percorrendo os dados de layout arquivo cellNames.json
            frm = Frame(self.table_frame)
            # filtrando nomes dos cards (adicione ou remova cards na variavel de classe _exclude_cards)
            Lay.creat_lay(frm, self.cards[card], 'label', data=data_table, font=('arial', 10))
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



if __name__ == '__main__':
    NewView()