from db_config import db
from flask_login import UserMixin
from datetime import datetime

# ----------------- USUÁRIOS -----------------

class Aluno(UserMixin, db.Model):
    __tablename__ = "alunos"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    serie = db.Column(db.String(50))

    emprestimos = db.relationship("Emprestimo", backref="aluno", lazy=True)
    reservas = db.relationship("Reserva", backref="aluno", lazy=True)
    historico = db.relationship("HistoricoLeitura", backref="aluno", lazy=True)

class Professor(UserMixin, db.Model):
    __tablename__ = "professores"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)

class Bibliotecario(UserMixin, db.Model):
    __tablename__ = "bibliotecarios"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)

class Diretor(UserMixin, db.Model):
    __tablename__ = "diretores"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)

class Supervisor(UserMixin, db.Model):
    __tablename__ = "supervisores"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)

# ----------------- LIVROS -----------------

class Categoria(db.Model):
    __tablename__ = "categorias"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)

    livros = db.relationship("Livro", backref="categoria", lazy=True)

class Livro(db.Model):
    __tablename__ = "livros"
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    autor = db.Column(db.String(120), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False, default=1)
    categoria_id = db.Column(db.Integer, db.ForeignKey("categorias.id"), nullable=True)

    emprestimos = db.relationship("Emprestimo", backref="livro", lazy=True)
    reservas = db.relationship("Reserva", backref="livro", lazy=True)
    historico = db.relationship("HistoricoLeitura", backref="livro", lazy=True)

# ----------------- EMPRÉSTIMOS E RESERVAS -----------------

class Emprestimo(db.Model):
    __tablename__ = "emprestimos"
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey("alunos.id"), nullable=False)
    livro_id = db.Column(db.Integer, db.ForeignKey("livros.id"), nullable=False)
    data_emprestimo = db.Column(db.Date, default=datetime.utcnow)
    data_devolucao_prevista = db.Column(db.Date)
    data_devolucao_real = db.Column(db.Date, nullable=True)

class Reserva(db.Model):
    __tablename__ = "reservas"
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey("alunos.id"), nullable=False)
    livro_id = db.Column(db.Integer, db.ForeignKey("livros.id"), nullable=False)
    data_reserva = db.Column(db.DateTime, default=datetime.utcnow)

# ----------------- HISTÓRICO -----------------

class HistoricoLeitura(db.Model):
    __tablename__ = "historicos"
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey("alunos.id"), nullable=False)
    livro_id = db.Column(db.Integer, db.ForeignKey("livros.id"), nullable=False)
    data_leitura = db.Column(db.DateTime, default=datetime.utcnow)

# ----------------- OUTROS -----------------

class Sugestao(db.Model):
    __tablename__ = "sugestoes"
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey("alunos.id"), nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    autor = db.Column(db.String(120), nullable=False)
    data_sugestao = db.Column(db.DateTime, default=datetime.utcnow)

class Relatorio(db.Model):
    __tablename__ = "relatorios"
    id = db.Column(db.Integer, primary_key=True)
    bibliotecario_id = db.Column(db.Integer, db.ForeignKey("bibliotecarios.id"))
    conteudo = db.Column(db.Text, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
