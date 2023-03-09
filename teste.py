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
    table_name = f"{data.get('nome da rota')}{data.get('data da rota')}"
    print(table_name)
    try:
        cursor.execute(f"CREATE TABLE {table_name} {tuple(data.keys())}")
        cursor.execute(f"INSERT INTO {table_name} VALUES{tuple(data.values())}")
        conn.commit()
    except Error as erro:
        print(erro)
        cursor.execute(f"INSERT INTO {table_name} VALUES{tuple(data.values())}")
        conn.commit()


def dict_dados():
    for city in cityNames:
        temp_data = {
            'nome da rota': f'{city}',
            'data da rota': f'{randint(1, 31)}_{randint(1, 12)}_2023',
            'nome do vendedor': f"{choice(vendNames)}",
            'data para retorno': f'{randint(1, 31)}_{randint(1, 12)}_2023',
            'saldo cobrado': f'{randint(5500, 12000)}',
            'repasse cobrado': f'{randint(300, 1200)}',
            'total cobrado': '0',
            'repasse novo': f'{randint(800, 1500)}',
            'repasse total': '0',
            'fichas novas': f'{randint(34, 44)}',
            'fichas em branco': f'{randint(0, 6)}',
            'fichas repasse': f'{randint(2, 12)}',
            'venda anterior': f'{randint(28000, 36000)}',
            'devolucao de rua': f'{randint(8769, 12540)}',
            'total vendido': '0',
            'compra deposito': f'{randint(29440, 32400)}',
            'entrega deposito': '0',
            'venda nova': f'{randint(18890, 36783)}',
            'brindes': f'{randint(112, 323)}',
            'vl fichas branco': f'{randint(0, 1000)}',
            'despesa rota': f'{randint(600, 1000)}',
            'despesa extra': f'{randint(0, 1000)}'}

        ger_banco(temp_data)


if __name__ == '__main__':
    dict_dados()
