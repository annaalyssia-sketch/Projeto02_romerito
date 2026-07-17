from flask import Flask, render_template, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "segredo"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100), unique = True)
    senha = db.Column(db.String(100))

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
def home():

    if "email" not in session:
        return redirect("/login")

    usuario = Usuario.query.filter_by(
        email=session["email"]
    ).first()

    # Se o usuário não existir mais no banco,
    # limpa a sessão e volta para o login
    if usuario is None:
        session.clear()
        return redirect("/login")

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
def buscar():

    if "email" not in session:
        return redirect("/login")

    usuario = Usuario.query.filter_by(
    email=session["email"]
    ).first()

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
        email = email,
        senha = senha
    ).first()

        if usuario:
            session["email"] = email
            session["nome"] = usuario.nome
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

        novo = Usuario(
            nome = nome,
            email = email,
            senha = senha
        )

        db.session.add(novo)
        db.session.commit()

        session["nome"] = nome
        session["email"] = email

        return redirect("/")

    return render_template("cadastro.html")

# CRIAR TAREFA
@app.route("/cronograma/criar", methods=["GET", "POST"])
def criar_tarefa():

    if "email" not in session:
        return redirect("/login")

    if request.method == "POST":

        materia_id = request.form["materia"]
        assunto = request.form["assunto"]
        horario = request.form["horario"]
        dia = request.form["dia"]
        descricao = request.form["descricao"]

        usuario =Usuario.query.filter_by(
            email = session["email"]
        ).first()

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
def listar():

    if "email" not in session:
        return redirect("/login")

    usuario = Usuario.query.filter_by(
    email=session["email"]
    ).first()

    tarefas = Tarefa.query.filter_by(
        usuario_id = usuario.id
    ).all()

    return render_template("listar.html", tarefas=tarefas)

# EDITAR
@app.route("/cronograma/editar/<int:id>", methods=["GET", "POST"])
def editar(id):

    if "email" not in session:
        return redirect("/login")

    usuario = Usuario.query.filter_by(
    email=session["email"]
    ).first()

    tarefa = Tarefa.query.filter_by(
    id=id,
    usuario_id=usuario.id
    ).first()

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
def remover(id):

    if "email" not in session:
        return redirect("/login")

    usuario = Usuario.query.filter_by(
    email=session["email"]
    ).first()

    tarefa = Tarefa.query.filter_by(
    id=id,
    usuario_id=usuario.id
    ).first()

    db.session.delete(tarefa)
    db.session.commit()

    return redirect("/listar")

# CRONOGRAMA
@app.route("/cronograma")
def cronograma():

    if "email" not in session:
        return redirect("/login")

    usuario = Usuario.query.filter_by(
    email=session["email"]
    ).first()

    tarefas = Tarefa.query.filter_by(
    usuario_id = usuario.id
    ).all()

    return render_template("meucronograma.html", tarefas=tarefas)

# DASHBOARD
@app.route("/dashboard")
def dashboard():

    if "email" not in session:
        return redirect("/login")

    usuario = Usuario.query.filter_by(
        email = session["email"]
    ).first()

    total = Tarefa.query.filter_by(
        usuario_id = usuario.id
    ).count()

    return render_template(
        "dashboard.html",
        total_tarefas=total
    )

# LOGOUT
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")

# RODAR
if __name__ == "__main__":
    app.run(debug=True)