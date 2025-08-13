# crud_emprestimo.py
from db_config import conectar
from datetime import date

def criar_emprestimo(aluno_id, livro_id, data_emprestimo=None, data_devolucao_prevista=None):
    try:
        conn = conectar()
        cursor = conn.cursor()
        # checar disponibilidade
        cursor.execute("SELECT quantidade FROM Livro WHERE id=%s", (livro_id,))
        row = cursor.fetchone()
        if not row:
            return {"status":"aviso","mensagem":"Livro não encontrado."}
        quantidade = row[0]
        if quantidade <= 0:
            return {"status":"aviso","mensagem":"Livro indisponível."}
        data_emprestimo = data_emprestimo or date.today().isoformat()
        cursor.execute("INSERT INTO Emprestimo (aluno_id, livro_id, data_emprestimo, data_devolucao_prevista) VALUES (%s,%s,%s,%s)",
                       (aluno_id, livro_id, data_emprestimo, data_devolucao_prevista))
        # decrementa quantidade
        cursor.execute("UPDATE Livro SET quantidade = quantidade - 1 WHERE id=%s", (livro_id,))
        conn.commit()
        return {"status":"sucesso","mensagem":"Empréstimo registrado.","id":cursor.lastrowid}
    except Exception as e:
        return {"status":"erro","mensagem":str(e)}
    finally:
        try: conn.close()
        except: pass

def listar_emprestimos(so_abertos=False):
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        q = """
            SELECT e.id, e.aluno_id, e.livro_id, e.data_emprestimo, e.data_devolucao_prevista, e.data_devolucao_real, e.multa,
                   a.nome as nome_aluno, l.titulo as titulo_livro
            FROM Emprestimo e
            LEFT JOIN Aluno a ON e.aluno_id = a.id
            LEFT JOIN Livro l ON e.livro_id = l.id
        """
        if so_abertos:
            q += " WHERE e.data_devolucao_real IS NULL"
            cursor.execute(q)
        else:
            cursor.execute(q)
        return cursor.fetchall()
    except Exception as e:
        return {"status":"erro","mensagem":str(e)}
    finally:
        try: conn.close()
        except: pass

def devolver_emprestimo(id_emprestimo, data_devolucao_real=None):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT livro_id, data_devolucao_real FROM Emprestimo WHERE id=%s", (id_emprestimo,))
        row = cursor.fetchone()
        if not row:
            return {"status":"aviso","mensagem":"Empréstimo não encontrado."}
        livro_id, devol_real = row[0], row[1]
        if devol_real is not None:
            return {"status":"aviso","mensagem":"Empréstimo já devolvido."}
        data_devolucao_real = data_devolucao_real or date.today().isoformat()
        cursor.execute("UPDATE Emprestimo SET data_devolucao_real=%s WHERE id=%s", (data_devolucao_real, id_emprestimo))
        cursor.execute("UPDATE Livro SET quantidade = quantidade + 1 WHERE id=%s", (livro_id,))
        conn.commit()
        return {"status":"sucesso","mensagem":"Devolução registrada."}
    except Exception as e:
        return {"status":"erro","mensagem":str(e)}
    finally:
        try: conn.close()
        except: pass
