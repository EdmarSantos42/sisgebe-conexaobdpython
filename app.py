import os
from datetime import date, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, login_user, login_required,
    logout_user, current_user, UserMixin
)
from werkzeug.security import generate_password_hash, check_password_hash

# importa a configuração do banco
from db_config import init_app, db

# importa os models
from models import (
    Aluno, Professor, Bibliotecario, Diretor, Supervisor,
    Livro, Categoria, Emprestimo, Reserva, HistoricoLeitura,
    Sugestao, Relatorio
)

# -------------------- CONFIGURAÇÃO --------------------
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "chave-secreta-padrao")

# inicializa banco com sqlite (db_config cuida disso)
init_app(app)

# -------------------- LOGIN MANAGER --------------------
login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    """
    O Flask-Login precisa que cada classe de usuário herde de UserMixin
    para que login_user e current_user funcionem corretamente.
    """
    return (Aluno.query.get(int(user_id))
            or Professor.query.get(int(user_id))
            or Bibliotecario.query.get(int(user_id))
            or Diretor.query.get(int(user_id))
            or Supervisor.query.get(int(user_id)))


# -------------------- ROTAS PRINCIPAIS --------------------
@app.route("/")
@login_required
def index():
    livros = Livro.query.all()
    return render_template("index.html", livros=livros)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        # tenta localizar usuário em todas as tabelas
        user = (Aluno.query.filter_by(email=email).first()
                or Professor.query.filter_by(email=email).first()
                or Bibliotecario.query.filter_by(email=email).first()
                or Diretor.query.filter_by(email=email).first()
                or Supervisor.query.filter_by(email=email).first())

        if user and check_password_hash(user.senha, senha):
            login_user(user)
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("index"))
        else:
            flash("Email ou senha incorretos", "danger")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você saiu da conta.", "info")
    return redirect(url_for("login"))


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = generate_password_hash(request.form["senha"])
        serie = request.form.get("serie")

        if Aluno.query.filter_by(email=email).first():
            flash("Email já cadastrado!", "danger")
            return redirect(url_for("cadastro"))

        novo_aluno = Aluno(nome=nome, email=email, senha=senha, serie=serie)
        db.session.add(novo_aluno)
        db.session.commit()

        flash("Cadastro realizado! Faça login.", "success")
        return redirect(url_for("login"))

    return render_template("cadastro.html")


# -------------------- ROTAS DE MENU --------------------
@app.route("/categorias")
@login_required
def categorias():
    categorias = Categoria.query.all()
    return render_template("categorias.html", categorias=categorias)


@app.route("/alunos")
@login_required
def alunos():
    alunos = Aluno.query.all()
    return render_template("alunos.html", alunos=alunos)


@app.route("/professores")
@login_required
def professores():
    professores = Professor.query.all()
    return render_template("professores.html", professores=professores)


@app.route("/bibliotecarios")
@login_required
def bibliotecarios():
    bibliotecarios = Bibliotecario.query.all()
    return render_template("bibliotecarios.html", bibliotecarios=bibliotecarios)


@app.route("/diretores")
@login_required
def diretores():
    diretores = Diretor.query.all()
    return render_template("diretores.html", diretores=diretores)


@app.route("/supervisores")
@login_required
def supervisores():
    supervisores = Supervisor.query.all()
    return render_template("supervisores.html", supervisores=supervisores)


@app.route("/livros")
@login_required
def listar_livros():
    livros = Livro.query.all()
    return render_template("livros.html", livros=livros)


@app.route("/emprestimos")
@login_required
def emprestimos():
    emprestimos = Emprestimo.query.all()
    return render_template("emprestimos.html", emprestimos=emprestimos)


@app.route("/reservas")
@login_required
def reservas():
    reservas = Reserva.query.all()
    return render_template("reservas.html", reservas=reservas)


@app.route("/historicos")
@login_required
def historicos():
    historicos = HistoricoLeitura.query.all()
    return render_template("historicos.html", historicos=historicos)


@app.route("/sugestoes")
@login_required
def sugestoes():
    sugestoes = Sugestao.query.all()
    return render_template("sugestoes.html", sugestoes=sugestoes)


@app.route("/relatorios")
@login_required
def relatorios():
    relatorios = Relatorio.query.all()
    return render_template("relatorios.html", relatorios=relatorios)


# -------------------- ROTAS DE AÇÕES --------------------
@app.route("/emprestar/<int:livro_id>")
@login_required
def emprestar(livro_id):
    livro = Livro.query.get_or_404(livro_id)

    if livro.quantidade <= 0:
        flash("Este livro não está disponível.", "warning")
        return redirect(url_for("listar_livros"))

    emprestimo = Emprestimo(
        aluno_id=current_user.id,
        livro_id=livro.id,
        data_emprestimo=date.today(),
        data_devolucao_prevista=date.today() + timedelta(days=7)
    )

    livro.quantidade -= 1
    db.session.add(emprestimo)
    db.session.commit()

    flash("Livro emprestado com sucesso!", "success")
    return redirect(url_for("listar_livros"))


# -------------------- EXECUÇÃO --------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # garante que as tabelas existam
    app.run(debug=True)
