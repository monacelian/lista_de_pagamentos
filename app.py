import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, render_template_string

app = Flask(__name__)

# Pega a URL do banco da variável de ambiente (seguro, sem expor senha)
DATABASE_URL = os.environ.get("DATABASE_URL")

# Template HTML simples
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Painel do Banco</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; background: #f4f4f9; }
        table { border-collapse: collapse; width: 100%; margin-top: 20px; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
        th { background-color: #0077cc; color: white; }
        tr:nth-child(even) { background-color: #e9e9e9; }
    </style>
</head>
<body>
    <h1>Banco de Dados</h1>
    {% if error %}
        <p style="color:red;">Erro: {{ error }}</p>
    {% else %}
        <table>
            <tr>
                {% for col in columns %}
                    <th>{{ col }}</th>
                {% endfor %}
            </tr>
            {% for row in rows %}
                <tr>
                {% for col in columns %}
                    <td>{{ row[col] }}</td>
                {% endfor %}
                </tr>
            {% endfor %}
        </table>
    {% endif %}
</body>
</html>
"""

@app.route("/")
def index():
    if not DATABASE_URL:
        return render_template_string(HTML_TEMPLATE, error="DATABASE_URL não definida", rows=[], columns=[])
    
    try:
        # Conecta no banco usando SSL
        conn = psycopg2.connect(DATABASE_URL, sslmode="require", cursor_factory=RealDictCursor)
        cur = conn.cursor()
        
        # Troque 'sua_tabela' pelo nome da tabela que quer mostrar
        cur.execute("SELECT * FROM public.sua_tabela LIMIT 50")
        rows = cur.fetchall()
        columns = rows[0].keys() if rows else []

        cur.close()
        conn.close()

        return render_template_string(HTML_TEMPLATE, rows=rows, columns=columns, error=None)
    
    except Exception as e:
        return render_template_string(HTML_TEMPLATE, error=str(e), rows=[], columns=[])

if __name__ == "__main__":
    # Usa a porta do Railway, ou 3000 por padrão
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
