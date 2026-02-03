import os
import psycopg2
from flask import Flask

app = Flask(__name__)

# Pegando a URL do banco das variáveis de ambiente
DATABASE_URL = os.environ.get("DATABASE_URL")

@app.route("/")
def index():
    try:
        # Conectando no PostgreSQL
        conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        cur = conn.cursor()

        # Troque 'sua_tabela' pelo nome da tabela que você quer mostrar
        cur.execute("SELECT * FROM public.sua_tabela LIMIT 50")
        rows = cur.fetchall()
        cols = [desc[0] for desc in cur.description]

        cur.close()
        conn.close()

        # Criando uma tabela HTML simples
        html = "<h1>Banco de Dados</h1><table border=1>"
        html += "<tr>" + "".join(f"<th>{c}</th>" for c in cols) + "</tr>"

        for r in rows:
            html += "<tr>" + "".join(f"<td>{v}</td>" for v in r) + "</tr>"

        html += "</table>"
        return html

    except Exception as e:
        return f"<h1>Erro ao conectar no banco:</h1><p>{e}</p>"

if __name__ == "__main__":
    # Rodando o app no Railway
    app.run(host="0.0.0.0", port=3000)
