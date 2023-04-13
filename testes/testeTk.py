import tkinter as tk

janela = tk.Tk()
janela.title("Cadastro de Clientes")

label_names = ["nome_completo:", "idade:", "e-mail:", "telefone:"]
widgets = dict()

for text in label_names:
    frm_line = tk.Frame(janela, bd=1, relief='ridge')
    widgets.update(
        {   
            f"label_{text}": tk.Label(
                frm_line, text=text.title().replace('_', ' ')),
            f"entry_{text}": tk.Entry(frm_line)
        }
    )
    frm_line.pack(expand=1, fill='x', pady=4, padx=4, ipady=4, ipadx=4)

for widget in widgets.values():
    print(widget)
    widget.pack(side='left', expan=1, anchor='e'),


def salvar_cliente():
    nome: str = widgets['entry_nome_completo:'].get()
    idade: str = widgets['entry_idade:'].get()
    email: str = widgets['entry_e-mail:'].get()
    telefone: str = widgets['entry_telefone:'].get()
    print(nome, idade, email, telefone)
    with open("clientes.txt", "a") as f:
        f.write(
            f"{nome.capitalize().replace('_', ' ')}, {idade}, {email.replace('_', '-')}, {telefone}\n")


def clear_fields():
    for widget in widgets.values():
        if isinstance(widget, tk.Entry):
            widget.delete(0, tk.END)


btn_salvar = tk.Button(janela, text="Salvar", command=salvar_cliente)
btn_salvar.pack(side='left', expand=1, fill='x')
btn_clear = tk.Button(janela, text="Limpar", command=clear_fields)
btn_clear.pack(side='right', expand=1, fill='x')

janela.mainloop()