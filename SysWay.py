import os
import sys


class MyWayApp:
    """
        Walk on the system directories to find path`s or files
    """
    __ROOT__:str = os.path.dirname(__file__)
    def __init__(self, file:str or bytes=None, path:str=None, onlyWay:bool=False) -> None:
        self.path = path
        self.file = file
        self.option = onlyWay
    
    def walk_sys_file(self):
        for dirs, subdirs, files in os.walk(self.__ROOT__):
            print(f"dirnames: {dirs}\nsubdirs: {subdirs}\nfiles: {files}")
            if self.file and self.file in files:
                if not self.option:
                    return f"{dirs}/{self.file}".replace('library.zip', '')
                else:
                    return f"{dirs}/".replace('library.zip', '')
            elif self.path in dirs:
                return dirs



if __name__ == '__main__':
    app = MyWayApp(file='cellNames.json', onlyWay=True)
    print(app.walk_sys_file())
    pass