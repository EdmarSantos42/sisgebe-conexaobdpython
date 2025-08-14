# crud_supervisor.py
from db_config import conectar
from hashlib import sha256
def hash_senha(s): return sha256(s.encode('utf-8')).hexdigest()
def criar_supervisor(nome,email,senha,status='ativo'):
    try:
        conn=conectar(); cursor=conn.cursor()
        cursor.execute("INSERT INTO Supervisor (nome,email,senha,status) VALUES (%s,%s,%s,%s)",
                       (nome,email,hash_senha(senha),status))
        conn.commit(); return {"status":"sucesso","mensagem":"Supervisor criado.","id":cursor.lastrowid}
    except Exception as e: return {"status":"erro","mensagem":str(e)}
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception as e:
                print(f"Erro ao fechar conexão: {e}")

def listar_supervisores():
    try:
        conn=conectar(); cursor=conn.cursor(dictionary=True)
        cursor.execute("SELECT id,nome,email,status FROM Supervisor")
        return cursor.fetchall()
    except Exception as e: return {"status":"erro","mensagem":str(e)}
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception as e:
                print(f"Erro ao fechar conexão: {e}")

def atualizar_supervisor(id_s,nome=None,email=None,senha=None,status=None):
    try:
        conn=conectar(); cursor=conn.cursor()
        campos=[]; vals=[]
        if nome: campos.append("nome=%s"); vals.append(nome)
        if email: campos.append("email=%s"); vals.append(email)
        if senha: campos.append("senha=%s"); vals.append(hash_senha(senha))
        if status: campos.append("status=%s"); vals.append(status)
        if not campos: return {"status":"aviso","mensagem":"Nada para atualizar."}
        vals.append(id_s)
        cursor.execute("UPDATE Supervisor SET "+", ".join(campos)+" WHERE id=%s", tuple(vals))
        conn.commit()
        if cursor.rowcount==0: return {"status":"aviso","mensagem":"Supervisor não encontrado."}
        return {"status":"sucesso","mensagem":"Supervisor atualizado."}
    except Exception as e: return {"status":"erro","mensagem":str(e)}
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception as e:
                print(f"Erro ao fechar conexão: {e}")

def deletar_supervisor(id_s):
    try:
        conn=conectar(); cursor=conn.cursor()
        cursor.execute("DELETE FROM Supervisor WHERE id=%s",(id_s,))
        conn.commit()
        if cursor.rowcount==0: return {"status":"aviso","mensagem":"Supervisor não encontrado."}
        return {"status":"sucesso","mensagem":"Supervisor excluído."}
    except Exception as e: return {"status":"erro","mensagem":str(e)}
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception as e:
                print(f"Erro ao fechar conexão: {e}")
