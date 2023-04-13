from tkinter import *


class MenuSection:
    def __init__(self, master:Menu):
        self.menu = Menu(master, tearoff=0)

    def add_command(self, label:str, command:callable):
        self.menu.add_command(label=label, command=command)

class MainMenu:
    def __init__(self, master:Tk, names: dict):
        self.menubar = Menu(master)
        self.sections:dict[str: MenuSection] = dict()
        self.config_names = names

        for name in self.config_names.keys():
            menu_section = MenuSection(self.menubar)
            self.sections[name] = menu_section

            self.menubar.add_cascade(
                menu=menu_section.menu,
                label=name,
            )

            for sub_name in self.config_names[name].keys():
                menu_section.add_command(
                    label=sub_name, 
                    command=self.config_names[name][sub_name]
                )

        master.configure(menu=self.menubar)


if __name__ == '__main__':
    menu_names = {
            'File': {
                'Configuracoes': lambda: print('Voce clicou em Configuracoes'), 
                'Users': lambda: print('Voce clicou em Users')
            },
            'Edit': {
                'Copy': lambda: print('Voce clicou em Copy'), 
                'Past': lambda: print('Voce clicou em Past')
            },
        }
    _master = Tk()
    menu = MainMenu(master=_master, names=menu_names)
    _master.mainloop()
   
    