from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "segredo"

# BANCO
def conectar():
    return sqlite3.connect("database.db")

# CRIAR TABELAS
conn = conectar()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    email TEXT,
    senha TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS tarefas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    materia TEXT,
    assunto TEXT,
    horario TEXT,
    descricao TEXT,
    data TEXT,
    email TEXT
)
""")

conn.commit()
conn.close()

# HOME
@app.route("/")
def home():
    if "email" not in session:
        return redirect("/login")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM tarefas WHERE email = ?",
        (session["email"],)
    )

    tarefas = cursor.fetchall()

    conn.close()

    return render_template(
        "index.html",
        usuario=session["nome"],
        atividades=tarefas
    )

# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        email = request.form["email"]
        senha = request.form["senha"]

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM usuarios WHERE email = ? AND senha = ?",
            (email, senha)
        )

        usuario = cursor.fetchone()

        conn.close()

        if usuario:
            session["email"] = email
            session["nome"] = usuario[1]

            return redirect("/")

        return "Login inválido"

    return render_template("login.html")

# CADASTRO
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    if request.method == "POST":

        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]
        confirmar = request.form["confirmar_senha"]

        if senha != confirmar:
            return "Senhas diferentes"

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM usuarios WHERE email = ?",
            (email,)
        )

        usuario = cursor.fetchone()

        if usuario:
            conn.close()
            return "Usuário já existe"

        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
            (nome, email, senha)
        )

        conn.commit()
        conn.close()

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
        descricao = request.form["descricao"]
        data = request.form["data"]

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO tarefas
        (materia, assunto, horario, descricao, data, email)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            materia,
            assunto,
            horario,
            descricao,
            data,
            session["email"]
        ))

        conn.commit()
        conn.close()

        return redirect("/cronograma")

    return render_template("criar.html")

# LISTAR
@app.route("/listar")
def listar():

    if "email" not in session:
        return redirect("/login")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM tarefas WHERE email = ?",
        (session["email"],)
    )

    tarefas = cursor.fetchall()

    conn.close()

    return render_template("listar.html", tarefas=tarefas)

# EDITAR
@app.route("/cronograma/editar/<int:id>", methods=["GET", "POST"])
def editar(id):

    if "email" not in session:
        return redirect("/login")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM tarefas WHERE id = ?",
        (id,)
    )

    tarefa = cursor.fetchone()

    if request.method == "POST":

        materia = request.form["materia"]
        assunto = request.form["assunto"]
        horario = request.form["horario"]
        descricao = request.form["descricao"]
        data = request.form["data"]

        cursor.execute("""
        UPDATE tarefas
        SET materia = ?, assunto = ?, horario = ?,
        descricao = ?, data = ?
        WHERE id = ?
        """, (
            materia,
            assunto,
            horario,
            descricao,
            data,
            id
        ))

        conn.commit()
        conn.close()

        return redirect("/listar")

    conn.close()

    return render_template("editar.html", tarefa=tarefa)

# REMOVER
@app.route("/cronograma/remover/<int:id>")
def remover(id):

    if "email" not in session:
        return redirect("/login")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM tarefas WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/listar")

# CRONOGRAMA
@app.route("/cronograma")
def cronograma():

    if "email" not in session:
        return redirect("/login")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM tarefas WHERE email = ?",
        (session["email"],)
    )

    tarefas = cursor.fetchall()

    conn.close()

    return render_template("meucronograma.html", tarefas=tarefas)

# DASHBOARD
@app.route("/dashboard")
def dashboard():

    if "email" not in session:
        return redirect("/login")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM tarefas WHERE email = ?",
        (session["email"],)
    )

    total = cursor.fetchone()[0]

    conn.close()

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