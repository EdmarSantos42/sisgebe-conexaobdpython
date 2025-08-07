# db_config.py

import mysql.connector
from mysql.connector import Error

def conectar():
    try:
        conexao = mysql.connector.connect(
            host='localhost:3306',
            user='root',    # Troque se necessário
            password='eec123456@#$',        # Troque se necessário
            database='sgb'  # Nome do seu banco
        )
        if conexao.is_connected():
            print("Conexão bem-sucedida com o banco de dados!")
            return conexao
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None