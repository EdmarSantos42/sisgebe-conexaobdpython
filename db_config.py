# db_config.py

import mysql.connector
from mysql.connector import Error

def conectar():
    try:
        conexao = mysql.connector.connect(
            host='127.0.0.1',
            port=3306,
            user='root',    # Troque se necessário
            password='',        # Troque se necessário
            database='SGB'  # Nome do seu banco
        )
        if conexao.is_connected():
            print("Conexão bem-sucedida com o banco de dados!")
            return conexao
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None