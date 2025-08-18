# app.py

from db_config import conectar
from flask import (
    Flask, render_template, request, redirect, url_for, session, jsonify
)
from functools import wraps
from datetime import date

# CRUDs
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
app.secret_key = "troque_esta_chave_em_producao"

# Página inicial
@app.route("/")
def index():
    return render_template("index.html")

# =========================================================
#                      AUTENTICAÇÃO
# =========================================================
def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if "usuario" not in session:
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapper

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")
        # Login de teste (simples). Trocar por checagem real em produção.
        if email == "admin@biblioteca.com" and senha == "123456":
            session["usuario"] = email
            return redirect(url_for("dashboard"))
        return render_template("login.html", error="E-mail ou senha inválidos.")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("login"))

# =========================================================
#                      DASHBOARD
# =========================================================
@app.route("/")
@login_required
def dashboard():
    return render_template("dashboard.html", titulo="Painel Administrativo")

# =========================================================
#                      WEB PAGES (HTML)
#   Observação: Alguns templates antigos tinham menos campos
#   que o schema. Abaixo fazemos adaptações p/ não quebrar.
# =========================================================

# -------- Categorias --------
@app.route("/categorias", methods=["GET"])
@login_required
def categorias_listar_page():
    categorias = crud_categoria.listar_categorias()
    return render_template("categorias.html", categorias=categorias, titulo="Categorias")

@app.route("/categorias/adicionar", methods=["POST"])
@login_required
def categorias_adicionar_page():
    nome = request.form.get("nome")
    descricao = request.form.get("descricao")
    crud_categoria.criar_categoria(nome, descricao)
    return redirect(url_for("categorias_listar_page"))

@app.route("/categorias/deletar/<int:id>", methods=["GET"])
@login_required
def categorias_deletar_page(id):
    crud_categoria.deletar_categoria(id)
    return redirect(url_for("categorias_listar_page"))

# -------- Livros --------
@app.route("/livros", methods=["GET"])
@login_required
def livros_listar_page():
    livros = crud_livro.listar_livros()
    return render_template("livros.html", livros=livros, titulo="Livros")

@app.route("/livros/adicionar", methods=["POST"])
@login_required
def livros_adicionar_page():
    titulo = request.form.get("titulo")
    autor = request.form.get("autor")
    isbn = request.form.get("isbn")
    sinopse = request.form.get("sinopse")
    capa = request.form.get("capa")
    quantidade = request.form.get("quantidade", 1)
    categoria_id = request.form.get("categoria_id")
    crud_livro.criar_livro(titulo, autor, isbn, sinopse, capa, quantidade, categoria_id)
    return redirect(url_for("livros_listar_page"))

@app.route("/livros/deletar/<int:id>", methods=["GET"])
@login_required
def livros_deletar_page(id):
    crud_livro.deletar_livro(id)
    return redirect(url_for("livros_listar_page"))

# -------- Alunos --------
@app.route("/alunos", methods=["GET"])
@login_required
def alunos_listar_page():
    alunos = crud_aluno.listar_alunos()
    return render_template("alunos.html", alunos=alunos, titulo="Alunos")

@app.route("/alunos/adicionar", methods=["POST"])
@login_required
def alunos_adicionar_page():
    nome = request.form.get("nome")
    email = request.form.get("email")
    # HTML antigo não tinha senha/serie, então setamos defaults de teste
    senha = request.form.get("senha", "123456")
    serie = request.form.get("serie", "1º Ano")
    crud_aluno.criar_aluno(nome, email, senha, serie, "ativo")
    return redirect(url_for("alunos_listar_page"))

@app.route("/alunos/deletar/<int:id>", methods=["GET"])
@login_required
def alunos_deletar_page(id):
    crud_aluno.deletar_aluno(id)
    return redirect(url_for("alunos_listar_page"))

# -------- Professores --------
@app.route("/professores", methods=["GET"])
@login_required
def professores_listar_page():
    professores = crud_professor.listar_professores()
    return render_template("professores.html", professores=professores, titulo="Professores")

@app.route("/professores/adicionar", methods=["POST"])
@login_required
def professores_adicionar_page():
    nome = request.form.get("nome")
    email = request.form.get("email")
    senha = request.form.get("senha", "123456")
    disciplina = request.form.get("disciplina", "")
    crud_professor.criar_professor(nome, email, senha, disciplina, "ativo")
    return redirect(url_for("professores_listar_page"))

@app.route("/professores/deletar/<int:id>", methods=["GET"])
@login_required
def professores_deletar_page(id):
    crud_professor.deletar_professor(id)
    return redirect(url_for("professores_listar_page"))

# -------- Bibliotecários --------
@app.route("/bibliotecarios", methods=["GET"])
@login_required
def bibliotecarios_listar_page():
    bibliotecarios = crud_bibliotecario.listar_bibliotecarios()
    return render_template("bibliotecarios.html", bibliotecarios=bibliotecarios, titulo="Bibliotecários")

@app.route("/bibliotecarios/adicionar", methods=["POST"])
@login_required
def bibliotecarios_adicionar_page():
    nome = request.form.get("nome")
    email = request.form.get("email")
    senha = request.form.get("senha", "123456")
    crud_bibliotecario.criar_bibliotecario(nome, email, senha, "ativo")
    return redirect(url_for("bibliotecarios_listar_page"))

@app.route("/bibliotecarios/deletar/<int:id>", methods=["GET"])
@login_required
def bibliotecarios_deletar_page(id):
    crud_bibliotecario.deletar_bibliotecario(id)
    return redirect(url_for("bibliotecarios_listar_page"))

# -------- Diretores --------
@app.route("/diretores", methods=["GET"])
@login_required
def diretores_listar_page():
    diretores = crud_diretor.listar_diretores()
    return render_template("diretores.html", diretores=diretores, titulo="Diretores")

@app.route("/diretores/adicionar", methods=["POST"])
@login_required
def diretores_adicionar_page():
    nome = request.form.get("nome")
    email = request.form.get("email")
    senha = request.form.get("senha", "123456")
    crud_diretor.criar_diretor(nome, email, senha, "ativo")
    return redirect(url_for("diretores_listar_page"))

@app.route("/diretores/deletar/<int:id>", methods=["GET"])
@login_required
def diretores_deletar_page(id):
    crud_diretor.deletar_diretor(id)
    return redirect(url_for("diretores_listar_page"))

# -------- Supervisores --------
@app.route("/supervisores", methods=["GET"])
@login_required
def supervisores_listar_page():
    supervisores = crud_supervisor.listar_supervisores()
    return render_template("supervisores.html", supervisores=supervisores, titulo="Supervisores")

@app.route("/supervisores/adicionar", methods=["POST"])
@login_required
def supervisores_adicionar_page():
    nome = request.form.get("nome")
    email = request.form.get("email")
    senha = request.form.get("senha", "123456")
    crud_supervisor.criar_supervisor(nome, email, senha, "ativo")
    return redirect(url_for("supervisores_listar_page"))

@app.route("/supervisores/deletar/<int:id>", methods=["GET"])
@login_required
def supervisores_deletar_page(id):
    crud_supervisor.deletar_supervisor(id)
    return redirect(url_for("supervisores_listar_page"))

# -------- Empréstimos --------
@app.route("/emprestimos", methods=["GET"])
@login_required
def emprestimos_listar_page():
    emprestimos = crud_emprestimo.listar_emprestimos(so_abertos=False)
    # Template antigo usa e.data_devolucao; vamos expor prevista como 'data_devolucao'
    for e in emprestimos if isinstance(emprestimos, list) else []:
        if "data_devolucao" not in e:
            e["data_devolucao"] = e.get("data_devolucao_prevista")
        # e.id_livro / e.id_aluno podem vir como livro_id / aluno_id
        e["id_livro"] = e.get("livro_id", e.get("id_livro"))
        e["id_aluno"] = e.get("aluno_id", e.get("id_aluno"))
    return render_template("emprestimos.html", emprestimos=emprestimos, titulo="Empréstimos")

@app.route("/emprestimos/adicionar", methods=["POST"])
@login_required
def emprestimos_adicionar_page():
    id_livro = request.form.get("id_livro")
    id_aluno = request.form.get("id_aluno")
    data_emprestimo = request.form.get("data_emprestimo", date.today().isoformat())
    data_devolucao_prevista = request.form.get("data_devolucao")  # nome no HTML
    crud_emprestimo.criar_emprestimo(id_aluno, id_livro, data_emprestimo, data_devolucao_prevista)
    return redirect(url_for("emprestimos_listar_page"))

@app.route("/emprestimos/deletar/<int:id>", methods=["GET"])
@login_required
def emprestimos_deletar_page(id):
    # Não havia deletar no CRUD, mas podemos criar um fallback:
    # Aqui, apenas marcaria devolução real como hoje (se existir endpoint).
    crud_emprestimo.devolver_emprestimo(id, date.today().isoformat())
    return redirect(url_for("emprestimos_listar_page"))

# -------- Reservas --------
@app.route("/reservas", methods=["GET"])
@login_required
def reservas_listar_page():
    reservas = crud_reserva.listar_reservas(so_ativas=False)
    # Normalizar nomes p/ HTML simples
    for r in reservas if isinstance(reservas, list) else []:
        r["id_livro"] = r.get("livro_id", r.get("id_livro"))
        r["id_aluno"] = r.get("aluno_id", r.get("id_aluno"))
    return render_template("reservas.html", reservas=reservas, titulo="Reservas")

@app.route("/reservas/adicionar", methods=["POST"])
@login_required
def reservas_adicionar_page():
    id_livro = request.form.get("id_livro")
    id_aluno = request.form.get("id_aluno")
    data_reserva = request.form.get("data_reserva", date.today().isoformat())
    crud_reserva.criar_reserva(id_aluno, id_livro, data_reserva)
    return redirect(url_for("reservas_listar_page"))

@app.route("/reservas/deletar/<int:id>", methods=["GET"])
@login_required
def reservas_deletar_page(id):
    crud_reserva.deletar_reserva(id)
    return redirect(url_for("reservas_listar_page"))

# -------- Histórico de Leitura --------
@app.route("/historicos", methods=["GET"])
@login_required
def historicos_listar_page():
    historicos = crud_historico.listar_historico()
    # Template espera "data_leitura"; usamos data_inicio se existir
    for h in historicos if isinstance(historicos, list) else []:
        if "data_leitura" not in h:
            h["data_leitura"] = h.get("data_inicio")
        h["id_livro"] = h.get("livro_id", h.get("id_livro"))
        h["id_aluno"] = h.get("aluno_id", h.get("id_aluno"))
    return render_template("historicos.html", historicos=historicos, titulo="Histórico de Leitura")

@app.route("/historicos/adicionar", methods=["POST"])
@login_required
def historicos_adicionar_page():
    id_livro = request.form.get("id_livro")
    id_aluno = request.form.get("id_aluno")
    data_leitura = request.form.get("data_leitura", date.today().isoformat())
    # Como HTML antigo não tem início/fim, salvamos início = data_leitura e fim = None
    crud_historico.criar_historico(id_aluno, id_livro, data_leitura, None)
    return redirect(url_for("historicos_listar_page"))

@app.route("/historicos/deletar/<int:id>", methods=["GET"])
@login_required
def historicos_deletar_page(id):
    # Se houver um deletar no CRUD, use; se não houver, crie depois. Por ora, ignoramos.
    # Poderia ser implementado similar ao reservas_deletar_page
    return redirect(url_for("historicos_listar_page"))

# -------- Sugestões --------
@app.route("/sugestoes", methods=["GET"])
@login_required
def sugestoes_listar_page():
    sugestoes = crud_sugestao.listar_sugestoes()
    # Template antigo usa "titulo" e "descricao"; mapear justificativa -> descricao
    for s in sugestoes if isinstance(sugestoes, list) else []:
        if "descricao" not in s:
            s["descricao"] = s.get("justificativa", "")
    return render_template("sugestoes.html", sugestoes=sugestoes, titulo="Sugestões")

@app.route("/sugestoes/adicionar", methods=["POST"])
@login_required
def sugestoes_adicionar_page():
    titulo = request.form.get("titulo")
    descricao = request.form.get("descricao")  # mapeia para justificativa
    # Campos que o HTML não pede:
    autor = None
    categoria = None
    data_sugestao = date.today().isoformat()
    aluno_id = None
    professor_id = None
    crud_sugestao.criar_sugestao(titulo, autor, categoria, descricao, data_sugestao, aluno_id, professor_id)
    return redirect(url_for("sugestoes_listar_page"))

@app.route("/sugestoes/deletar/<int:id>", methods=["GET"])
@login_required
def sugestoes_deletar_page(id):
    # Caso seu CRUD tenha deletar. Se não tiver, adicione depois.
    return redirect(url_for("sugestoes_listar_page"))

# -------- Relatórios --------
@app.route("/relatorios", methods=["GET"])
@login_required
def relatorios_listar_page():
    relatorios = crud_relatorio.listar_relatorios()
    # Template antigo usa "titulo" e "conteudo". Vamos sintetizá-los.
    for r in relatorios if isinstance(relatorios, list) else []:
        tipo = r.get("tipo", "desconhecido")
        p_ini = r.get("periodo_inicio") or ""
        p_fim = r.get("periodo_fim") or ""
        r["titulo"] = r.get("titulo") or f"Relatório {tipo}"
        r["conteudo"] = r.get("conteudo") or f"Período: {p_ini} a {p_fim}"
    return render_template("relatorios.html", relatorios=relatorios, titulo="Relatórios")

@app.route("/relatorios/adicionar", methods=["POST"])
@login_required
def relatorios_adicionar_page():
    # HTML antigo só envia titulo/conteudo; vamos mapear para o schema
    # tipo default e período vazio para teste
    tipo = "livros"
    periodo_inicio = None
    periodo_fim = None
    gerado_por_bibliotecario = None
    gerado_por_diretor = None
    gerado_por_supervisor = None
    crud_relatorio.criar_relatorio(tipo, periodo_inicio, periodo_fim,
                                   gerado_por_bibliotecario, gerado_por_diretor, gerado_por_supervisor)
    return redirect(url_for("relatorios_listar_page"))

@app.route("/relatorios/deletar/<int:id>", methods=["GET"])
@login_required
def relatorios_deletar_page(id):
    # Se houver deletar no CRUD, chame aqui.
    return redirect(url_for("relatorios_listar_page"))

# =========================================================
#                      API REST (JSON)
#   Mantidas para mobile/integrações. Proteja com auth se quiser.
# =========================================================

# ---- Categoria ----
@app.route('/api/categorias', methods=['POST'])
def api_criar_categoria():
    d = request.json or {}
    return jsonify(crud_categoria.criar_categoria(d.get("nome"), d.get("descricao")))

@app.route('/api/categorias', methods=['GET'])
def api_listar_categorias():
    return jsonify(crud_categoria.listar_categorias())

@app.route('/api/categorias/<int:id>', methods=['PUT'])
def api_atualizar_categoria(id):
    d = request.json or {}
    return jsonify(crud_categoria.atualizar_categoria(id, d.get("nome"), d.get("descricao")))

@app.route('/api/categorias/<int:id>', methods=['DELETE'])
def api_deletar_categoria(id):
    return jsonify(crud_categoria.deletar_categoria(id))

# ---- Livro ----
@app.route('/api/livros', methods=['POST'])
def api_criar_livro():
    d = request.json or {}
    return jsonify(crud_livro.criar_livro(
        d.get("titulo"), d.get("autor"), d.get("isbn"), d.get("sinopse"),
        d.get("capa"), d.get("quantidade", 1), d.get("categoria_id")
    ))

@app.route('/api/livros', methods=['GET'])
def api_listar_livros():
    return jsonify(crud_livro.listar_livros())

@app.route('/api/livros/<int:id>', methods=['GET'])
def api_obter_livro(id):
    return jsonify(crud_livro.obter_livro(id))

@app.route('/api/livros/<int:id>', methods=['PUT'])
def api_atualizar_livro(id):
    d = request.json or {}
    return jsonify(crud_livro.atualizar_livro(
        id, d.get("titulo"), d.get("autor"), d.get("isbn"), d.get("sinopse"),
        d.get("capa"), d.get("quantidade"), d.get("categoria_id")
    ))

@app.route('/api/livros/<int:id>', methods=['DELETE'])
def api_deletar_livro(id):
    return jsonify(crud_livro.deletar_livro(id))

# ---- Aluno ----
@app.route('/api/alunos', methods=['POST'])
def api_criar_aluno():
    d = request.json or {}
    return jsonify(crud_aluno.criar_aluno(
        d.get("nome"), d.get("email"), d.get("senha"), d.get("serie"), d.get("status", "ativo")
    ))

@app.route('/api/alunos', methods=['GET'])
def api_listar_alunos():
    return jsonify(crud_aluno.listar_alunos())

@app.route('/api/alunos/<int:id>', methods=['GET'])
def api_obter_aluno(id):
    return jsonify(crud_aluno.obter_aluno(id))

@app.route('/api/alunos/<int:id>', methods=['PUT'])
def api_atualizar_aluno(id):
    d = request.json or {}
    return jsonify(crud_aluno.atualizar_aluno(
        id, d.get("nome"), d.get("email"), d.get("senha"), d.get("serie"), d.get("status")
    ))

@app.route('/api/alunos/<int:id>', methods=['DELETE'])
def api_deletar_aluno(id):
    return jsonify(crud_aluno.deletar_aluno(id))

# ---- Professor ----
@app.route('/api/professores', methods=['POST'])
def api_criar_professor():
    d = request.json or {}
    return jsonify(crud_professor.criar_professor(
        d.get("nome"), d.get("email"), d.get("senha"), d.get("disciplina"), d.get("status", "ativo")
    ))

@app.route('/api/professores', methods=['GET'])
def api_listar_professores():
    return jsonify(crud_professor.listar_professores())

@app.route('/api/professores/<int:id>', methods=['PUT'])
def api_atualizar_professor(id):
    d = request.json or {}
    return jsonify(crud_professor.atualizar_professor(
        id, d.get("nome"), d.get("email"), d.get("senha"), d.get("disciplina"), d.get("status")
    ))

@app.route('/api/professores/<int:id>', methods=['DELETE'])
def api_deletar_professor(id):
    return jsonify(crud_professor.deletar_professor(id))

# ---- Bibliotecario ----
@app.route('/api/bibliotecarios', methods=['POST'])
def api_criar_bibliotecario():
    d = request.json or {}
    return jsonify(crud_bibliotecario.criar_bibliotecario(
        d.get("nome"), d.get("email"), d.get("senha"), d.get("status", "ativo")
    ))

@app.route('/api/bibliotecarios', methods=['GET'])
def api_listar_bibliotecarios():
    return jsonify(crud_bibliotecario.listar_bibliotecarios())

@app.route('/api/bibliotecarios/<int:id>', methods=['PUT'])
def api_atualizar_bibliotecario(id):
    d = request.json or {}
    return jsonify(crud_bibliotecario.atualizar_bibliotecario(
        id, d.get("nome"), d.get("email"), d.get("senha"), d.get("status")
    ))

@app.route('/api/bibliotecarios/<int:id>', methods=['DELETE'])
def api_deletar_bibliotecario(id):
    return jsonify(crud_bibliotecario.deletar_bibliotecario(id))

# ---- Diretor ----
@app.route('/api/diretores', methods=['POST'])
def api_criar_diretor():
    d = request.json or {}
    return jsonify(crud_diretor.criar_diretor(
        d.get("nome"), d.get("email"), d.get("senha"), d.get("status", "ativo")
    ))

@app.route('/api/diretores', methods=['GET'])
def api_listar_diretores():
    return jsonify(crud_diretor.listar_diretores())

@app.route('/api/diretores/<int:id>', methods=['PUT'])
def api_atualizar_diretor(id):
    d = request.json or {}
    return jsonify(crud_diretor.atualizar_diretor(
        id, d.get("nome"), d.get("email"), d.get("senha"), d.get("status")
    ))

@app.route('/api/diretores/<int:id>', methods=['DELETE'])
def api_deletar_diretor(id):
    return jsonify(crud_diretor.deletar_diretor(id))

# ---- Supervisor ----
@app.route('/api/supervisores', methods=['POST'])
def api_criar_supervisor():
    d = request.json or {}
    return jsonify(crud_supervisor.criar_supervisor(
        d.get("nome"), d.get("email"), d.get("senha"), d.get("status", "ativo")
    ))

@app.route('/api/supervisores', methods=['GET'])
def api_listar_supervisores():
    return jsonify(crud_supervisor.listar_supervisores())

@app.route('/api/supervisores/<int:id>', methods=['PUT'])
def api_atualizar_supervisor(id):
    d = request.json or {}
    return jsonify(crud_supervisor.atualizar_supervisor(
        id, d.get("nome"), d.get("email"), d.get("senha"), d.get("status")
    ))

@app.route('/api/supervisores/<int:id>', methods=['DELETE'])
def api_deletar_supervisor(id):
    return jsonify(crud_supervisor.deletar_supervisor(id))

# ---- Empréstimo ----
@app.route('/api/emprestimos', methods=['POST'])
def api_criar_emprestimo():
    d = request.json or {}
    return jsonify(crud_emprestimo.criar_emprestimo(
        d.get("aluno_id"), d.get("livro_id"), d.get("data_emprestimo"), d.get("data_devolucao_prevista")
    ))

@app.route('/api/emprestimos', methods=['GET'])
def api_listar_emprestimos():
    so_abertos = (request.args.get("abertos", "false").lower() == "true")
    return jsonify(crud_emprestimo.listar_emprestimos(so_abertos))

@app.route('/api/emprestimos/<int:id>/devolver', methods=['POST'])
def api_devolver_emprestimo(id):
    d = request.json or {}
    return jsonify(crud_emprestimo.devolver_emprestimo(id, d.get("data_devolucao_real")))

# ---- Reserva ----
@app.route('/api/reservas', methods=['POST'])
def api_criar_reserva():
    d = request.json or {}
    return jsonify(crud_reserva.criar_reserva(
        d.get("aluno_id"), d.get("livro_id"), d.get("data_reserva")
    ))

@app.route('/api/reservas', methods=['GET'])
def api_listar_reservas():
    so_ativas = (request.args.get("ativas", "false").lower() == "true")
    return jsonify(crud_reserva.listar_reservas(so_ativas))

@app.route('/api/reservas/<int:id>', methods=['PUT'])
def api_atualizar_reserva(id):
    d = request.json or {}
    return jsonify(crud_reserva.atualizar_reserva(id, d.get("status")))

@app.route('/api/reservas/<int:id>', methods=['DELETE'])
def api_deletar_reserva(id):
    return jsonify(crud_reserva.deletar_reserva(id))

# ---- Histórico de Leitura ----
@app.route('/api/historicos', methods=['POST'])
def api_criar_historico():
    d = request.json or {}
    return jsonify(crud_historico.criar_historico(
        d.get("aluno_id"), d.get("livro_id"), d.get("data_inicio"), d.get("data_fim")
    ))

@app.route('/api/historicos', methods=['GET'])
def api_listar_historico():
    aluno_id = request.args.get("aluno_id")
    return jsonify(crud_historico.listar_historico(aluno_id))

# ---- Sugestão ----
@app.route('/api/sugestoes', methods=['POST'])
def api_criar_sugestao():
    d = request.json or {}
    return jsonify(crud_sugestao.criar_sugestao(
        d.get("titulo"), d.get("autor"), d.get("categoria"), d.get("justificativa"),
        d.get("data_sugestao"), d.get("aluno_id"), d.get("professor_id")
    ))

@app.route('/api/sugestoes', methods=['GET'])
def api_listar_sugestoes():
    return jsonify(crud_sugestao.listar_sugestoes())

# ---- Relatório ----
@app.route('/api/relatorios', methods=['POST'])
def api_criar_relatorio():
    d = request.json or {}
    return jsonify(crud_relatorio.criar_relatorio(
        d.get("tipo"), d.get("periodo_inicio"), d.get("periodo_fim"),
        d.get("gerado_por_bibliotecario"), d.get("gerado_por_diretor"), d.get("gerado_por_supervisor")
    ))

@app.route('/api/relatorios', methods=['GET'])
def api_listar_relatorios():
    return jsonify(crud_relatorio.listar_relatorios())

# =========================================================
#                 ERROS AMIGÁVEIS (opcional)
# =========================================================
@app.errorhandler(404)
def not_found(e):
    if "usuario" in session:
        return render_template("dashboard.html", titulo="Não encontrado"), 404
    return redirect(url_for("login"))

# =========================================================
#                       RUN
# =========================================================
if __name__ == "__main__":
    # Em produção, use um servidor WSGI (gunicorn/uwsgi) e desative debug
    app.run(debug=True)
