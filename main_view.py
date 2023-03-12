from tkinter import *
from tkinter import ttk
from dataHandler import HandlerDB as Db
from mainLayout import Layout as Lay
from manage import ViewCard
from clockWise import MyClock
from users_layout import MainView as Users
from main_menu import MainMenu
from my_treeview import MyTable

class NewView:
    _handler = Db()
    cards = ViewCard.layers
    list_headers = ['Rota', 'Data', 'Retorno']
    def __init__(self) -> None:
        self.window = Tk()
        
        self._names = dict(zip(
            self._handler.query_request_columns('users'), 
            self._handler.request_data('users')[0],
        ))
        self.text_tables_routes = StringVar(self.window)
        self.text_tables_vendor = StringVar(self.window)
        
        self.menu_names = {
            'Gerenciamento': {
                'Configuracoes': lambda:print('configuracoes'), 
                'Users': lambda:Users(Toplevel())
            },
        }

        self.menu = MainMenu(master=self.window, names=self.menu_names)

        self.frm_primary_rows = Frame(self.window, relief='ridge', bd=2)
        self.frm_secondary_rows = Frame(self.window,)
        self.frm_primary_rows.pack(side='top', expand=0, fill='x')
        self.frm_secondary_rows.pack(side='bottom', expand=1, fill='both')

        self.frm_labels = Frame(self.frm_primary_rows)
        self.label_0 = Label(self.frm_labels, text='', anchor='ne', font=('arial', 12), justify='right', width=30)
        self.label_0.pack(side='right', expand=1, fill='x')
        self.clock = MyClock(self.frm_labels, self.label_0)
        self.frm_labels.pack(expand=0, fill='x')

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
        
        self.combo_vendors = ttk.Combobox( # Combobox Vendedores
            self.frm_rw00_cln00, textvariable=self.text_tables_routes, 
            values=self._names['user_name_entry'])
        self.combo_vendors.pack(side='left', padx=4, pady=4, ipadx=4, ipady=4)
        
        self.label_desc_vendor = Label(self.frm_rw00_cln00, text='Rota:', font=('arial', 14))
        self.label_desc_vendor.pack(side='left', padx=4, ipadx=4)

        self.combo_routes = ttk.Combobox( # Combobox Rotas
            self.frm_rw00_cln00, textvariable=self.text_tables_vendor, 
            values=self._handler.query_request_tables())
        self.combo_routes.pack(side='left', padx=4, pady=4, ipadx=4, ipady=4)
        
        self.main_table = MyTable(
            _root=self.frm_rw01_cln00,
            _columns=self.list_headers,
            _width=120,
        ).build_view()

        # self.create_view('Campina_23_6_2023')
        self.table_frame = Frame(self.frm_rw00_cln01)
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
        

    def create_view(self, _table=None):
        self.table_frame.destroy()
        self.table_frame = Frame(self.frm_rw00_cln01)

        if _table:
            _data_table = self.request_data(_table)
        else:
            _data_table = None
        
        for card in self.cards.keys():
            if card != 'celNomesL4':
                row = Frame(self.table_frame)
                Lay.creat_lay(row, self.cards[card], 'label', font=('arial', 8))
                row.pack(expand=1, fill='both')
            else:
                row = Frame(self.table_frame)
                frm_btt = Frame(row)
                btt_add = Button(frm_btt, text='Adicionar')
                btt_print = Button(row, text='Imprimir')
                btt_add.pack(side='left')
                btt_print.pack(side='right')

                Lay.creat_lay(row, self.cards[card], 'label', font=('arial', 8), subwidget=frm_btt)
                row.pack(expand=1, fill='both')
        self.table_frame.pack()


if __name__ == '__main__':
    NewView()