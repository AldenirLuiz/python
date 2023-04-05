import sqlite3 as db
from sqlite3 import OperationalError, Connection, Cursor
from SysWay import MyWayApp as Way
import os


class HandlerDB:
    __ROOT_DIR__: list = Way(path='dataBase').walk_sys_file()
    # print(__ROOT_DIR__)
    __DATABASE_DATA__: str = 'dadosCobranca.db'
    __DATABASE_USERS__: str = 'userData.db'
    _query_table_exists: str = "SELECT name FROM sqlite_master WHERE type='table';"
    _query_table_check: str = "SELECT name FROM sqlite_master WHERE type='table' AND name='{}';"
    _temp_query_columns: str = "PRAGMA table_info({})"
    _request_data_from: str = "SELECT * FROM '{}'"
    _request_from: str = "SELECT * FROM '{}' WHERE nome_do_vendedor=?;"
    _request_from_vendor:str = "SELECT * FROM {} WHERE nome_do_vendedor=?;"
    _request_data_with:str = "SELECT * FROM '{}' WHERE data_da_rota LIKE ? AND data_para_retorno=?"

    _error_code_table: str = "Tabela Inexistente"

    def __init__(self, _database:str='users') -> None:
        
        if _database == 'users':
            self.database = self.__DATABASE_USERS__
        else:
            self.database = self.__DATABASE_DATA__
        try:
            way:str = Way(file=self.database).walk_sys_file()
            print(f"databaseType: {_database} | path: {way}")
            self.banco: Connection = db.connect(way)
            self.cursor: Cursor = self.banco.cursor()
            
        except OperationalError as _erro:
            message: str = f"""Problema ao Conectar com o Banco de dados.\n
                ->Possivel erro de permissao de leitura/gravacao, 
                Contate o administrador do Sistema.
                ERRO:{_erro}"""
            print(message)
            self.ErrConnectDB(message)
            

    def query_add(self, _data: dict[str, str], _table:str=None, contiguos:bool=False) -> str:
        if not _table:
            _table_: str = f"{_data['nome_da_rota']}"
        else:
            _table_ = _table
        
        if not self.verify_tables(_table=_table_):
            temp_table_create: str = f"CREATE TABLE {_table_} {tuple(_data.keys())};"
            self.cursor.execute(temp_table_create)
            self.banco.commit()
        temp_data_adict: str = f"INSERT INTO {_table_} VALUES{tuple(_data.values())};"

        self.cursor.execute(temp_data_adict)
        self.banco.commit()
        return "All data are aded"

    def query_request_tables(self) -> list:

        try:
            _tables = self.cursor.execute(self._query_table_exists).fetchall()
            return [x[0] for x in _tables]
        except db.Error as _erro:
            raise _erro

    def query_request_columns(self, _table: str) -> list:

        if self.verify_tables(_table):
            columns: list = [
                x[1] for x in self.cursor.execute(
                    self._temp_query_columns.format(_table)
                ).fetchall()
            ]
            return columns
        else:
            return [self._error_code_table, _table]

    def request_data(self, _table):
        if self.verify_tables(_table):
            _data = self.cursor.execute(self._request_data_from.format(_table)).fetchall()
            return _data
        else:
            return ['Table not exists', _table]
        
    def request_data_from(self, *args):
        _data = self.cursor.execute(self._request_from.format(*args)).fetchall()
        return _data
    
    def request_data_from_column(self, _column0, _column1, _table):
        _data = self.cursor.execute(
            self._request_data_with.format(_table), (_column0, _column1,)
        ).fetchall()
        return _data

    def request_from_vendor(self, vendor, table=None):
        data_request = dict()
        if table:
            _data = self.cursor.execute(self._request_from_vendor.format(table), (vendor,)).fetchall()
            if _data != []:
                temp_data = {table: _data}
                data_request.update(temp_data)
        else:
            for _table in self.query_request_tables():
                _data = self.cursor.execute(self._request_from_vendor.format(_table), (vendor,)).fetchall()
                if _data != []:
                    temp_data = {_table: _data}
                    data_request.update(temp_data)
        return data_request
        

    def verify_tables(self, _table: str) -> bool:
        _query_check = self.cursor.execute(self._query_table_check.format(_table)).fetchall()
        # print(f"query_check: {_query_check}")
        if _query_check != list():
            return True
        else:
            return False
        
    @staticmethod
    def format_table_names(_tables: list[str, str]):
        temp_names = list()
        for _table_name in _tables:
            temp_name = str()
            temp_date = str()
            for char in _table_name:
                if char.isalpha():
                    temp_name += char
                elif char.isalnum():
                    temp_date += char
                else:
                    temp_date += '/'
            temp_names.append(f"{temp_name} - {temp_date}")
        return temp_names

    class ErrConnectDB(Exception):
        pass

    def delete_data(self, _table, _data):
        pass


if __name__ == "__main__":
    hand_data = HandlerDB(_database='data')
    hand_users = HandlerDB(_database='users')

    def request_users():
        count = 0
        for user in hand_users.request_data('users'):
            print(user)
            hand_users.cursor.execute(f"DROP TABLE IF EXISTS users")
            count+=1

    def request_data_users():

        dictdata = dict()
        tables: list[str] = hand_users.query_request_tables()
        columns = hand_users.query_request_columns(tables[0])
        data = hand_users.request_data(tables[0])
     
        for _data in data:
            tempdata = dict(zip(columns, _data))
            dictdata.update({f"{tempdata['user_name_entry']}": tempdata})

        print(dictdata)

    print(hand_data.query_request_columns('Santa_Luzia'))