from tkinter import Frame, Button, Toplevel, Entry, messagebox, END
from mainLayout import Layout as Lay
from manage import ViewCard
from dataHandler import HandlerDB as DB
from pdf_print import Header
from datetime import datetime, timedelta
import webbrowser


tree_objects = dict()

class MyLayout:
    """
        Construindo Interface da tabela de acordo com os dados contidos no arquivo de configuracao .json
    """
    _db = DB('data')
    _exclude = ['data da rota', 'retorno']

    def __init__(self, _root, _data=None, _type='label') -> None:
        self.my_cards = ViewCard()
        self.root = _root
        self.data = _data
        self.type_of = _type
        self.comand = lambda: None
        self.table_frame = Frame(_root)
        self.widgets_values = dict()
        self.last_value = int()
        self.my_child = None
        self.cards = self.my_cards.layers
        self.table_frame = Frame(_root)
        
    
    def _type(self):

        if self.type_of == 'entry':
            self.comand = lambda: self.add_data()
            self.cards = Process().exclude_fields()
            
        else:
            self.comand = lambda: tree_objects.update({'child':MyCards(
                _root=Toplevel(),
                _type='entry', 
                _data=self.data,)})
            

    def add_data(self):
        try:
            if self.data and self.data.get('venda_nova') != None:
                self.last_value = int(self.data.get('venda_nova'))
            else:
                self.last_value = 0
            data = CalcData(self.widgets_values, self.last_value).process()
            if self._db.query_add(data) == "All data are aded":
                self.root.destroy()
                for obj in tree_objects.values():
                    del obj
                messagebox.showinfo('showinfo',"Os Dados Foram Inseridos\nTudo Ok")
            else:
                print('Nenhum dado foi inserido')
        except ValueError as _error:
            messagebox.showwarning('showwarning',"Um ERRO ocorreu ao tentar guardar os dados\nVerifique os dados antes de salvar")
        

    def clear_fields(self):
        for widget in self.widgets_values.values():
            if isinstance(widget, Entry):
                widget.delete(0, END)


class MyCards(MyLayout):
    def __init__(self, _root, _data=None, _type='label') -> None:
        super().__init__(_root=_root, _data=_data, _type=_type)
        self.my_cards = ViewCard()
        self._type()
        for obj in tree_objects.values():
            del obj
        self.cards = self.my_cards.layers
        tree_objects['fater'] = self

        for card in self.cards:
            self.frm_row = Frame(self.root)
            
            if card != 'celNomesL4':
                if self.type_of == 'entry' and list(self.cards[card].keys()) == self._exclude:
                    new_data = NewData(self.data).new_data()
                    self.widgets_values.update(Lay.creat_lay(
                        self.frm_row, self.cards[card], _type, data=new_data,
                        font=('arial', 12), default=True))
                else:
                    self.widgets_values.update(Lay.creat_lay(
                        self.frm_row, self.cards[card], self.type_of, data=self.data,
                        font=('arial', 12)))
            else:
                self.frm_btt = Frame(self.frm_row)
                command_button = MyButton(self.frm_btt, 'Cadastrar', self.comand)
                printer_button = MyButton(self.frm_btt, 'Imprimir', lambda:PdfGen(_data))
                
                self.widgets_values.update(Lay.creat_lay(
                    self.frm_row, self.cards[card], self.type_of, 
                    font=('arial', 12), data=_data, subwidget=self.frm_btt))
                self.frm_btt.pack()
            self.frm_row.pack(expand=1, fill='both')
        self.table_frame.pack()
        if _type == 'entry': # requisitando os widgets com dados de entrada
            printer_button.config(text='Limpar', command=lambda: self.clear_fields())
        else:
            command_button.config(command=self.comand)


class Process:
    _exclude=[
        'total_cobrado','total_vendido','entrega_deposito',
        'total_de_fichas','total_na_rua','venda_anterior',]
    def __init__(self) -> None:
        self.my_cards = ViewCard()
        self.data_exclude = self._exclude
        self.temp_cards: dict = self.my_cards.layers

    def exclude_fields(self):
        for cell in self.temp_cards.keys():
            for card in self.temp_cards[cell]:
                for value in self.temp_cards[cell][card]:
                    if value in self.data_exclude:
                        self.temp_cards[cell][card].remove(value)
        return self.temp_cards

    def dict_val(self) -> dict:
        return self.temp_cards


class CalcData:
    def __init__(self, data:dict, last_data=None) -> dict:
        self.data = data
        self.processed_data = dict()

        if last_data:
            self.last_data = last_data
        else:
            #print(self.last_data)
            if self.data.get('total_vendido'):
                if isinstance(self.data.get('total_vendido'), Entry):
                    self.last_data = self.data.get('total_vendido').get()
                else: self.last_data = 0
            else:
                self.last_data = 0

    def process(self):
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
        

 
class PdfGen:
    def __init__(self, data) -> None:
        self.template = Header(data, None)
        self.template.create_template()
        webbrowser.open("index.html", new=0)
        

class NewData:
    context = dict()
    def __init__(self, _data) -> None:

        if _data and 'Tabela Inexistente' not in _data.keys():
            self.context = _data
            self.context.update({
                'nome_da_rota': _data.get('nome_da_rota'),
                'data_da_rota': _data.get('data_para_retorno'),
                'nome_do_vendedor': _data.get('nome_do_vendedor'),
                'data_para_retorno': MyDateFields(
                    datetime.date(datetime.strptime(_data.get('data_para_retorno'), '%d-%m-%y')))})
        else:
            self.context = {
                'data_da_rota': datetime.strftime(datetime.date(datetime.now()), '%d-%m-%y'),
                'data_para_retorno': str(MyDateFields(datetime.date(datetime.now())))
                }

    def new_data(self):
        return self.context


class MyDateFields:
    def __init__(self, current) -> None:
        self.current_date = current
        self.time_diference = timedelta(days=70)
        self.estimate_date = self.current_date + self.time_diference
    
    def __str__(self) -> str:
        return self.estimate_date.strftime('%d-%m-%y')



class MyButton(Button):
    def __init__(cls, _root, _text, _command=None) -> None:
        super().__init__(master=_root, text=_text, command=_command)
        return cls.pack(
            side='left', expand=1, fill='x', 
            pady=32, padx=32, ipadx=8, ipady=8,
            anchor='n',)


if __name__ == "__main__":

    class RequestData:
        data_table: dict = dict()
        _handler = DB(_database='data')
        def __init__(self, _table) -> None:
            self.my_table = _table
            self.data_table: dict = dict(
                zip(
                    self._handler.query_request_columns(self.my_table), 
                    self._handler.request_data(self.my_table)[0]))
        @classmethod        
        def dict_val(self) -> dict:
            return  self.data_table

    from tkinter import Tk, Frame
    dataf = RequestData('Campina')
    dict_data= dataf.data_table
    window = Tk()
    window.tk_strictMotif(1)
    frame = Frame(window)
    frame.pack()
    view = MyCards(_root=frame, _type='label', _data=dict_data)
    window.mainloop()

