# crud_sugestao.py
from db_config import conectar
from datetime import date

def criar_sugestao(titulo, autor, categoria, justificativa, data_sugestao=None, aluno_id=None, professor_id=None):
    try:
        conn=conectar(); cursor=conn.cursor()
        data_sugestao = data_sugestao or date.today().isoformat()
        cursor.execute(
            "INSERT INTO Sugestao (titulo, autor, categoria, justificativa, data_sugestao, aluno_id, professor_id) VALUES (%s,%s,%s,%s,%s,%s,%s)",
            (titulo, autor, categoria, justificativa, data_sugestao, aluno_id, professor_id)
        )
        conn.commit()
        return {"status":"sucesso","mensagem":"Sugestão registrada.","id":cursor.lastrowid}
    except Exception as e:
        return {"status":"erro","mensagem":str(e)}
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception as e:
                print(f"Erro ao fechar conexão: {e}")

def listar_sugestoes():
    try:
        conn=conectar(); cursor=conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Sugestao")
        return cursor.fetchall()
    except Exception as e:
        return {"status":"erro","mensagem":str(e)}
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception as e:
                print(f"Erro ao fechar conexão: {e}")
