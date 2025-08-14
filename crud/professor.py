# crud_professor.py
from db_config import conectar
from hashlib import sha256

def hash_senha(s):
    return sha256(s.encode('utf-8')).hexdigest()

def criar_professor(nome, email, senha, disciplina=None, status='ativo'):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Professor (nome, email, senha, disciplina, status) VALUES (%s,%s,%s,%s,%s)",
                       (nome, email, hash_senha(senha), disciplina, status))
        conn.commit()
        return {"status":"sucesso","mensagem":"Professor criado.","id":cursor.lastrowid}
    except Exception as e:
        return {"status":"erro","mensagem":str(e)}
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception as e:
                print(f"Erro ao fechar conexão: {e}")

def listar_professores():
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, nome, email, disciplina, status FROM Professor")
        return cursor.fetchall()
    except Exception as e:
        return {"status":"erro","mensagem":str(e)}
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception as e:
                print(f"Erro ao fechar conexão: {e}")

def atualizar_professor(id_prof, nome=None, email=None, senha=None, disciplina=None, status=None):
    try:
        conn = conectar()
        cursor = conn.cursor()
        campos=[]; vals=[]
        if nome: campos.append("nome=%s"); vals.append(nome)
        if email: campos.append("email=%s"); vals.append(email)
        if senha: campos.append("senha=%s"); vals.append(hash_senha(senha))
        if disciplina: campos.append("disciplina=%s"); vals.append(disciplina)
        if status: campos.append("status=%s"); vals.append(status)
        if not campos: return {"status":"aviso","mensagem":"Nada para atualizar."}
        vals.append(id_prof)
        cursor.execute("UPDATE Professor SET " + ", ".join(campos) + " WHERE id=%s", tuple(vals))
        conn.commit()
        if cursor.rowcount==0: return {"status":"aviso","mensagem":"Professor não encontrado."}
        return {"status":"sucesso","mensagem":"Professor atualizado."}
    except Exception as e:
        return {"status":"erro","mensagem":str(e)}
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception as e:
                print(f"Erro ao fechar conexão: {e}")

def deletar_professor(id_prof):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Professor WHERE id=%s", (id_prof,))
        conn.commit()
        if cursor.rowcount==0: return {"status":"aviso","mensagem":"Professor não encontrado."}
        return {"status":"sucesso","mensagem":"Professor excluído."}
    except Exception as e:
        return {"status":"erro","mensagem":str(e)}
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception as e:
                print(f"Erro ao fechar conexão: {e}")
