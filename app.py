import os
import psycopg2
from flask import Flask, render_template_string
from datetime import datetime

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
                <td>{{ row[5] | format_date }}</td>
                <td>{{ row[6] | format_date }}</td>
                <td>{{ row[7] }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
"""

app.jinja_env.filters['format_date'] = lambda s: datetime.strptime(s, "%a, %d %b %Y %H:%M:%S %Z").strftime("%d/%m/%Y %H:%M")

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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
