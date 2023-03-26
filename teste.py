import sqlite3
from sqlite3 import Error
from random import randint, choice


banco = 'dataBase/dadosCobranca.db'
conn = sqlite3.connect(banco)
cursor = conn.cursor()


cityNames = ["Campina", "Patos", "Itaporanga", "Juazeirinho", "Brejo"]
vendNames = ["Jeronimo", "Corro", "Alex"]


def ger_banco(data: dict):
    print(data)
    table_name = f"{data.get('nome_da_rota')}"
    print(table_name)
    try:
        if not verify_tables(table_name):
            cursor.execute(f"CREATE TABLE {table_name} {tuple(data.keys())}")
        cursor.execute(f"INSERT INTO {table_name} VALUES{tuple(data.values())}")
        conn.commit()
    except Error as erro:
        print(erro)
        cursor.execute(f"INSERT INTO {table_name} VALUES{tuple(data.values())}")
        conn.commit()

def verify_tables(_table: str) -> bool:
        _query_check = cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{_table}';").fetchall()
        if _query_check != list():
            return True
        else:
            return False


def dict_dados():
    for city in cityNames:
        temp_data = {
            'nome_da_rota': f'{city}',
            'data_da_rota': f'{randint(1, 31)}_{randint(1, 12)}_2023',
            'nome_do_vendedor': f"{choice(vendNames)}",
            'data_para_retorno': f'{randint(1, 31)}_{randint(1, 12)}_2023',
            'saldo_cobrado': f'{randint(5500, 12000)}',
            'repasse_cobrado': f'{randint(300, 1200)}',
            'total_cobrado': '0',
            'repasse_novo': f'{randint(800, 1500)}',
            'repasse_total': '0',
            'fichas_novas': f'{randint(34, 44)}',
            'fichas_em_branco': f'{randint(0, 6)}',
            'fichas_repasse': f'{randint(2, 12)}',
            'total_de_fichas': f'{randint(38, 46)}',
            'venda_anterior': f'{randint(28000, 36000)}',
            'devolucao_de_rua': f'{randint(8769, 12540)}',
            'total_vendido': '0',
            'compra_deposito': f'{randint(29440, 32400)}',
            'entrega_deposito': '0',
            'venda_nova': f'{randint(18890, 36783)}',
            'brindes': f'{randint(112, 323)}',
            'vl_fichas_branco': f'{randint(0, 1000)}',
            'total_na_rua': '0',
            'despesa_rota': f'{randint(600, 1000)}',
            'despesa_extra': f'{randint(0, 1000)}'}

        ger_banco(temp_data)


if __name__ == '__main__':
    dict_dados()
