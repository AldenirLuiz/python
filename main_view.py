from tkinter import *
from tkinter import ttk, messagebox
from dataHandler import HandlerDB as Db
from clockWise import MyClock
from users_layout import MainView as Users
from main_menu import MainMenu
from my_treeview import MyTable
from table_frame import MyCards
from manage import ViewCard
from SysWay import MyWayApp as way
from pdf_print import Header
import webbrowser
from datetime import datetime
from SysWay import MyWayApp as Way

class NewView:
    _handler_db_users = Db(_database='users')
    _handler_db_data = Db(_database='data')
    _db = _handler_db_data
    list_headers = ['Rota', 'Data', 'Retorno']
    menu_names = {
            'Configurações': {
                'Users': lambda:Users(Toplevel()),
                'Sair': lambda:exit(0) },
            'Sobre': {
                'About':  lambda: Toplevel().children(Label(text='Aldenir luiz | ╚2023'))}}
    
    def __init__(self) -> None:
        # Configuracoes primarias da janela principal
        self.window = Tk()
        self.window_style = ttk.Style(self.window)
        self.window_style.configure("BW.TLabel", foreground="black", background="cyan")
        self.window.geometry(
            f'{self.window.winfo_screenwidth()}x{self.window.winfo_screenheight()}')
        self.window.overrideredirect(False)
        self.window.state('normal')
        self.window.title('Gerenciamento de Dados de Crediario - Corró Variedades')
        self.icon = PhotoImage(file=way('icone.png').walk_sys_file())
        self.window.iconphoto(True, self.icon)
        # Containers de nomes para rotas e vendedores
        self._names = list(self.request_data_users().keys())
        self._routes = list()
        # Variavel de estado de selecao na treeview de rotas e vendedores
        self.text_tables_routes = StringVar(self.window)
        self.text_tables_vendor = StringVar(self.window)
        # objeto Menu
        self.menu = MainMenu(master=self.window, names=self.menu_names)
        # Containers da linhas primarias e secundarias de widgets
        self.frm_primary_rows = MyFrame(self.window, 'top', 0)
        self.frm_secondary_rows = MyFrame(self.window, 'bottom', 1)
        self.frm_labels = MyFrame(self.frm_primary_rows, None, 0)
        # Labels primarias e variavel do objeto Relogio
        self.label_0 = ttk.Label(
            self.frm_labels, text='', anchor='ne', font=('arial', 12), 
            justify='right', width=30,)
        self.label_0.pack(side='right', expand=1, fill='x')
        self.clock = MyClock(self.frm_labels, self.label_0)
        # Containers das colunas primarias e secundarias
        self.frm_row01_column_00 = MyFrame(self.frm_secondary_rows, 'left', 1)
        self.frm_row01_column_01 = MyFrame(self.frm_secondary_rows, 'right', 1)
        # Container do quadro de selecao de rotas e vendedores
        self.frm_rw00_cln00  = MyFrame(self.frm_row01_column_00, 'top', 1) #linha p/ combobox
        self.frm_rw01_cln00  = MyFrame(self.frm_row01_column_00, 'bottom', 1) # linha p/ tabela
        # Container do quadro de visualizacao da planilha
        self.frm_rw00_cln01  = MyFrame(self.frm_row01_column_01, None, 1, _width=700, _height=800)
        self.label_hist = ttk.Label( master=self.frm_rw00_cln00, text='Corro Variedades', font=('times new roman', 52))
        self.label_hist.pack(expand=1, fill='x', padx=4, ipadx=4, anchor='n')
        self.label_desc_route = ttk.Label( master=self.frm_rw00_cln00, text='Vendedor:', font=('arial', 12))
        self.label_desc_route.pack(side='left', padx=4, ipadx=4)
        self.combo_values = self.fill_combo()
        self.data = dict()

        self.combo_vendors = ttk.Combobox( # Combobox Vendedores
            self.frm_rw00_cln00, textvariable=self.text_tables_vendor, 
            values=self.combo_values)
        self.combo_vendors.bind(
            "<<ComboboxSelected>>",
            lambda e: self.request_tree(self.text_tables_vendor.get()))
        self.combo_vendors.pack(side='left', padx=4, pady=4, ipadx=4, ipady=4)
        self.label_desc_vendor = ttk.Label( master=self.frm_rw00_cln00, text='Rota:', font=('arial', 12))
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
            _width=120, font=('arial', 12)).build_view()
        self.btt_pack_treeview = MyFrame(self.frm_rw01_cln00, 'bottom', 1)
        self.btt_delete = MyButton(
            self.btt_pack_treeview, _text='Delete', _bg='red', _command=lambda: self.delete_data()
        )
        self.btt_manage = MyButton(
            self.btt_pack_treeview, _text='Editar', _bg='green', _command=lambda: self.edit_data()
        )
        self.btt_manage.config(state='disabled')
        #self.btt_pack_treeview.pack(side='bottom',expand=1, fill='x', padx=2, pady=0, ipadx=2, ipady=0)
        
        self.main_table.bind("<Double-1>", self.treeview_clicked)
        self.combo_vendors.insert('end', self._names[0])
        self.request_tree(self._names[0])
        self.table_frame = Frame(self.frm_rw00_cln01)
        self.btt_pack = Frame(self.table_frame)
        self.table_frame.pack(side='top')

        self.comands = {
            'label':[
                lambda: self.treeview_clicked(None, 'entry'),
                lambda: PdfGen(self.get_data())],
            'entry':[
                lambda: self.add_data(self.view.manager()),
                lambda: self.clear_fields()]}
        
        self.view = EntryView(self.table_frame, self.data, 'label', self.comands['label']).build()

        self.window.mainloop()

class NewViewFunc(NewView):
    def __init__(self) -> None:
        super().__init__()

    def pdf_print(self):
        _data = self.get_data()
        print(_data)
        PdfGen(_data)
    
    def delete_data(self):
        item = self.main_table.selection()[0]
        values = self.main_table.item(item, 'values')

        pop_up = messagebox.askquestion(
            'Deseja Apagar?', 
            f"""Tem Certeza que quer apagar a planilha definitivamente?
                Dados a serem apagados: 
                Rota: {values[0]} 
                Data da Rota: {values[1].replace(' ','')}
                Data do Retorno: {values[2].replace(' ','')}""",
            icon='warning')
        print(pop_up)
        if pop_up != 'no':
            self._handler_db_data.delete_data(
                values[1].replace(' / ','-'), 
                values[2].replace(' / ','-'), 
                values[0])
            self.request_tree(self.text_tables_vendor.get())
        else:
            messagebox.showinfo('Nenhum dado alterado.', 'Comando Cancelado Pelo Usuário! Nenhum dado será apagado.')


    def edit_data(self):
        print('Editar')
        pass

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


    def treeview_clicked(self, event, _type=None):
        if _type == None:
            _type_ = 'label'
        else:
            _type_ = _type
        try:
            self.data = self.get_data()
        except:
            self.data = dict()
 
        self.table_frame.destroy()
        self.table_frame = Frame(self.frm_rw00_cln01)
        self.btt_pack = Frame(self.table_frame)

        self.view = EntryView(
                _root=self.table_frame, _data=self.data, _type=_type_, 
                _commands=self.comands[_type_]).build()
        self.table_frame.pack()
    
    def get_data(self):
        item = self.main_table.selection()[0]
        values = self.main_table.item(item, 'values')
        data = self._handler_db_data.request_data_from_column(
            values[1].replace(' / ','-'), 
            values[2].replace(' / ','-'), 
            values[0])
        columns = self._handler_db_data.query_request_columns(values[0])
        return dict(zip(columns, data[0]))


    def add_data(self, _data ):
        try:
            if _data and _data.get('venda_nova') != None:
                self.last_value = int(_data.get('venda_nova').get())
            else:
                self.last_value = 0
            data = CalcData(_data, self.last_value).process()
            if self._db.query_add(data) == "All data are aded":
                messagebox.showinfo('showinfo',"Os Dados Foram Inseridos\nTudo Ok")
                print(
                    f"""                
                {datetime.strftime(datetime.today(), '%d/%m/%Y %H:%M-%S')} ->
                Rota Adicionada:
                {_data.get('nome_da_rota').get()} - {_data.get('data_para_retorno').get()}""")
                self.request_tree(self.text_tables_vendor.get())
            else:
                print('Nenhum dado foi inserido')
        except ValueError as _error:
            messagebox.showwarning('showwarning',"Um ERRO ocorreu ao tentar guardar os dados\nVerifique os dados antes de salvar")
        
    def clear_fields(self):
        for widget in self.view.manager().values():
            if isinstance(widget, Entry):
                widget.delete(0, END)
    

class CalcData:
    def __init__(self, data:dict, last_data=None) -> None:
        self.data = data
        self.processed_data = dict()

        if last_data:
            self.last_data = last_data
        else:
            if self.data.get('total_vendido').get():
                if isinstance(self.data.get('total_vendido'), Entry):
                    self.last_data = self.data.get('total_vendido').get()
                else: self.last_data = 0
            else:
                self.last_data = 0

    def process(self) -> dict:
        for key in self.data.keys():
            if isinstance(self.data[key], Entry):
                self.processed_data.update(
                    {f'{key}': self.data[key].get()})
        self.processed_data.update({
            'data_da_rota': 
                self.data['data_da_rota'].get().replace('/', '-'),
            'data_para_retorno': 
                self.data['data_para_retorno'].get().replace('/', '-'),
            'total_cobrado': 
                int(self.data['saldo_cobrado'].get()) + 
                int(self.data['repasse_cobrado'].get()),
            'total_vendido': 
                int(self.last_data) - 
                int(self.data['devolucao_de_rua'].get()),
            'total_de_fichas': 
                int(self.data['fichas_novas'].get()) +
                int(self.data['fichas_repasse'].get()) +
                int(self.data['fichas_em_branco'].get()),
            'entrega_deposito': 
                int(self.data['compra_deposito'].get()) +
                int(self.data['devolucao_de_rua'].get()) - (
                    int(self.data['venda_nova'].get()) +
                    int(self.data['brindes'].get())),
            'total_na_rua':
                int(self.data['venda_nova'].get())+
                int(self.data['brindes'].get())+
                int(self.data['vl_fichas_branco'].get()),
            'venda_anterior': self.last_data})
        return self.processed_data
        

class EntryView:
    def __init__(self, _root, _data, _type, _commands) -> None:
        self.comand = _commands
        self.layers = ViewCard().layers
        self.root = _root
        self.data = _data
        self.type = _type

        if _type == "label":
            self.names = ['Cadastrar', 'Imprimir']
        else:
            self.names = ['Salvar', 'Limpar']

    def build(self):
        return MyCards(
            _root= self.root, _data=self.data, 
            _type=self.type, _cards=self.layers, 
            _subwidget=NewButtons(self.root, _commands=self.comand, _name=self.names).build())


class PdfGen:
    def __init__(self, data) -> None:
        self.template = Header(data, None)
        self.template.create_template()
        self.browser = webbrowser.get()
        print(f"Browser: {self.browser}\n{self.browser.open_new_tab(Way(file='index.html').walk_sys_file())}")
            

class NewButtons:
    def __init__(self, root, _commands, _name):
        self.btt_pack = Frame(root)
        self.btt_save = MyButton(self.btt_pack, _name[0], _command=_commands[0], _bg='green')
        self.btt_print = MyButton(self.btt_pack, _name[1], _command=_commands[1], _bg='orange')
    
    def build(self):
        return self.btt_pack


class MyButton(Button):
    def __init__(cls, _root, _text, _command=None, _bg=None) -> None:
        super().__init__(master=_root, text=_text, command=_command, bg=_bg)
        return cls.pack(
            side='left', expand=1, fill='x', 
            pady=6, padx=6, ipadx=4, ipady=4,)


class MyFrame(Frame):
    def __init__(cls, _root, _side, _expand=1, _width=None, _height=None) -> None:
        super().__init__(master=_root, relief='sunken', bd=1, width=_width, height=_height)
        return cls.pack(side=_side, expand=_expand, fill='both', ipady=2, ipadx=2)


if __name__ == '__main__':
    NewViewFunc()