# -*- coding: utf-8 -*-
# Aldenir Luiz 17/02/2023
import os


class MyWayApp:
    """
Walk through the system directories to find paths or files
O módulo SysWay by Aldenir Luiz é um script Python tendo uma classe MyWayApp e um método walk_sys_file. 
Esse método usa a biblioteca os para caminhar pelos diretórios do sistema e encontrar arquivos ou caminhos.
O construtor da classe recebe três argumentos opcionais: um arquivo, um caminho e uma opção para retornar apenas caminhos ou arquivos.
O método walk_sys_file inicia o processo de caminhar pelos diretórios do sistema usando a função os.walk. 
Ele verifica se o arquivo especificado no construtor existe nos diretórios ou subdiretórios que está caminhando. 
Se o arquivo for encontrado e a opção for configurada para retornar apenas caminhos ele adicionará o caminho ao resultado. 
Caso contrário, ele retornará o caminho completo do arquivo.
Se o caminho especificado no construtor existir nos diretórios caminhados ele adicionará o caminho ao resultado.
Se nenhum arquivo ou caminho foi encontrado, ele retornará uma lista vazia.
    """
    __ROOT__:str = os.path.dirname(__file__)
    _library:str = 'library.zip'
    def __init__(self, file:str or bytes=None, path:str=None, onlyWay:bool=False, first:bool=True) -> None:
        self.path = path
        self.file = file
        self.option = onlyWay
        self.first = first
    
    def walk_sys_file(self) -> list or str:
        my_dirs = list()
        my_files = list()
        for dirs, subdirs, files in os.walk(self.__ROOT__):
            # print(f"dirnames: {dirs}\nsubdirs: {subdirs}\nfiles: {files}")

            if self.file and self.file in files:
                if not self.option:
                    if self.first:
                        return f"{dirs}/{self.file}".replace(self._library, '')
                    else:
                        my_files.append(f"{dirs}/{self.file}".replace(self._library, ''))
                else:
                   my_files.append(f"{dirs}/".replace(self._library, ''))
            elif f"/{self.path}" in dirs:
                if self.first:
                    return dirs
                else:
                    my_dirs.append(dirs)
        
        if self.file:
            return my_files
        else:
            return my_dirs
        
            

if __name__ == '__main__':
    app = MyWayApp(file='dadosCobranca.db')
    print(app.walk_sys_file())
    pass