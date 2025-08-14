# crud_relatorio.py
from db_config import conectar
from datetime import date

def criar_relatorio(tipo, periodo_inicio, periodo_fim, gerado_por_bibliotecario=None, gerado_por_diretor=None, gerado_por_supervisor=None):
    try:
        conn=conectar(); cursor=conn.cursor()
        cursor.execute(
            "INSERT INTO Relatorio (tipo, periodo_inicio, periodo_fim, gerado_por_bibliotecario, gerado_por_diretor, gerado_por_supervisor) VALUES (%s,%s,%s,%s,%s,%s)",
            (tipo, periodo_inicio, periodo_fim, gerado_por_bibliotecario, gerado_por_diretor, gerado_por_supervisor)
        )
        conn.commit()
        return {"status":"sucesso","mensagem":"Relatório criado.","id":cursor.lastrowid}
    except Exception as e:
        return {"status":"erro","mensagem":str(e)}
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception as e:
                print(f"Erro ao fechar conexão: {e}")

def listar_relatorios():
    try:
        conn=conectar(); cursor=conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Relatorio")
        return cursor.fetchall()
    except Exception as e:
        return {"status":"erro","mensagem":str(e)}
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception as e:
                print(f"Erro ao fechar conexão: {e}")
