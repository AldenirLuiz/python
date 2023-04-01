from tkinter import Frame, Button, Toplevel, Entry, messagebox, END
from mainLayout import Layout as Lay
from manage import ViewCard
from dataHandler import HandlerDB as DB
from pdf_print import Header
from datetime import datetime, timedelta
import webbrowser

class TableFrame:
    """
        classe de configuracao da interface da tabela
    """
    _cards = ViewCard().layers

    def __init__(self, _root: Frame, _data:dict=None, _type:str=None) -> None:
        
        self.root= _root
        self.table_frame = Frame(_root)
        self.type_of = _type
    
        if self.type_of == 'label':
            self.comand = lambda: TopLevelWidow(Toplevel(), _type='entry'),
            self.cards = self._cards
        else:
            self.comand = lambda: CalcData(self.cards, _data),
            self.cards = Process().exclude_fields()

        if _data:
            self._data_table = _data
        else:
            self._data_table = None
        MyLayout(self.root, self.comand, _data, _type=self.type_of)
        

class Process:
    _exclude=[
        'total_cobrado','total_vendido','entrega_deposito',
        'total_de_fichas','total_na_rua','venda_anterior',]
    temp_cards: dict = ViewCard().layers
    def __init__(self) -> None:
        self.data_exclude = self._exclude

    def exclude_fields(self):
        for cell in self.temp_cards.keys():
            for card in self.temp_cards[cell]:
                for value in self.temp_cards[cell][card]:
                    if value in self.data_exclude:
                        self.temp_cards[cell][card].remove(value)

    def include_calc_fields(self, data, include):
        
        for cell in data:
            if isinstance(data[cell], Entry):
                print(data[cell].get())
    
    def dict_val(self) -> dict:
        return self.temp_cards


class CalcData:
    processed_data = dict()
    last_data = int()
    def __init__(self, data:dict, last_data=None) -> dict:
        self.data = data
        self.processed = self.process_data()

        if last_data:
            self.last_data = last_data
        else:
            self.last_data = self.data['venda_anterior']

    def process_data(self,):

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
                int(self.data['vl_fichas_branco'].get())
                })
        
    @classmethod
    def dict_val(self) -> dict:
        print(f'dict')
        return self.processed_data

 
class PdfGen:
    def __init__(self, data) -> None:
        self.template = Header(data, None)
        self.template.create_template()
        webbrowser.open("index.html", new=0)
        
        
class MyLayout:
    """
        Construindo Interface da tabela de acordo com os dados contidos no arquivo de configuracao .json
    """
    _db = DB('data')
    _exclude = ['data da rota', 'retorno']
    def __init__(self, _root, _command, _data=None, _type='label') -> None:
        self.table_frame = Frame(_root)
        self.widgets_values = dict()
        self.last_value = int()
        if _data != None:
            self.last_value = _data.get('venda_nova')
        else:
            self.last_value = None

        for card in ViewCard.layers:
            self.btt_row = Frame(_root)
            if card != 'celNomesL4':
                if _type == 'entry' and list(ViewCard.layers[card].keys()) == self._exclude:
                    new_data = {
                        'nome_da_rota': _data.get('nome_da_rota'),
                        'data_da_rota': _data.get('data_para_retorno'),
                        'nome_do_vendedor': _data.get('nome_do_vendedor'),
                        'data_para_retorno': MyDateFields(
                            datetime.date(datetime.strptime(_data.get('data_para_retorno'), '%d-%m-%y'))
                        )

                    }
                    self.widgets_values.update(Lay.creat_lay(
                        self.btt_row, ViewCard.layers[card], _type, data=new_data,
                        font=('arial', 12), default=True))
                else:
                    self.widgets_values.update(Lay.creat_lay(
                        self.btt_row, ViewCard.layers[card], _type, data=_data,
                        font=('arial', 12)))
                
            else:
                self.frm_btt = Frame(self.btt_row)
                command_button = MyButton(self.frm_btt, 'Cadastrar', _command)
                printer_button = MyButton(self.frm_btt, 'Imprimir', lambda:PdfGen(_data))
                
                self.widgets_values.update(Lay.creat_lay(
                    self.btt_row, ViewCard.layers[card], _type, 
                    font=('arial', 12), data=_data, subwidget=self.frm_btt))
                
                self.frm_btt.pack()
            self.btt_row.pack(expand=1, fill='both')
        self.table_frame.pack()

        if _type == 'entry': # requisitando os widgets com dados de entrada
            command_button.config(command=lambda: self.add_data())
            printer_button.config(text='Limpar', command=lambda: self.clear_fields())
        else:
            command_button.config(command=lambda: TopLevelWidow(Toplevel(), _type='entry', _data=_data))
            

    def add_data(self):
        try:
            data = CalcData(self.widgets_values, self.last_value).dict_val()
            if self._db.query_add(CalcData(self.widgets_values).dict_val()) == "All data are aded":
                messagebox.showinfo('showinfo',"Os Dados Foram Inseridos\nTudo Ok")
                print("passed")
            else:
                print('Nenhum dado foi inserido')
        except ValueError as _error:
            messagebox.showwarning('showwarning',"Um ERRO ocorreu ao tentar guardar os dados\nVerifique os dados antes de salvar")
        

    def clear_fields(self):
        for widget in self.widgets_values.values():
            if isinstance(widget, Entry):
                widget.delete(0, END)



class MyDateFields:
    def __init__(self, current) -> None:
        self.current_date = current
        self.time_diference = timedelta(days=70)
        self.estimate_date = self.current_date + self.time_diference
    
    def __str__(self) -> str:
        return self.estimate_date.strftime('%d/%m/%y')



class MyButton(Button):
    def __init__(cls, _root, _text, _command=None) -> None:
        super().__init__(master=_root, text=_text, command=_command)
        return cls.pack(
            side='left', expand=1, fill='x', 
            pady=32, padx=32, ipadx=8, ipady=8,
            anchor='n',)


class TopLevelWidow(TableFrame):
    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()



if __name__ == "__main__":
    print(MyDateFields(datetime.date(datetime.now())))
    print(datetime.date(datetime.now()))

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
    dataf = RequestData('Itaporanga')
    dict_data= dataf.data_table
    cards = ViewCard.layers
    window = Tk()
    window.tk_strictMotif(1)
    frame = Frame(window)
    frame.pack()
    view = TableFrame(_root=frame, _type='label', _data=dict_data)
    window.mainloop()

