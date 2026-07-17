from flask import Flask, render_template, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy

from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

app = Flask(__name__)
app.secret_key = "segredo"
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Faça login para acessar esta página."

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Usuario(UserMixin, db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100), unique = True)
    senha = db.Column(db.String(255))

#UM USUARIO PODE TER VARIAS TAREFAS
    tarefas = db.relationship(
        "Tarefa",
        backref="usuario",
        lazy=True
    )

class Tarefa(db.Model):
    __tablename__ = "tarefas"

    id = db.Column(db.Integer, primary_key = True)
    materia_id = db.Column(
    db.Integer,
    db.ForeignKey("materias.id"))
    assunto = db.Column(db.String(100))
    horario = db.Column(db.String(50))
    dia = db.Column(db.String(50))
    descricao = db.Column(db.Text)

#CADA TAREFA PERTENCE A UM USUARIO
    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id")
    )

class Materia(db.Model):
    __tablename__ = "materias"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True)

    tarefas = db.relationship(
        "Tarefa",
        backref="materia",
        lazy=True
    )

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Usuario, int(user_id))

with app.app_context():
    db.create_all()

    if Materia.query.count() == 0:
        lista = [
            "Matemática",
            "Português",
            "História",
            "Geografia",
            "Biologia",
            "Química",
            "Física",
            "Inglês"
        ]

        for nome in lista:
            db.session.add(Materia(nome=nome))

        db.session.commit()


# HOME
@app.route("/")
@login_required
def home():

    usuario = current_user

    tarefas = Tarefa.query.filter_by(
        usuario_id=usuario.id
    ).all()

    return render_template(
        "index.html",
        usuario=usuario.nome,
        atividades=tarefas
    )
# BUSCAR
@app.route("/buscar")
@login_required
def buscar():

    usuario = current_user

    assunto = request.args.get("assunto", "")

    tarefas = Tarefa.query.filter(
    Tarefa.usuario_id == usuario.id,
    Tarefa.assunto.like(f"%{assunto}%")
    ).all()

    return render_template(
        "listar.html",
        tarefas=tarefas
    )

# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        senha = request.form["senha"]

        if not email or not senha:
            flash("Preencha todos os campos")
            return redirect("/login")

        usuario = Usuario.query.filter_by(
            email=email
        ).first()

        if usuario and check_password_hash(
            usuario.senha,
            senha
        ):
            login_user(usuario)
            return redirect("/")

        flash("Email ou senha inválidos")
        return redirect("/login")

    return render_template("login.html")

# CADASTRO
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    if request.method == "POST":

        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]
        confirmar = request.form["confirmar_senha"]

#VALIDAÇÃO NOVA
        if not nome or not email or not senha:
            flash("Preencha todos os campos")
            return redirect("/cadastro")

        if senha != confirmar:
            flash("Senhas diferentes")
            return redirect("/cadastro")
        
        usuario = Usuario.query.filter_by(
            email = email
        ).first()

        if usuario:
            flash("Usuário já existe")
            return redirect("/cadastro")
        
        senha_hash = generate_password_hash(senha)

        novo = Usuario(
            nome = nome,
            email = email,
            senha = senha_hash
        )

        db.session.add(novo)
        db.session.commit()

        login_user(novo)

        return redirect("/")

    return render_template("cadastro.html")

# CRIAR TAREFA
@app.route("/cronograma/criar", methods=["GET", "POST"])
@login_required
def criar_tarefa():

    if request.method == "POST":

        materia_id = request.form["materia"]
        assunto = request.form["assunto"]
        horario = request.form["horario"]
        dia = request.form["dia"]
        descricao = request.form["descricao"]

        usuario = current_user

        nova = Tarefa(
           materia_id = materia_id,
           assunto = assunto,
           horario = horario,
           dia = dia,
           descricao = descricao, 
           usuario_id = usuario.id
       )
        
        db.session.add(nova)
        db.session.commit()

        flash("Tarefa criada com sucesso!")
        return redirect("/")

    materias = Materia.query.all()

    return render_template( "criar.html", materias = materias)

# LISTAR
@app.route("/listar")
@login_required
def listar():

    usuario = current_user

    tarefas = Tarefa.query.filter_by(
        usuario_id = usuario.id
    ).all()

    return render_template("listar.html", tarefas=tarefas)

# EDITAR
@app.route("/cronograma/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):

    usuario = current_user

    tarefa = Tarefa.query.filter_by(
        id=id,
        usuario_id=usuario.id
    ).first()

    if not tarefa:
        flash("Tarefa não encontrada")
        return redirect("/listar")

    if request.method == "POST":

        materia_id = request.form["materia"]
        assunto = request.form["assunto"]
        horario = request.form["horario"]
        dia = request.form["dia"]
        descricao = request.form["descricao"]

        tarefa.materia_id = materia_id
        tarefa.assunto = assunto
        tarefa.horario = horario
        tarefa.dia = dia
        tarefa.descricao = descricao

        db.session.commit()

        return redirect("/listar")

    materias = Materia.query.all()

    return render_template(
        "editar.html",
        tarefa=tarefa,
        materias=materias
    )
# REMOVER
@app.route("/cronograma/remover/<int:id>")
@login_required
def remover(id):

    usuario = current_user

    tarefa = Tarefa.query.filter_by(
        id=id,
        usuario_id=usuario.id
    ).first()

    if not tarefa:
        flash("Tarefa não encontrada")
        return redirect("/listar")

    db.session.delete(tarefa)
    db.session.commit()

    return redirect("/listar")

# CRONOGRAMA
@app.route("/cronograma")
@login_required
def cronograma():

    usuario = current_user

    tarefas = Tarefa.query.filter_by(
    usuario_id = usuario.id
    ).all()

    return render_template("meucronograma.html", tarefas=tarefas)

# DASHBOARD
@app.route("/dashboard")
@login_required
def dashboard():

    usuario = current_user

    total = Tarefa.query.filter_by(
        usuario_id = usuario.id
    ).count()

    return render_template(
        "dashboard.html",
        total_tarefas=total
    )

# LOGOUT
@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect("/login")

# RODAR
if __name__ == "__main__":
    app.run(debug=True)