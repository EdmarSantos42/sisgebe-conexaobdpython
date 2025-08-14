# app.py

from db_config import conectar
from crud import categoria
from flask import Flask, request, jsonify
import crud.categoria as crud_categoria
import crud.livro as crud_livro
import crud.aluno as crud_aluno
import crud.professor as crud_professor
import crud.bibliotecario as crud_bibliotecario
import crud.diretor as crud_diretor
import crud.supervisor as crud_supervisor
import crud.emprestimo as crud_emprestimo
import crud.reserva as crud_reserva
import crud.historicoleitura as crud_historico
import crud.sugestao as crud_sugestao
import crud.relatorio as crud_relatorio

app = Flask(__name__)

def main():
    conexao= conectar()
    if conexao:
        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM livros;")  # Exemplo de consulta simples

            resultados = cursor.fetchall()

            print("\nLivros cadastrados:")
            for linha in resultados:
                print(linha)

        except Exception as e:
            print(f"Erro na execução: {e}")
        finally:
            conexao.close()
            print("\nConexão encerrada.")

if __name__ == "__main__":
    main()

def menu():
    while True:
        print("\n=== MENU SGB ===")
        print("1. Criar Categoria")
        print("2. Listar Categorias")
        print("3. Atualizar Categoria")
        print("4. Deletar Categoria")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome da categoria: ")
            descricao = input("Descrição: ")
            categoria.criar_categoria(nome, descricao)
        elif opcao == "2":
            cats = categoria.listar_categorias()
            for c in cats:
                print(f"{c['id']} - {c['nome']} ({c['descricao']})")
        elif opcao == "3":
            id_cat = int(input("ID da categoria: "))
            nome = input("Novo nome: ")
            descricao = input("Nova descrição: ")
            categoria.atualizar_categoria(id_cat, nome, descricao)
        elif opcao == "4":
            id_cat = int(input("ID da categoria: "))
            categoria.deletar_categoria(id_cat)
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu()

# --- Livro routes ---
@app.route('/livros', methods=['POST'])
def criar_livro():
    dados = request.json
    resultado = crud_livro.criar_livro(
        dados.get("titulo"), dados.get("autor"), dados.get("isbn"),
        dados.get("sinopse"), dados.get("capa"), dados.get("quantidade",1), dados.get("categoria_id")
    )
    return jsonify(resultado)

@app.route('/livros', methods=['GET'])
def listar_livros():
    return jsonify(crud_livro.listar_livros())

@app.route('/livros/<int:id_livro>', methods=['GET'])
def obter_livro(id_livro):
    return jsonify(crud_livro.obter_livro(id_livro))

@app.route('/livros/<int:id_livro>', methods=['PUT'])
def atualizar_livro(id_livro):
    dados = request.json
    return jsonify(crud_livro.atualizar_livro(
        id_livro, dados.get("titulo"), dados.get("autor"), dados.get("isbn"),
        dados.get("sinopse"), dados.get("capa"), dados.get("quantidade"), dados.get("categoria_id")
    ))

@app.route('/livros/<int:id_livro>', methods=['DELETE'])
def deletar_livro(id_livro):
    return jsonify(crud_livro.deletar_livro(id_livro))

# --- Aluno ---
@app.route('/alunos', methods=['POST'])
def criar_aluno_route():
    d=request.json
    return jsonify(crud_aluno.criar_aluno(d.get("nome"), d.get("email"), d.get("senha"), d.get("serie"), d.get("status","ativo")))

@app.route('/alunos', methods=['GET'])
def listar_alunos_route():
    return jsonify(crud_aluno.listar_alunos())

@app.route('/alunos/<int:id_aluno>', methods=['GET'])
def obter_aluno_route(id_aluno):
    return jsonify(crud_aluno.obter_aluno(id_aluno))

@app.route('/alunos/<int:id_aluno>', methods=['PUT'])
def atualizar_aluno_route(id_aluno):
    d=request.json
    return jsonify(crud_aluno.atualizar_aluno(
        id_aluno, d.get("nome"), d.get("email"), d.get("senha"), d.get("serie"), d.get("status")
    ))

@app.route('/alunos/<int:id_aluno>', methods=['DELETE'])
def deletar_aluno_route(id_aluno):
    return jsonify(crud_aluno.deletar_aluno(id_aluno))

# --- Professor (similares) ---
@app.route('/professores', methods=['POST'])
def criar_prof_route():
    d=request.json
    return jsonify(crud_professor.criar_professor(d.get("nome"), d.get("email"), d.get("senha"), d.get("disciplina"), d.get("status","ativo")))

@app.route('/professores', methods=['GET'])
def listar_prof_route():
    return jsonify(crud_professor.listar_professores())

@app.route('/professores/<int:id_prof>', methods=['PUT'])
def atualizar_prof_route(id_prof):
    d=request.json
    return jsonify(crud_professor.atualizar_professor(id_prof, d.get("nome"), d.get("email"), d.get("senha"), d.get("disciplina"), d.get("status")))

@app.route('/professores/<int:id_prof>', methods=['DELETE'])
def deletar_prof_route(id_prof):
    return jsonify(crud_professor.deletar_professor(id_prof))

# --- Bibliotecario/Diretor/Supervisor (create/list/update/delete) ---
@app.route('/bibliotecarios', methods=['POST'])
def criar_bib_route():
    d=request.json
    return jsonify(crud_bibliotecario.criar_bibliotecario(d.get("nome"), d.get("email"), d.get("senha"), d.get("status","ativo")))

@app.route('/bibliotecarios', methods=['GET'])
def listar_bib_route():
    return jsonify(crud_bibliotecario.listar_bibliotecarios())

@app.route('/bibliotecarios/<int:id_b>', methods=['PUT'])
def atualizar_bib_route(id_b):
    d=request.json
    return jsonify(crud_bibliotecario.atualizar_bibliotecario(id_b, d.get("nome"), d.get("email"), d.get("senha"), d.get("status")))

@app.route('/bibliotecarios/<int:id_b>', methods=['DELETE'])
def deletar_bib_route(id_b):
    return jsonify(crud_bibliotecario.deletar_bibliotecario(id_b))

# Diretor
@app.route('/diretores', methods=['POST'])
def criar_dir_route():
    d=request.json
    return jsonify(crud_diretor.criar_diretor(d.get("nome"), d.get("email"), d.get("senha"), d.get("status","ativo")))

@app.route('/diretores', methods=['GET'])
def listar_dir_route():
    return jsonify(crud_diretor.listar_diretores())

@app.route('/diretores/<int:id_d>', methods=['PUT'])
def atualizar_dir_route(id_d):
    d=request.json
    return jsonify(crud_diretor.atualizar_diretor(id_d, d.get("nome"), d.get("email"), d.get("senha"), d.get("status")))

@app.route('/diretores/<int:id_d>', methods=['DELETE'])
def deletar_dir_route(id_d):
    return jsonify(crud_diretor.deletar_diretor(id_d))

# Supervisor
@app.route('/supervisores', methods=['POST'])
def criar_sup_route():
    d=request.json
    return jsonify(crud_supervisor.criar_supervisor(d.get("nome"), d.get("email"), d.get("senha"), d.get("status","ativo")))

@app.route('/supervisores', methods=['GET'])
def listar_sup_route():
    return jsonify(crud_supervisor.listar_supervisores())

@app.route('/supervisores/<int:id_s>', methods=['PUT'])
def atualizar_sup_route(id_s):
    d=request.json
    return jsonify(crud_supervisor.atualizar_supervisor(id_s, d.get("nome"), d.get("email"), d.get("senha"), d.get("status")))

@app.route('/supervisores/<int:id_s>', methods=['DELETE'])
def deletar_sup_route(id_s):
    return jsonify(crud_supervisor.deletar_supervisor(id_s))

# --- Empréstimos ---
@app.route('/emprestimos', methods=['POST'])
def criar_emprestimo_route():
    d=request.json
    return jsonify(crud_emprestimo.criar_emprestimo(d.get("aluno_id"), d.get("livro_id"), d.get("data_emprestimo"), d.get("data_devolucao_prevista")))

@app.route('/emprestimos', methods=['GET'])
def listar_emprestimos_route():
    so_abertos = request.args.get("abertos","false").lower()=="true"
    return jsonify(crud_emprestimo.listar_emprestimos(so_abertos))

@app.route('/emprestimos/<int:id_e>/devolver', methods=['POST'])
def devolver_emprestimo_route(id_e):
    d=request.json or {}
    return jsonify(crud_emprestimo.devolver_emprestimo(id_e, d.get("data_devolucao_real")))

# --- Reservas ---
@app.route('/reservas', methods=['POST'])
def criar_reserva_route():
    d=request.json
    return jsonify(crud_reserva.criar_reserva(d.get("aluno_id"), d.get("livro_id"), d.get("data_reserva")))

@app.route('/reservas', methods=['GET'])
def listar_reservas_route():
    ativas = request.args.get("ativas","false").lower()=="true"
    return jsonify(crud_reserva.listar_reservas(so_ativas=ativas))

@app.route('/reservas/<int:id_r>', methods=['PUT'])
def atualizar_reserva_route(id_r):
    d=request.json
    return jsonify(crud_reserva.atualizar_reserva(id_r, d.get("status")))

@app.route('/reservas/<int:id_r>', methods=['DELETE'])
def deletar_reserva_route(id_r):
    return jsonify(crud_reserva.deletar_reserva(id_r))

# --- HistoricoLeitura ---
@app.route('/historico', methods=['POST'])
def criar_historico_route():
    d=request.json
    return jsonify(crud_historico.criar_historico(d.get("aluno_id"), d.get("livro_id"), d.get("data_inicio"), d.get("data_fim")))

@app.route('/historico', methods=['GET'])
def listar_historico_route():
    aluno = request.args.get("aluno_id")
    return jsonify(crud_historico.listar_historico(aluno_id=aluno))

# --- Sugestao ---
@app.route('/sugestoes', methods=['POST'])
def criar_sugestao_route():
    d=request.json
    return jsonify(crud_sugestao.criar_sugestao(d.get("titulo"), d.get("autor"), d.get("categoria"), d.get("justificativa"), d.get("data_sugestao"), d.get("aluno_id"), d.get("professor_id")))

@app.route('/sugestoes', methods=['GET'])
def listar_sugestoes_route():
    return jsonify(crud_sugestao.listar_sugestoes())

# --- Relatorios ---
@app.route('/relatorios', methods=['POST'])
def criar_relatorio_route():
    d=request.json
    return jsonify(crud_relatorio.criar_relatorio(d.get("tipo"), d.get("periodo_inicio"), d.get("periodo_fim"), d.get("gerado_por_bibliotecario"), d.get("gerado_por_diretor"), d.get("gerado_por_supervisor")))

@app.route('/relatorios', methods=['GET'])
def listar_relatorios_route():
    return jsonify(crud_relatorio.listar_relatorios())

if __name__ == "__main__":
    app.run(debug=True)