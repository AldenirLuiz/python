from tkinter import Tk, Frame
from tkinter.ttk import Treeview, Style
from ctypes import Union

class MyTable:
    """
        Construct Personalized ttk.TreeView Object
        <author:>Aldenir Luiz 12/03/2023

        <root: required*>master to pack widget
        <columns: required*>columns names for dispay in top view
        <width: optional>define max width of widget
    """
    def __init__(self, _root: Tk, _columns: list, _width: int=100, font:tuple=('arial', 12)) -> None:
        self.font:tuple = font
        self.style: Style = Style()
        self.master: Tk = _root
        self.columns: Union[list:str] = _columns
        self.max_width: int = _width
        self.font_bold = (*self.font, 'bold')
        

        self.main_table = Treeview(
            master = self.master,
            selectmode = 'extended',
            columns=self.columns, 
            show='headings',
            ); self.build_view(),
            

    def build_view(self):
        self.style.configure("Treeview.Heading", font=self.font_bold)
        self.style.configure("Treeview", font=self.font)
        index_count = 0
        for column_name in self.columns:
            self.main_table.column(
                column_name, minwidth=50, width=self.max_width, anchor='n'
            )
            self.main_table.heading(
                index_count, text=column_name, anchor='n'
            )
            index_count+=1
        self.main_table.pack(expand=1, fill='both')
        return self.main_table


if __name__ == "__main__":
    tree_columns_names = ["Nome", "Idade", "Sexo", "Id"]
    tree_data = [
        ['Aldenir', '29', 'Masculino', '#3231'],
        ['Jeronimo', '41', 'Masculino', '#4561'],
        ['Francisco', '34', 'Masculino', '#7895']
    ]

    my_window = Tk()
    view = MyTable(my_window, tree_columns_names, 120).build_view()

    for (_nome, _idade,_sexo, _id) in tree_data:
        view.insert('', 'end', values=(_nome, _idade, _sexo, _id))

    my_window.mainloop()
