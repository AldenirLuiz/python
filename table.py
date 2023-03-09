from tkinter import *
from mainLayout import Layout
from manage import ViewCard
from dataHandler import HandlerDB as Db


class MyTable(Toplevel):
    """
        Criar Uma vizualizacao para os dados com uma toplevel
        <:var text_superior>: texto primario no rodape da planilha
        <:var message>
    """
    text_superior: str = "Seu texto"
    message: str = 'Um texto de exemplo, Para adicionar a sua aplicacao'
    _handler = Db()
    _exclude_cards: list[str, str] = ["notebookNames"]
    dict_data = dict()

    def __init__(self, _table):
        super().__init__()
        self.cards = ViewCard().layers_
        self.container_0 = Frame(self)
        self.container_btt = Frame(self.container_0)
        self.layout_data(_table)

        self.label = Label(self.container_btt, text=f'{self.text_superior}\n{self.message}')
        self.label.pack(side='left', expand=True, fill='both')
        self.btt_exit = Button(self.container_btt, text='SAIR', command=lambda: self.destroy())
        self.btt_exit.pack(side='right', expand=True, fill='both')

        self.container_btt.pack(expand=True, fill='both')
        self.container_0.pack(expand=1, fill='both')

    def layout_data(self, _table):
        """Criando visualizacao dos dados armazenados na tabela passada como argumento
        <param> >_table<: tabela valida do banco de dados"""

        for card in self.cards:  # percorrendo os dados de layout arquivo cellNames.json
            frm = Frame(self.container_0)
            # filtrando nomes dos cards (adicione ou remova cards na variavel de classe _exclude_cards)
            if card not in self._exclude_cards:
                Layout.creat_lay(frm, self.cards[card], 'label', data=self.ret_query_data(_table))
            frm.pack(expand=1, fill='both')

    @classmethod
    def ret_query_data(cls, _table):
        _column = cls._handler.query_request_columns(_table)
        _data = cls._handler.request_data(_table)
        cls.dict_data = dict(zip(_column, _data[0]))
        return cls.dict_data
