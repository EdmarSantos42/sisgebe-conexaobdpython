# crud_historicoleitura.py
from db_config import conectar
from datetime import date

def criar_historico(aluno_id, livro_id, data_inicio=None, data_fim=None):
    try:
        conn=conectar(); cursor=conn.cursor()
        data_inicio = data_inicio or date.today().isoformat()
        cursor.execute("INSERT INTO HistoricoLeitura (aluno_id, livro_id, data_inicio, data_fim) VALUES (%s,%s,%s,%s)",
                       (aluno_id, livro_id, data_inicio, data_fim))
        conn.commit()
        return {"status":"sucesso","mensagem":"Histórico criado.","id":cursor.lastrowid}
    except Exception as e:
        return {"status":"erro","mensagem":str(e)}
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception as e:
                print(f"Erro ao fechar conexão: {e}")

def listar_historico(aluno_id=None):
    try:
        conn=conectar(); cursor=conn.cursor(dictionary=True)
        if aluno_id:
            cursor.execute("SELECT * FROM HistoricoLeitura WHERE aluno_id=%s", (aluno_id,))
        else:
            cursor.execute("SELECT * FROM HistoricoLeitura")
        return cursor.fetchall()
    except Exception as e:
        return {"status":"erro","mensagem":str(e)}
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception as e:
                print(f"Erro ao fechar conexão: {e}")
