from tkinter import *
from tkinter import ttk
from dataHandler import HandlerDB as Db
from clockWise import MyClock
from users_layout import MainView as Users
from main_menu import MainMenu
from my_treeview import MyTable
from table_frame import MyCards
from manage import ViewCard
from SysWay import MyWayApp as way


class NewView:
    _handler_db_users = Db(_database='users')
    _handler_db_data = Db(_database='data')
    list_headers = ['Rota', 'Data', 'Retorno']
    

    menu_names = {
            'Configurações': {
                'Users': lambda:Users(Toplevel()),
                'Sair': lambda:exit(0) },
            'Sobre': {
                'About':  lambda: Toplevel().children(Label(text='Aldenir luiz | ╚2023'))}}
    
    def __init__(self) -> None:
        self.window = Tk()
        self.window.geometry(f'{self.window.winfo_screenwidth()}x{self.window.winfo_screenheight()}')
        self.window.overrideredirect(False)
        #self.window.state('withdrawn')
        self.window.title('Gerenciamento de Dados de Crediario - Corró Variedades')
        #self.icon = PhotoImage(file=way('pessoa.png').walk_sys_file())
        #self.window.iconphoto(True, self.icon)
        self._names = list(self.request_data_users().keys())
        self._routes = list()
        self.text_tables_routes = StringVar(self.window)
        self.text_tables_vendor = StringVar(self.window)
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
        self.frm_rw00_cln01  = Frame(
            self.frm_row01_column_01, 
            relief='ridge', bd=2, 
            width=700, height=800)
        self.frm_rw00_cln01.pack(expand=0, fill='both')
        self.label_hist = Label(self.frm_rw00_cln00, text='Corro Variedades', font=('times new roman', 52))
        self.label_hist.pack(expand=1, fill='x', padx=4, ipadx=4, anchor='n')
        self.label_desc_route = Label(self.frm_rw00_cln00, text='Vendedor:', font=('arial', 12))
        self.label_desc_route.pack(side='left', padx=4, ipadx=4)
        self.combo_values = self.fill_combo()
        self.view_cards = ViewCard()
        self.layers = self.view_cards.layers

        self.combo_vendors = ttk.Combobox( # Combobox Vendedores
            self.frm_rw00_cln00, textvariable=self.text_tables_vendor, 
            values=self.combo_values)
        self.combo_vendors.bind(
            "<<ComboboxSelected>>",
            lambda e: self.request_tree(self.text_tables_vendor.get()))
        self.combo_vendors.pack(side='left', padx=4, pady=4, ipadx=4, ipady=4)
        self.label_desc_vendor = Label(self.frm_rw00_cln00, text='Rota:', font=('arial', 12))
        self.label_desc_vendor.pack(side='left', padx=4, ipadx=4)
        self.combo_routes = ttk.Combobox( # Combobox Rotas
            self.frm_rw00_cln00, textvariable=self.text_tables_routes, 
            values=self._routes,
            exportselection=True)
        self.combo_routes.bind(
            "<<ComboboxSelected>>", 
            lambda e: self.treeview_data(self.text_tables_routes.get())
        )
        self.combo_routes.pack(side='left', padx=4, pady=4, ipadx=4, ipady=4)
        self.main_table = MyTable(
            _root=self.frm_rw01_cln00,
            _columns=self.list_headers,
            _width=120, font=('arial', 12)) .build_view()
        

        self.main_table.bind("<Double-1>", self.treeview_clicked)
        self.combo_vendors.insert('end', self._names[0])
        self.request_tree(self._names[0])
        self.table_frame = Frame(self.frm_rw00_cln01)
        self.view = MyCards(self.table_frame, _type='label')
        self.table_frame.pack()
        self.update()
        
    def update(self):
        self.request_tree(self.text_tables_vendor.get())
        self.window.after(1500, self.update)
        self.window.mainloop()
        
    def request_tree(self, vendor:str):
        data:dict = self._handler_db_data.request_from_vendor(vendor)
        self.combo_routes.delete(0, END)
        self.combo_routes.config(values=list(data.keys()))
        self.treeview_data()
    
    def fill_combo(self):
        temp=str()
        if temp := self._names :
            temp = self._names
            return temp
        return ["Nenhum Usuario"] 


    def treeview_data(self, _table=None, single=None):
        tree_data = list()
        vendor:str = self.text_tables_vendor.get()
        if single:
            data = self._handler_db_data.request_from_vendor(vendor)
        else:
            data = self._handler_db_data.request_from_vendor(vendor=vendor, table=_table)
        for _iten in self.main_table.get_children():
            self.main_table.delete(_iten)
        for result in data.keys():
            for value in data[result]:
                str_date: str = value[1].replace('-', ' / ')
                str_date_return: str = value[3].replace('-', ' / ')
                self.main_table.insert('', 0, values=[value[0], str_date, str_date_return])
                tree_data.append([value[0], str_date, str_date_return])
        return tree_data


    def request_data_users(self,):
        dictdata = dict()
        tables: list[str] = self._handler_db_users.query_request_tables()
        columns = self._handler_db_users.query_request_columns(tables[0])
        data = self._handler_db_users.request_data(tables[0])
    
        for _data in data:
            tempdata = dict(zip(columns, _data))
            dictdata.update({f"{tempdata['user_name_entry']}": tempdata})
        return dictdata


    def treeview_clicked(self, event):
        self.table_frame.destroy()

        item = self.main_table.selection()[0]
        values = self.main_table.item(item, 'values')

        data = self._handler_db_data.request_data_from_column(
            values[1].replace(' / ','-'), values[2].replace(' / ','-'), values[0])
        
        columns = self._handler_db_data.query_request_columns(values[0])
        _dict_data = dict(zip(columns, data[0]))
        
        self.table_frame = Frame(self.frm_rw00_cln01)
        self.view = MyCards(self.table_frame, _data=_dict_data, _type='label', _cards=self.layers)
        self.table_frame.pack()


if __name__ == '__main__':
    NewView()