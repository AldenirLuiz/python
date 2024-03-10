from tkinter import Frame
from mainLayout import Layout as Lay
from manage import ViewCard
from dataHandler import HandlerDB as DB
from datetime import datetime, timedelta


tree_objects = dict()

class MyLayout:
    """
        Construindo Interface da tabela de acordo com os dados contidos no arquivo de configuracao .json
    """
    _db = DB('data')
    _datefields= ['data da rota', 'retorno']
    _exclude=[
        'total_cobrado','total_vendido','entrega_deposito',
        'total_de_fichas','total_na_rua','venda_anterior',]

    def __init__(self, _root, _data=None, _type='label', _cards=None, _subwidget=None) -> None:
        self.my_cards = ViewCard()
        self.root = _root
        self.data = _data
        self.type_of = _type
        self.comand = lambda: None
        self.table_frame = Frame(_root)
        self.widgets_values = dict()
        self.last_value = int()
        self.my_child = None
        self.table_frame = Frame(_root)
        self.subwidget = _subwidget

        if _cards:
            self.cards = _cards
        else:
            self.cards = self.my_cards.layers
        
    
    def manager(self) -> dict:
        return self.widgets_values


class MyCards(MyLayout):
    def __init__(self, _root, _data=None, _type='label', _cards=None, _subwidget=None) -> None:
        super().__init__(_root=_root, _data=_data, _type=_type, _cards=_cards, _subwidget=_subwidget)
        self.my_cards = ViewCard()
        if _cards:
            self.cards = _cards
        else:
            self.cards = self.my_cards.layers

        for card in self.cards:
            self.frm_row = Frame(self.root)
            
            if card != 'celNomesL4':
                if self.type_of == 'entry' and list(self.cards[card].keys()) == self._datefields:
                    self.widgets_values.update(Lay.creat_lay(
                        self.frm_row, self.cards[card], _type, data=NewData(self.data).new_data(),
                        font=('arial', 12), default=True), _exclude=self._exclude)
                else:
                    self.widgets_values.update(Lay.creat_lay(
                        _root=self.frm_row, celulas=self.cards[card], type_wid=self.type_of, data=self.data,
                        font=('arial', 12), _exclude=self._exclude))
            else:
                self.widgets_values.update(Lay.creat_lay(
                    self.frm_row, self.cards[card], self.type_of, 
                    font=('arial', 12), data=_data, subwidget=self.subwidget, _exclude=self._exclude))
                #self.subwidget.pack()

            self.frm_row.pack(expand=1, fill='both')
        self.table_frame.pack(expand=1, fill='both')
        

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

    def new_data(self) -> dict:
        return self.context


class MyDateFields:
    def __init__(self, current) -> None:
        self.current_date = current
        self.time_diference = timedelta(days=70)
        self.estimate_date = self.current_date + self.time_diference
    
    def __str__(self) -> str:
        return self.estimate_date.strftime('%d-%m-%y')


