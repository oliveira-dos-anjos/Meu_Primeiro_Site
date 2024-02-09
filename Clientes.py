from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)


# Obtendo o caminho absoluto para o arquivo Clientes.db na pasta 'data'
db_path = os.path.join(app.root_path, 'data', 'Clientes.db')


@app.route('/')
def index():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Clientes')  # all
    Clientes = cursor.fetchall()
    conn.close()
    return render_template('Clientes.html', Clientes=Clientes)

if __name__ == "__main__":
    app.run(debug=True)
