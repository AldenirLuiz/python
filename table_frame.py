from tkinter import Frame, Button, Toplevel
from mainLayout import Layout as Lay
from manage import ViewCard



class TableFrame:
    _cards = ViewCard().layers
    _exclude=[
        'total_cobrado',
        'total_vendido',
        'entrega_deposito']
    
    _labels:dict[str: str] = {
        'btt_adict': 'Adicionar Nova',
        'btt_print': 'Imprimir',
        'btt_save': 'Salvar Dados',
        'btt_clear': 'Limpar Campos',}

    _comands:dict = {
        'toplevel': lambda: TopLevelWidow(
            Toplevel(), _type='entry'),
        'testbutton': lambda: print("MyNameIsButtom"),}

    def __init__(self, _root: Frame, _data:dict=None, _type:str=None) -> None:
        
        self.root= _root
        self.table_frame = Frame(_root)
        self.type_of = _type
        self.cards = Process(self._exclude)

        if self.type_of == 'label':
            self.comand = self._comands['toplevel']
        else:
            self.comand = self._comands['testbutton']

        if _data:
            self._data_table = _data
        else:
            self._data_table = None
        MyLayout(self.root, self.comand, _data, _type=self.type_of, )
        

class Process:
    temp_cards: dict = ViewCard().layers
    def __init__(self, exclude) -> None:
        for cell in self.temp_cards.keys():
            for card in self.temp_cards[cell]:
                for value in self.temp_cards[cell][card]:
                    if value in exclude:
                        self.temp_cards[cell][card].remove(value)
    
    def __dict__(self) -> dict:
        return self.temp_cards


class RequestData:
    data_table: dict = dict()
    def __init__(self, _table) -> None:
        self.my_table = _table
        self.data_table: dict = dict(
            zip(
                self._handler.query_request_columns(self.my_table), 
                self._handler.request_data(self.my_table)[0]))
        
    def __dict__(self) -> dict:
        return  self.data_table
 

class MyLayout:
    _tipo = ['label', 'entry']
    def __init__(self, _root, _command, _data=None, _type='label') -> None:
        self.table_frame = Frame(_root)
        for card in ViewCard.layers:
            self.btt_row = Frame(_root)

            if card != 'celNomesL4':
                Lay.creat_lay(self.btt_row, ViewCard.layers[card], _type, data=_data)
            else:
                self.frm_btt = Frame(self.btt_row)
                MyButton(self.frm_btt, 'Cadastrar', _command)
                Lay.creat_lay(_root, ViewCard.layers[card], self._tipo[0], 
                    font=('arial', 12), data=_data, subwidget=self.frm_btt)
                self.frm_btt.pack()
            self.btt_row.pack(expand=1, fill='both')
        self.table_frame.pack()


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
    cards = ViewCard.layers
    window = Tk()
    window.tk_strictMotif(1)
    frame = Frame(window)
    frame.pack()
    view = TableFrame(_root=frame, _type='label')
    window.mainloop()