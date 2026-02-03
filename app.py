import os
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

# Pega a variável do Railway
DATABASE_URL = os.environ.get("DATABASE_URL")

@app.route("/")
def listar_pagamentos():
    try:
        # Conecta no banco
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        # Pega todos os registros da tabela correta
        cur.execute("SELECT * FROM pagamentos;")
        rows = cur.fetchall()

        # Fecha conexão
        cur.close()
        conn.close()

        # Retorna como JSON
        return jsonify(rows)

    except Exception as e:
        return {"erro": str(e)}, 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
