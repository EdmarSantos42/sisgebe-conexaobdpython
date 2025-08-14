# crud_reserva.py
from db_config import conectar
from datetime import date

def criar_reserva(aluno_id, livro_id, data_reserva=None):
    try:
        conn=conectar(); cursor=conn.cursor()
        data_reserva = data_reserva or date.today().isoformat()
        cursor.execute("INSERT INTO Reserva (aluno_id, livro_id, data_reserva, status) VALUES (%s,%s,%s,%s)",
                       (aluno_id, livro_id, data_reserva, 'ativa'))
        conn.commit()
        return {"status":"sucesso","mensagem":"Reserva criada.","id":cursor.lastrowid}
    except Exception as e:
        return {"status":"erro","mensagem":str(e)}
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception as e:
                print(f"Erro ao fechar conexão: {e}")

def listar_reservas(so_ativas=False):
    try:
        conn=conectar(); cursor=conn.cursor(dictionary=True)
        if so_ativas:
            cursor.execute("SELECT * FROM Reserva WHERE status='ativa'")
        else:
            cursor.execute("SELECT * FROM Reserva")
        return cursor.fetchall()
    except Exception as e:
        return {"status":"erro","mensagem":str(e)}
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception as e:
                print(f"Erro ao fechar conexão: {e}")

def atualizar_reserva(id_reserva, status):
    try:
        conn=conectar(); cursor=conn.cursor()
        cursor.execute("UPDATE Reserva SET status=%s WHERE id=%s", (status, id_reserva))
        conn.commit()
        if cursor.rowcount==0: return {"status":"aviso","mensagem":"Reserva não encontrada."}
        return {"status":"sucesso","mensagem":"Reserva atualizada."}
    except Exception as e:
        return {"status":"erro","mensagem":str(e)}
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception as e:
                print(f"Erro ao fechar conexão: {e}")

def deletar_reserva(id_reserva):
    try:
        conn=conectar(); cursor=conn.cursor()
        cursor.execute("DELETE FROM Reserva WHERE id=%s", (id_reserva,))
        conn.commit()
        if cursor.rowcount==0: return {"status":"aviso","mensagem":"Reserva não encontrada."}
        return {"status":"sucesso","mensagem":"Reserva excluída."}
    except Exception as e:
        return {"status":"erro","mensagem":str(e)}
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception as e:
                print(f"Erro ao fechar conexão: {e}")
