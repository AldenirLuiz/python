from tkinter import Frame, Button, Toplevel, Entry, messagebox
from mainLayout import Layout as Lay
from manage import ViewCard
from dataHandler import HandlerDB as DB
from pdf_print import Header
import os

class TableFrame:
    """
        classe de configuracao da interface da tabela
    """
    _cards = ViewCard().layers
    
    _labels:dict[str: str] = {
        'btt_adict': 'Adicionar Nova',
        'btt_print': 'Imprimir',
        'btt_save': 'Salvar Dados',
        'btt_clear': 'Limpar Campos',}


    def __init__(self, _root: Frame, _data:dict=None, _type:str=None) -> None:
        
        self.root= _root
        self.table_frame = Frame(_root)
        self.type_of = _type
        
        if self.type_of == 'label':
            self.comand = lambda: TopLevelWidow(Toplevel(), _type='entry'),
            self.cards = self._cards
        else:
            self.comand = lambda: CalcData(self.cards),
            self.cards = Process().exclude_fields()

        if _data:
            self._data_table = _data
        else:
            self._data_table = None
        MyLayout(self.root, self.comand, _data, _type=self.type_of, )
        

class Process:
    _exclude=[
        'total_cobrado',
        'total_vendido',
        'entrega_deposito',
        'total_de_fichas',
        'total_na_rua']
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
    def __init__(self, data:dict) -> dict:
        self.data = data
        self.processed = self.process_data()


    def process_data(self,):

        for key in self.data.keys():
            if isinstance(self.data[key], Entry):
                self.processed_data.update(
                    {
                        f'{key}': self.data[key].get()})
                
        self.processed_data.update({
            'total_cobrado': 
                int(self.data['saldo_cobrado'].get()) + 
                int(self.data['repasse_cobrado'].get()),
            'total_vendido': 
                int(self.data['venda_anterior'].get()) - 
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
 
 

class PdfGen:
    def __init__(self, data) -> None:
        self.browsers = ["firefox", "chrome", "edge", "explorer"]
        self.template = Header(data, None)
        self.template.create_template()
        for browser in self.browsers:
            if not os.system(f"{browser} index.html"):
                print('A Pagina foi gerada.')
                return None
        


class MyLayout:
    """
        Construindo Interface da tabela de acordo com os dados contidos no arquivo de configuracao .json
    """
    _tipo = ['label', 'entry']
    _db = DB('data')
    def __init__(self, _root, _command, _data=None, _type='label') -> None:
        self.table_frame = Frame(_root)
        self.widgets_values = dict()

        for card in ViewCard.layers:
            self.btt_row = Frame(_root)
            if card != 'celNomesL4': # detectando e construindo o frame dos buttons
                self.widgets_values.update(Lay.creat_lay(
                    self.btt_row, ViewCard.layers[card], _type, data=_data,
                    font=('arial', 12)))
                
            else: # construindo os demais frames dos cards
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
        else:
            command_button.config(command=lambda: TopLevelWidow(Toplevel(), _type='entry'))

    def add_data(self):
        try:
            data = CalcData(self.widgets_values).dict_val()
            if self._db.query_add(CalcData(self.widgets_values).dict_val()) == "All data are aded":
                messagebox.showinfo('showinfo',"Os Dados Foram Inseridos\nTudo Ok")
                print("passed")
            else:
                print('Nenhum dado foi inserido')
        except ValueError as _error:
            messagebox.showwarning('showwarning',"Um ERRO ocorreu ao tentar guardar os dados\nVerifique os dados antes de salvar")
        

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