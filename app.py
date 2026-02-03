import os
import psycopg2
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)
DATABASE_URL = os.environ.get("DATABASE_URL")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Lista de Pagamentos</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f9f9f9; }
        h2 { text-align: center; margin-top: 20px; }
        table { border-collapse: collapse; width: 95%; margin: 20px auto; background-color: #fff; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: center; }
        th { background-color: #4CAF50; color: white; }
        tr:nth-child(even) { background-color: #f2f2f2; }
        .approved { color: green; font-weight: bold; }
        .pending { color: orange; font-weight: bold; }
        button { padding: 5px 10px; margin: 0; }
    </style>
</head>
<body>
    <h2>Pagamentos</h2>
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>User ID</th>
                <th>Email</th>
                <th>Amount</th>
                <th>Status</th>
                <th>Created At</th>
                <th>Updated At</th>
                <th>Transaction ID</th>
                <th>Ação</th>
            </tr>
        </thead>
        <tbody>
            {% for row in rows %}
            <tr>
                <td>{{ row[0] }}</td>
                <td>{{ row[1] }}</td>
                <td>{{ row[2] }}</td>
                <td>{{ row[3] }}</td>
                <td class="{{ row[4] }}">{{ row[4] }}</td>
                <td>{{ row[5].strftime("%d/%m/%Y %H:%M") }}</td>
                <td>{{ row[6].strftime("%d/%m/%Y %H:%M") }}</td>
                <td>{{ row[7] }}</td>
                <td>
                    <form method="POST" action="/update_status">
                        <input type="hidden" name="id" value="{{ row[0] }}">
                        <select name="status">
                            <option value="pending" {% if row[4]=='pending' %}selected{% endif %}>pending</option>
                            <option value="approved" {% if row[4]=='approved' %}selected{% endif %}>approved</option>
                        </select>
                        <button type="submit">Salvar</button>
                    </form>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
"""

@app.route("/")
def listar_pagamentos():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT * FROM pagamentos;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return render_template_string(HTML_TEMPLATE, rows=rows)
    except Exception as e:
        return f"Erro: {str(e)}", 500

@app.route("/update_status", methods=["POST"])
def update_status():
    pagamento_id = request.form.get("id")
    status = request.form.get("status")
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("UPDATE pagamentos SET status=%s WHERE id=%s", (status, pagamento_id))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("listar_pagamentos"))
    except Exception as e:
        return f"Erro: {str(e)}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
