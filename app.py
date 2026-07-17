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

class Tarefa(db.Model):
    __tablename__ = "tarefas"

    id = db.Column(db.Integer, primary_key = True)
    materia = db.Column(db.String(100))
    assunto = db.Column(db.String(100))
    horario = db.Column(db.String(50))
    dia = db.Column(db.String(50))
    descricao = db.Column(db.Text)
    email = db.Column(db.String(100))

with app.app_context():
    db.create_all()

# HOME
@app.route("/")
def home():
    if "email" not in session:
        return redirect("/login")

    tarefas = Tarefa.query.filter_by(
    email=session["email"]
).all()

    return render_template(
        "index.html",
        usuario=session["nome"],
        atividades=tarefas
    )

# BUSCAR
@app.route("/buscar")
def buscar():

    if "email" not in session:
        return redirect("/login")

    materia = request.args.get("materia", "")

    tarefas = Tarefa.query.filter(
    Tarefa.email == session["email"],
    Tarefa.materia.like(f"%{materia}%")
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

        materia = request.form["materia"]
        assunto = request.form["assunto"]
        horario = request.form["horario"]
        dia = request.form["dia"]
        descricao = request.form["descricao"]

        nova = Tarefa(
           materia = materia,
           assunto = assunto,
           horario = horario,
           dia = dia,
           descricao = descricao, 
           email = session["email"] 
       )
        
        db.session.add(nova)
        db.session.commit()

        flash("Tarefa criada com sucesso!")
        return redirect("/")

    return render_template("criar.html")

# LISTAR
@app.route("/listar")
def listar():

    if "email" not in session:
        return redirect("/login")

    tarefas = Tarefa.query.filter_by(
        email = session["email"]
    ).all()

    return render_template("listar.html", tarefas=tarefas)

# EDITAR
@app.route("/cronograma/editar/<int:id>", methods=["GET", "POST"])
def editar(id):

    if "email" not in session:
        return redirect("/login")

    tarefa = db.session.get(Tarefa, id)

    if request.method == "POST":
        materia = request.form["materia"]
        assunto = request.form["assunto"]
        horario = request.form["horario"]
        dia = request.form["dia"]
        descricao = request.form["descricao"]

        tarefa.materia = materia 
        tarefa.assunto = assunto 
        tarefa.horario = horario 
        tarefa.dia = dia 
        tarefa.descricao = descricao

        db.session.commit()

        return redirect("/listar")

    return render_template("editar.html", tarefa=tarefa)

# REMOVER
@app.route("/cronograma/remover/<int:id>")
def remover(id):

    if "email" not in session:
        return redirect("/login")

    tarefa = db.session.get(Tarefa, id)

    db.session.delete(tarefa)
    db.session.commit()

    return redirect("/listar")

# CRONOGRAMA
@app.route("/cronograma")
def cronograma():

    if "email" not in session:
        return redirect("/login")

    tarefas = Tarefa.query.filter_by(
    email=session["email"]
).all()

    return render_template("meucronograma.html", tarefas=tarefas)

# DASHBOARD
@app.route("/dashboard")
def dashboard():

    if "email" not in session:
        return redirect("/login")

    total = Tarefa.query.filter_by(
        email = session["email"]
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