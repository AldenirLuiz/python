from tkinter import *
from tkinter import ttk
import dataHandler

class MainView:
    db = dataHandler.HandlerDB(_database='users')
    list_type_users = ['Usuario', 'Administrador', 'Vendedor']
    list_header = ['Nome', 'Telefone', 'Email', 'Cargo']
    descritive_font = ('arial', 22)
    secondary_font = ('arial', 14)
    other_font = ('arial', 12)
    message_user = """
        This is a tool for manage and add Users, dont use for add products!
        and note: the type of user field atempt to add user type and this afect 
        permission of user on the system
    """

    def __init__(self, master:Toplevel):
        master.geometry('900x660')
        self.top_level_frm_00 = Frame(master)
        self.top_level_frm_00.pack(
            expand=1, fill='both', padx=8, pady=8, ipadx=8, ipady=8
        )
        # create layout model for main view 
        
        self.frame_superior_esquerdo = dict()
        self.frame_superior_Direito = dict()
        self.coluna_esquerda = dict()
        self.coluna_direita = dict()
        self.imagem_prod = PhotoImage(file='pessoa.png')

        self.containers_linhas_primarias = {
            'linha_primaria_00' : 
                Frame(
                    self.top_level_frm_00,
                ), # Linha0 primaria
            'linha_primaria_01' : 
                Frame(
                    self.top_level_frm_00
                ), # Linha0 primaria
        }
        self.containers_colunas_primarias = {
            'linha00_coluna00' : # frame de descricoes do produto
                Frame(
                    self.containers_linhas_primarias['linha_primaria_00'],
                    relief="ridge", bd=2
                ),
            'linha01_coluna00': # frame da imagem do produto
                Frame(
                    self.containers_linhas_primarias['linha_primaria_01'],
                    width=200, height=200, relief="ridge", bd=2
                ),
            'linha00_coluna01': 
                Frame( 
                    self.containers_linhas_primarias['linha_primaria_00'], 
                    relief="ridge", bd=2
                ),
            'linha01_coluna01': 
                Frame(
                    self.containers_linhas_primarias['linha_primaria_01'], 
                    relief="ridge", bd=2
                ),
        }
        self.containers_linhas_secundarias = {
            'linha01_coluna01_linha02' : # Frame selecao rota
                Frame( # Lina secundaria bottom
                    self.containers_colunas_primarias['linha01_coluna01']
                ),
            
        }
        self.frame_superior_esquerdo = { 
            'label_p_desc00' : 
                Label( # Label de descricao da grade
                    self.containers_colunas_primarias['linha00_coluna00'], 
                    text='Usuarios', relief="ridge",  font=self.descritive_font,
                ),
            
            'label_img': 
                Label(
                    self.containers_colunas_primarias['linha01_coluna00'], 
                    image=self.imagem_prod, width=200, height=200
                ),
            'text_box': 
                ttk.Treeview(
                        self.containers_linhas_secundarias['linha01_coluna01_linha02'],
                        selectmode='extended', columns=self.list_header, show='headings',
                        height=30
                    )
        }

        # Frame superior Direito
        self.frame_superior_Direito = {
            'label_desc': 
                Label(
                    self.containers_colunas_primarias['linha00_coluna01'], 
                    text='Cadastrar Usuários', anchor='n', 
                    font=self.descritive_font, relief='ridge',                 ),
            'user_name' : 
                Label(
                    self.containers_colunas_primarias['linha00_coluna01'], 
                    text='Nome do Usuario', font=self.other_font
                ),
            'user_name_entry' : 
                Entry( # Entry selecao vendedor
                    self.containers_colunas_primarias['linha00_coluna01'],
                    width=80,
                ),
            'fone_number' : 
                Label(
                    self.containers_colunas_primarias['linha00_coluna01'], 
                    text='Numero Telefone', font=self.other_font
                ),
            'fone_number_entry' : 
                Entry( # Entry selecao vendedor
                    self.containers_colunas_primarias['linha00_coluna01'],
                    width=80,
                ),
            'email' : 
                Label(
                    self.containers_colunas_primarias['linha00_coluna01'], 
                    text='E-mail', font=self.other_font
                ),
            'email_entry' : 
                Entry( # Entry selecao vendedor
                    self.containers_colunas_primarias['linha00_coluna01'],
                    width=80,
                ),
            
            'user_type' : 
                Label( 
                    self.containers_colunas_primarias['linha00_coluna01'], 
                    text='Tipo de Usuario', font=self.other_font,
                ),
            'user_type' : 
                ttk.Combobox( # Entry selecao rota
                    self.containers_colunas_primarias['linha00_coluna01'],
                    values=self.list_type_users,
                    width=50,
                ),
        }

        # Frame buttons
        self.frame_buttons = {
            'btt_data_collector': 
                Button(
                    self.containers_colunas_primarias['linha00_coluna01'],
                    text='Adicionar', bg='green', border=2, relief='ridge',
                    command=lambda: self.add_data_users()
                ),
            'btt_data_clear': 
                Button(
                    self.containers_colunas_primarias['linha00_coluna01'],
                    text='Limpar', bg='orange', command=lambda: self.clear_fields()
                ),
        }
        
        # Frame inferior coluna a direita
        self.frame_inferior_Direito = {
            'label_observacoes_01':Label(
                    self.containers_colunas_primarias['linha00_coluna00'],
                    text='Please Verify the entrys for correct data.'
            ),
            'opt_label' : 
                Label( # Label selecao rota
                    self.containers_colunas_primarias['linha00_coluna00'], 
                    text=self.message_user, 
                    font=self.other_font
                ),
            'btt_exit': 
                Button(
                    self.containers_colunas_primarias['linha00_coluna00'],
                    text='<- Sair', border=2, relief='ridge', command=lambda x=0: exit(x)
                ),
        }
        count = 0
        for head in self.list_header:
            self.frame_superior_esquerdo['text_box'].heading(count, text=head, anchor='n')
            self.frame_superior_esquerdo['text_box'].column(count, width=120, anchor='n')
            count+=1

        self.pack_Widgets(
            widgets=[
                self.containers_linhas_primarias, 
                self.containers_linhas_secundarias,
                self.frame_superior_esquerdo,
                self.frame_superior_Direito,],
            expand=1)
        self.pack_Widgets(
            widgets=[
                self.containers_colunas_primarias,
                self.frame_buttons,],
            direction='left',
            expand=1)
        self.pack_Widgets(
            widgets=[{
                    'label_observacoes_01': 
                        self.frame_inferior_Direito['label_observacoes_01'],
                    'label_observacoes_02': 
                        self.frame_inferior_Direito['opt_label'],
                    'btt_exit': 
                        self.frame_inferior_Direito['btt_exit']}],
            direction='top',
            expand=1)
        self.data_view_update()
        # self.frm_view.mainloop()

        
    def data_view_update(self):
        for iten in self.frame_superior_esquerdo['text_box'].selection():
            print(iten)
            self.frame_superior_esquerdo['text_box'].delete(iten)

        for value in self.db.request_data('users'):
            self.frame_superior_esquerdo['text_box'].insert('', 'end', values=value)

    def pack_Widgets(self, **kwargs):
        _widgets: list[dict[str: Widget]] = kwargs.get('widgets')
        _direction: str = kwargs.get('direction')
        _expand:int = kwargs.get('expand')
        _fill = 'both'
        
        for _package in _widgets:
            for _widget in _package.keys():
                if isinstance(
                    _package[_widget], ttk.Combobox
                ) or isinstance(
                    _package[_widget], Entry):
                    _expand = None
                    _fill = None
                elif isinstance(
                    _package[_widget], Button):
                    _expand = 1
                    _fill = 'x'
                elif isinstance(
                    _package[_widget], Label):
                    _expand = 0
                    _fill = 'x'

                _package[_widget].pack(
                    side=_direction, expand=_expand, fill=_fill,
                    pady=4, padx=4,
                    ipady=4, ipadx=4
                )

    def add_data_users(self):
        _value = dict()
        for _entry in self.frame_superior_Direito.keys():
            if isinstance(
                self.frame_superior_Direito[_entry], Entry) or isinstance(
                self.frame_superior_Direito[_entry], ttk.Combobox):
                _value.update(
                    {_entry: self.frame_superior_Direito[_entry].get()})
        self.db.query_add(_value, 'users')
        _value = dict()
        self.data_view_update()

    def clear_fields(self):
        for _entry in self.frame_superior_Direito.keys():
            if isinstance(
                self.frame_superior_Direito[_entry], Entry) or isinstance(
                self.frame_superior_Direito[_entry], ttk.Combobox):
                self.frame_superior_Direito[_entry].delete(0, END)



if __name__ == "__main__":
    window = Tk()
    MainView(window)
    window.mainloop()
    
