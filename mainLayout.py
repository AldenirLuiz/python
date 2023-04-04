from tkinter import Label, Entry, Frame, Widget


# ESTA CLASSE E RESPONSAVEL POR DISTRIBUIR O LAYOUT DINAMICAMENTE
class Layout:
    dictEntryWidget = dict()

    # define o tipo de widget para os dados como do tipo entrada
    @staticmethod
    def ret_entry(nome: str, pai: Widget):
        widget = Entry(  # configuracoes do Entry
                pai, width=16, relief='groove', name=nome)
        widget.grid(  # posicao de alocamento do widget na grade
                row=1, column=1, padx=2, pady=2, ipadx=2, ipady=2)
        return widget

    # define o tipo de widget para os dados como do tipo texto
    @staticmethod
    def ret_label(nome: str, pai: Widget, vtext: str, _font=None):
        if _font:
            font = _font
        else: font = ("arial", 12)
        widget = Label(  # configuracoes do Label
                pai, font=font, text=vtext, width=14,
                relief='flat', name=nome)
        widget.grid(  # posicao de alocamento na grade
                row=1, column=1, padx=2, pady=2, ipadx=2, ipady=2)
        return widget

    # cria um widget opcional (usado para preencher o espaco reservado)
    @staticmethod
    def sub_widget(sb_widget: Widget):
        sb_widget.pack(  # alocando o subwidget na grade
                side='right', expand=1, fill='both',
                padx=2, pady=2, ipadx=2, ipady=2)

    # cria o card a receber os widgets
    @staticmethod
    def create_card(pai: Widget, desc: str):
        # container de disposicao da grade frm0
        label = Label(pai, text=desc.upper(), relief='groove')
        label.pack(expand=1, fill='x')

    # cria uma tarja de descricao acima do card quando solicitado
    @staticmethod
    def desc_widget(pai: Widget, descricao: str):
        label_cobranca = Label(pai, text=descricao.upper(), anchor='center')
        label_cobranca.pack()

    # cria o texto a ser exibido ao lado do widget de dados
    @staticmethod
    def ret_static_var(pai: Widget, text_var: str, _font=None):
        if _font:
            font = _font
        else: font = ("arial", 12)
        texto_statico = Label(  # configuracoes do Label
                pai, text=text_var, font=font, width=20, relief='flat', anchor='ne')
        texto_statico.grid(  # posicao de alocamento do widget na grade
                row=1, column=0, padx=2, pady=2, ipadx=2, ipady=2)

    @staticmethod
    def creat_lay(
        pai,
        celulas: dict,
        type_wid: str,
        desc: str = None,
        subwidget=None,
        data: dict = None,
        font=None,
        default=None) -> dict:

        data_frames: dict = data
            
        #  percorre as celulas presentes no pacote
        for desc, celula in celulas.items():
            frm0 = Frame(pai, relief='groove', bd=2)
            Layout.create_card(frm0, desc)
            # percorre os widgets presentes no pacote
            for widget in celula:
                # removendo caracteres desnecessarios
                nome = str(widget)
                if data_frames:
                    data_names = data_frames.get(nome)
                else:
                    data_names = ""
                frm1 = Frame(frm0, relief='flat')  # criando container da grade
                Layout.ret_static_var(frm1, str(widget).upper().replace('_', ' '), _font=font)
                # filtro de tipo de widget para Entry
                if type_wid == 'entry':
                    Layout.dictEntryWidget[nome] = Layout.ret_entry(nome=nome, pai=frm1)
                    if default:
                        if data_frames.get(nome):
                            Layout.dictEntryWidget[f'{nome}'].insert(0, data_frames.get(nome))
                else:  # filtro de tipo de widget para Label
                    Layout.dictEntryWidget[f'{nome}'] = Layout.ret_label(nome=nome, pai=frm1, vtext=data_names, _font=font)
                frm1.pack(anchor='w', expand=1, fill='both')  # alocando do container da grade
            if subwidget:  # aqui sera alocado um subwidget caso for solicitado.
                Layout.sub_widget(subwidget)
            frm0.pack(side='left', expand=1, fill='both', padx=4, pady=4, ipadx=2, ipady=2)
        # retorna os widgets configurados e enpacotados para uso
        return Layout.dictEntryWidget
    
    