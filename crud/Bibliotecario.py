# crud_bibliotecario.py
from db_config import conectar
from hashlib import sha256

def hash_senha(s): return sha256(s.encode('utf-8')).hexdigest()

def criar_bibliotecario(nome, email, senha, status='ativo'):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Bibliotecario (nome,email,senha,status) VALUES (%s,%s,%s,%s)",
                       (nome, email, hash_senha(senha), status))
        conn.commit()
        return {"status":"sucesso","mensagem":"Bibliotecário criado.","id":cursor.lastrowid}
    except Exception as e:
        return {"status":"erro","mensagem":str(e)}
    finally:
        try: conn.close()
        except: pass

def listar_bibliotecarios():
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id,nome,email,status FROM Bibliotecario")
        return cursor.fetchall()
    except Exception as e:
        return {"status":"erro","mensagem":str(e)}
    finally:
        try: conn.close()
        except: pass

def atualizar_bibliotecario(id_b, nome=None, email=None, senha=None, status=None):
    try:
        conn = conectar()
        cursor = conn.cursor()
        campos=[]; vals=[]
        if nome: campos.append("nome=%s"); vals.append(nome)
        if email: campos.append("email=%s"); vals.append(email)
        if senha: campos.append("senha=%s"); vals.append(hash_senha(senha))
        if status: campos.append("status=%s"); vals.append(status)
        if not campos: return {"status":"aviso","mensagem":"Nada para atualizar."}
        vals.append(id_b)
        cursor.execute("UPDATE Bibliotecario SET " + ", ".join(campos) + " WHERE id=%s", tuple(vals))
        conn.commit()
        if cursor.rowcount==0: return {"status":"aviso","mensagem":"Bibliotecário não encontrado."}
        return {"status":"sucesso","mensagem":"Bibliotecário atualizado."}
    except Exception as e:
        return {"status":"erro","mensagem":str(e)}
    finally:
        try: conn.close()
        except: pass

def deletar_bibliotecario(id_b):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Bibliotecario WHERE id=%s", (id_b,))
        conn.commit()
        if cursor.rowcount==0: return {"status":"aviso","mensagem":"Bibliotecário não encontrado."}
        return {"status":"sucesso","mensagem":"Bibliotecário excluído."}
    except Exception as e:
        return {"status":"erro","mensagem":str(e)}
    finally:
        try: conn.close()
        except: pass
