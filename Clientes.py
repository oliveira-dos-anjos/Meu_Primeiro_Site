from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Conexao com o banco de dados
conn = sqlite3.connect('Clientes.db')
cursor = conn.cursor()


@app.route('/')
def index():
    conn = sqlite3.connect('Clientes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Clientes')  # all
    Clientes = cursor.fetchall()
    conn.close()
    return render_template('Clientes.html', Clientes=Clientes)

if __name__ == "__main__":
    app.run(debug=True)
