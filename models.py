# models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import enum

db = SQLAlchemy()

# ---------- ENUMS ----------
class StatusAluno(enum.Enum):
    ativo = "ativo"
    bloqueado = "bloqueado"

class StatusGeral(enum.Enum):
    ativo = "ativo"
    inativo = "inativo"

class StatusReserva(enum.Enum):
    ativa = "ativa"
    expirada = "expirada"
    cancelada = "cancelada"

class TipoRelatorio(enum.Enum):
    mensal = "mensal"
    turma = "turma"
    aluno = "aluno"
    livros = "livros"

# ---------- MODELS ----------
class Categoria(db.Model):
    __tablename__ = "categoria"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.Text)
    livros = db.relationship("Livro", backref="categoria", lazy=True)

class Livro(db.Model):
    __tablename__ = "livro"
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(20), unique=True)
    sinopse = db.Column(db.Text)
    capa = db.Column(db.Text)
    quantidade = db.Column(db.Integer, default=1)
    categoria_id = db.Column(db.Integer, db.ForeignKey("categoria.id"))
    emprestimos = db.relationship("Emprestimo", backref="livro", lazy=True)
    reservas = db.relationship("Reserva", backref="livro", lazy=True)
    historicos = db.relationship("HistoricoLeitura", backref="livro", lazy=True)

class Aluno(UserMixin, db.Model):
    __tablename__ = "aluno"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    serie = db.Column(db.String(20), nullable=False)
    status = db.Column(db.Enum(StatusAluno), default=StatusAluno.ativo)
    emprestimos = db.relationship("Emprestimo", backref="aluno", lazy=True)
    reservas = db.relationship("Reserva", backref="aluno", lazy=True)
    historicos = db.relationship("HistoricoLeitura", backref="aluno", lazy=True)
    sugestoes = db.relationship("Sugestao", backref="aluno", lazy=True)

class Professor(UserMixin, db.Model):
    __tablename__ = "professor"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    disciplina = db.Column(db.String(50))
    status = db.Column(db.Enum(StatusGeral), default=StatusGeral.ativo)
    sugestoes = db.relationship("Sugestao", backref="professor", lazy=True)

class Bibliotecario(UserMixin, db.Model):
    __tablename__ = "bibliotecario"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Enum(StatusGeral), default=StatusGeral.ativo)
    relatorios = db.relationship("Relatorio", backref="bibliotecario", lazy=True)

class Diretor(UserMixin, db.Model):
    __tablename__ = "diretor"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Enum(StatusGeral), default=StatusGeral.ativo)
    relatorios = db.relationship("Relatorio", backref="diretor", lazy=True)

class Supervisor(UserMixin, db.Model):
    __tablename__ = "supervisor"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Enum(StatusGeral), default=StatusGeral.ativo)
    relatorios = db.relationship("Relatorio", backref="supervisor", lazy=True)

class Emprestimo(db.Model):
    __tablename__ = "emprestimo"
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey("aluno.id"))
    livro_id = db.Column(db.Integer, db.ForeignKey("livro.id"))
    data_emprestimo = db.Column(db.Date, nullable=False)
    data_devolucao_prevista = db.Column(db.Date)
    data_devolucao_real = db.Column(db.Date)
    multa = db.Column(db.Numeric(6, 2), default=0.00)

class Reserva(db.Model):
    __tablename__ = "reserva"
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey("aluno.id"))
    livro_id = db.Column(db.Integer, db.ForeignKey("livro.id"))
    data_reserva = db.Column(db.Date)
    status = db.Column(db.Enum(StatusReserva))

class HistoricoLeitura(db.Model):
    __tablename__ = "historico_leitura"
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey("aluno.id"))
    livro_id = db.Column(db.Integer, db.ForeignKey("livro.id"))
    data_inicio = db.Column(db.Date)
    data_fim = db.Column(db.Date)

class Sugestao(db.Model):
    __tablename__ = "sugestao"
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150))
    autor = db.Column(db.String(100))
    categoria = db.Column(db.String(50))
    justificativa = db.Column(db.Text)
    data_sugestao = db.Column(db.Date)
    aluno_id = db.Column(db.Integer, db.ForeignKey("aluno.id"))
    professor_id = db.Column(db.Integer, db.ForeignKey("professor.id"))

class Relatorio(db.Model):
    __tablename__ = "relatorio"
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.Enum(TipoRelatorio))
    periodo_inicio = db.Column(db.Date)
    periodo_fim = db.Column(db.Date)
    gerado_por_bibliotecario = db.Column(db.Integer, db.ForeignKey("bibliotecario.id"))
    gerado_por_diretor = db.Column(db.Integer, db.ForeignKey("diretor.id"))
    gerado_por_supervisor = db.Column(db.Integer, db.ForeignKey("supervisor.id"))
