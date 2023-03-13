from tkinter import Frame, Button
from mainLayout import Layout as Lay
from manage import ViewCard


class TableFrame:
    def __init__(
            self,
            _root: Frame, 
            _cards:dict,
            _data:dict=None) -> None:
        
        self.table_frame = Frame(_root)
        self.cards = _cards
            
        if _data:
            self._data_table = _data
        else:
            self._data_table = None
        
        for card in self.cards.keys():
            row = Frame(self.table_frame)
            if card != 'celNomesL4':
                self.build_layout(row, card, _data=self._data_table)
            else:
                frm_btt = Frame(row)
                btt_add = Button(frm_btt, text='Adicionar')
                btt_print = Button(frm_btt, text='Imprimir', command=lambda: self.print_pdf())
                btt_add.pack(side='left')
                btt_print.pack(side='right')
                self.build_layout(row, card, _subwidget=frm_btt,  _data=self._data_table)
            
            row.pack(expand=1, fill='both')
        self.table_frame.pack()

    def build_layout(self,_master, _card, _subwidget=None, _data=None):
        build = Lay.creat_lay(
            _master, self.cards[_card], 'label', font=('arial', 8), subwidget=_subwidget, data=_data
        )
        return build
    
    def request_data(self, _table):
        my_table = _table
        data_table: dict = dict(zip(
                self._handler.query_request_columns(my_table), 
                self._handler.request_data(my_table)[0]
            )
        )
        return  data_table


if __name__ == "__main__":
    from tkinter import Tk, Frame

    cards = ViewCard.layers
    window = Tk()
    frame = Frame(window)
    frame.pack()
    view = TableFrame(_root=frame, _cards=cards)
    window.mainloop()