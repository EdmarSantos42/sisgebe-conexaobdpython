# crud_livro.py
from db_config import conectar

def criar_livro(titulo, autor, isbn=None, sinopse=None, capa=None, quantidade=1, categoria_id=None):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Livro (titulo, autor, isbn, sinopse, capa, quantidade, categoria_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (titulo, author_or_none(autor), isbn, sinopse, capa, quantidade, categoria_id)
        )
        conn.commit()
        return {"status":"sucesso","mensagem":"Livro criado com sucesso.","id":cursor.lastrowid}
    except Exception as e:
        return {"status":"erro","mensagem":str(e)}
    finally:
        try: conn.close()
        except: pass

def author_or_none(a):
    return a if a is not None else ""

def listar_livros():
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Livro")
        return cursor.fetchall()
    except Exception as e:
        return {"status":"erro","mensagem":str(e)}
    finally:
        try: conn.close()
        except: pass

def obter_livro(id_livro):
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Livro WHERE id=%s", (id_livro,))
        row = cursor.fetchone()
        if not row:
            return {"status":"aviso","mensagem":"Livro não encontrado."}
        return row
    except Exception as e:
        return {"status":"erro","mensagem":str(e)}
    finally:
        try: conn.close()
        except: pass

def atualizar_livro(id_livro, titulo, autor, isbn, sinopse, capa, quantidade, categoria_id):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Livro SET titulo=%s, autor=%s, isbn=%s, sinopse=%s, capa=%s, quantidade=%s, categoria_id=%s WHERE id=%s",
            (titulo, autor, isbn, sinopse, capa, quantidade, categoria_id, id_livro)
        )
        conn.commit()
        if cursor.rowcount==0:
            return {"status":"aviso","mensagem":"Nenhum livro encontrado para atualizar."}
        return {"status":"sucesso","mensagem":"Livro atualizado com sucesso."}
    except Exception as e:
        return {"status":"erro","mensagem":str(e)}
    finally:
        try: conn.close()
        except: pass

def deletar_livro(id_livro):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Livro WHERE id=%s", (id_livro,))
        conn.commit()
        if cursor.rowcount==0:
            return {"status":"aviso","mensagem":"Nenhum livro encontrado para deletar."}
        return {"status":"sucesso","mensagem":"Livro excluído com sucesso."}
    except Exception as e:
        return {"status":"erro","mensagem":str(e)}
    finally:
        try: conn.close()
        except: pass
