from db_config import conectar

def criar_categoria(nome, descricao):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Categoria (nome, descricao) VALUES (%s, %s)", (nome, descricao))
        conn.commit()
        return{"status": "sucesso", "mensagem":"Categoria criada com sucesso!"}
    except Exception as e:
        return{"status":"erro","mensagem":str(e)}
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception as e:
                print(f"Erro ao fechar conexão: {e}")
        
def listar_categorias():
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Categoria")
        return cursor.fetchall()
    except Exception as e:
        return{"status":"erro","mensagem":str(e)}
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception as e:
                print(f"Erro ao fechar conexão: {e}")

def atualizar_categoria(id_categoria, novo_nome, nova_descricao):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE Categoria SET nome=%s, descricao=%s WHERE id=%s", 
                    (novo_nome, nova_descricao, id_categoria))
        conn.commit()
        if cursor.rowcount == 0:
            return{"status":"aviso","mensagem":"Nenhuma categoria encontrada para atualizar."}
        return{"status":"sucesso","mensagem":"Categoria atualizada!"}
    except Exception as e:
        return{"status":"erro","mensagem":str(e)}
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception as e:
                print(f"Erro ao fechar conexão: {e}")

def deletar_categoria(id_categoria):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Categoria WHERE id=%s", (id_categoria,))
        conn.commit()
        if cursor.rowcount == 0:
            return{"status":"aviso","mensagem":"Nenhuma categoria encontrada para deletar."}
        return{"status":"sucesso","mensagem":"Categoria excluida!"}
    except Exception as e:
        return{"status":"erro","mensagem":str(e)}
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception as e:
                print(f"Erro ao fechar conexão: {e}")

