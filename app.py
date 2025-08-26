import os
import models  # registra os modelos
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date, timedelta
from db_config import init_app, db
from urllib.parse import quote_plus

app = Flask(__name__)
init_app(app)  # aqui sim você passa o app para configurar

# importa os models
from models import (
    db, Aluno, Professor, Bibliotecario, Diretor, Supervisor,
    Livro, Categoria, Emprestimo, Reserva, HistoricoLeitura,
    Sugestao, Relatorio
)

load_dotenv()  # carrega variáveis do .env

# Pega valores do .env
user = os.getenv("DB_USER")
password = quote_plus(os.getenv("DB_PASSWORD"))  # escapa caracteres especiais
host = os.getenv("DB_HOST", "127.0.0.1")
port = os.getenv("DB_PORT", "3306")
dbname = os.getenv("DB_NAME")

# Configuração Flask
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

# Configuração SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{dbname}"
)


# Configuração do banco
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "03ea75a2b0d264b0cc7cb8f82b73a766")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    # aqui podemos buscar o usuário em qualquer tabela
    return (Aluno.query.get(int(user_id))
            or Professor.query.get(int(user_id))
            or Bibliotecario.query.get(int(user_id))
            or Diretor.query.get(int(user_id))
            or Supervisor.query.get(int(user_id)))

# ---------- ROTAS ----------

@app.route("/")
def index():
    livros = Livro.query.all()
    return render_template("index.html", livros=livros)

@app.route("/")
def home():
    return "Servidor Flask rodando com SQLite 🚀"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        # busca em todas as tabelas de usuários
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
    return redirect(url_for("index"))


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


@app.route("/livros")
@login_required
def listar_livros():
    livros = Livro.query.all()
    return render_template("livros.html", livros=livros)


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
        data_devolucao_prevista = date.today() + timedelta(days=7)
    )

    livro.quantidade -= 1
    db.session.add(emprestimo)
    db.session.commit()

    flash("Livro emprestado com sucesso!", "success")
    return redirect(url_for("listar_livros"))

# --------- EXECUTAR ----------
if __name__ == "__main__":
    app.run(debug=True)
