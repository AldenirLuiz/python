import sqlite3 as db
from sqlite3 import OperationalError, Connection, Cursor
import os


class HandlerDB:
    __ROOT_DIR__: str = os.path.abspath(os.path.dirname(__file__))
    __DATABASE__: str = 'dadosCobranca.db'

    _query_table_exists: str = "SELECT name FROM sqlite_master WHERE type='table';"
    _query_table_check: str = "SELECT name FROM sqlite_master WHERE type='table' AND name='{}';"
    _temp_query_columns: str = "PRAGMA table_info({})"
    _request_data_from: str = "SELECT * FROM '{}'"
    _error_code_table: str = "Tabela Inexistente"

    def __init__(self) -> None:
        try:
            self.banco: Connection = db.connect(
                f'{self.__ROOT_DIR__}/dataBase/{self.__DATABASE__}')
            self.cursor: Cursor = self.banco.cursor()
        except OperationalError as _erro:
            message: str = f"""Problema ao Conectar com o Banco de dados.\n
                ->Possivel erro de permissao de leitura/gravacao, 
                Contate o administrador do Sistema.
                ERRO:{_erro}"""
            print(message)
            self.ErrConnectDB(message)

    def query_add(self, _data: dict[str, str]) -> str:
        _table_: str = f"{_data['nome da rota']}{_data['data da rota']}"
        temp_table_create: str = f"CREATE TABLE {_table_} {tuple(_data.keys())};"
        temp_data_adict: str = f"INSERT INTO {_table_} VALUES{tuple(_data.values())};"

        if not self.verify_tables(_table=_table_):
            self.cursor.execute(temp_table_create)
            self.banco.commit()
            self.cursor.execute(temp_data_adict)
            self.banco.commit()
            return "All data are aded"
        else:
            return f"A tabela {_table_} ja existe no banco de dados!"

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
            # print(f"columns: {columns}")
            return columns
        else:
            return [self._error_code_table, _table]

    def request_data(self, _table):
        if self.verify_tables(_table):
            _data = self.cursor.execute(self._request_data_from.format(_table)).fetchall()
            return _data
        else:
            return ['Table not exists', _table]

    def verify_tables(self, _table: str) -> bool:
        _query_check = self.cursor.execute(self._query_table_check.format(_table)).fetchall()
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


if __name__ == "__main__":
    hand = HandlerDB()
    # print(hand.verify_tables('Itaporanga28_2_2023'))
    tables: list[str] = hand.query_request_tables()
    print(hand.format_table_names(tables))
    # print(tables)
    # print(hand.query_request_tables(_table=tables[0]))
    # print(hand.query_request_columns(tables[0]))
    # dictdata = dict(zip(hand.query_request_columns(tables[0]), hand.request_data(tables[0])[0]))
    # print(dictdata)
