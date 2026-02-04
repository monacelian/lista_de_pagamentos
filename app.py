import os

import psycopg2
from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)

# chave de sessão (pode ser qualquer texto)
app.secret_key = os.environ.get("SECRET_KEY", "segredo123")

DATABASE_URL = os.environ.get("DATABASE_URL")
ADMIN_USER = os.environ.get("ADMIN_USER")
ADMIN_PASS = os.environ.get("ADMIN_PASS")


# ---------- HTML LOGIN ----------
LOGIN_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
    <style>
        body { font-family: Arial; background: #f2f2f2; }
        .box {
            width: 300px; margin: 100px auto; padding: 20px;
            background: white; border-radius: 8px; text-align: center;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        input { width: 90%; padding: 8px; margin: 8px 0; }
        button { padding: 8px 15px; background: #4CAF50; color: white; border: none; }
        .erro { color: red; }
    </style>
</head>
<body>
    <div class="box">
        <h3>Login</h3>
        {% if erro %}<p class="erro">{{ erro }}</p>{% endif %}
        <form method="POST">
            <input name="user" placeholder="Usuário"><br>
            <input name="pass" type="password" placeholder="Senha"><br>
            <button type="submit">Entrar</button>
        </form>
    </div>
</body>
</html>
"""


# ---------- HTML TABELA ----------
TABLE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Pagamentos</title>
    <style>
        body { font-family: Arial; background: #f9f9f9; }
        h2 { text-align: center; }
        table { border-collapse: collapse; width: 95%; margin: auto; background: white; }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: center; }
        th { background: #4CAF50; color: white; }
        tr:nth-child(even) { background: #f2f2f2; }
        .approved { color: green; font-weight: bold; }
        .pending { color: orange; font-weight: bold; }
        .top { text-align: right; margin: 10px; }
        a { text-decoration: none; }
    </style>
</head>
<body>

<div class="top">
    <a href="/logout">Sair</a>
</div>

<h2>Lista de Pagamentos</h2>

<table>
<tr>
<th>ID</th>
<th>User</th>
<th>Email</th>
<th>Valor</th>
<th>Status</th>
<th>Criado</th>
<th>Atualizado</th>
<th>Tx</th>
<th>Ação</th>
</tr>

{% for r in rows %}
<tr>
<td>{{ r[0] }}</td>
<td>{{ r[1] }}</td>
<td>{{ r[2] }}</td>
<td>{{ r[3] }}</td>
<td class="{{ r[4] }}">{{ r[4] }}</td>
<td>{{ r[5].strftime("%d/%m %H:%M") }}</td>
<td>{{ r[6].strftime("%d/%m %H:%M") }}</td>
<td>{{ r[7] }}</td>
<td>
<form method="POST" action="/update">
<input type="hidden" name="id" value="{{ r[0] }}">
<select name="status">
<option value="pending" {% if r[4]=='pending' %}selected{% endif %}>pending</option>
<option value="approved" {% if r[4]=='approved' %}selected{% endif %}>approved</option>
</select>
<button>Salvar</button>
</form>
</td>
</tr>
{% endfor %}
</table>

</body>
</html>
"""


# ---------- LOGIN ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    erro = None
    if request.method == "POST":
        if request.form["user"] == ADMIN_USER and request.form["pass"] == ADMIN_PASS:
            session["logado"] = True
            return redirect("/")
        else:
            erro = "Usuário ou senha inválidos"
    return render_template_string(LOGIN_HTML, erro=erro)


# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ---------- LISTAR ----------
@app.route("/")
def home():
    if not session.get("logado"):
        return redirect("/login")

    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT * FROM pagamentos ORDER BY id DESC;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return render_template_string(TABLE_HTML, rows=rows)


# ---------- UPDATE ----------
@app.route("/update", methods=["POST"])
def update():
    if not session.get("logado"):
        return redirect("/login")

    pid = request.form["id"]
    status = request.form["status"]

    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("UPDATE pagamentos SET status=%s WHERE id=%s", (status, pid))
    conn.commit()
    cur.close()
    conn.close()

    return redirect("/")


# ---------- RUN ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
