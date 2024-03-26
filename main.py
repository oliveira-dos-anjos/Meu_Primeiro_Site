from flask import Flask, render_template, request, session, redirect
from flask_mail import Mail, Message
import re
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'


# Obtendo o caminho absoluto para o arquivo Clientes.db na pasta 'data'
db_path = os.path.join(app.root_path, 'data', 'Clientes.db')

# Conexao com o banco de dados
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Criacao de tabela se nao existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Clientes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL,
        mensagem TEXT NOT NULL              
    )
''')

conn.commit()  # Salvar
conn.close()  # Fechar


# Configuração para Flask-Mail
app.config['MAIL_SERVER'] = 'sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 587  # Use a porta adequada (25, 465, 587, ou 2525)
app.config['MAIL_USERNAME'] = 'a09f28282721cf'
app.config['MAIL_PASSWORD'] = '3248403a8ce0e8'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = 'raffasadol@gmail.com'

mail = Mail(app)

def validar_email(email):
    padrao = r'^[\w\.-]+@[a-zA-Z\d\.-]+\.(com|edu|gov|org)$'
    return re.match(padrao, email) is not None

def Salvar_info(nome, email, mensagem):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Clientes (nome, email,mensagem)
        VALUES(?, ?, ?)
    ''', (nome, email,mensagem))
    conn.commit()  # Salvar
    conn.close()  # Fechar

@app.route('/submit_form', methods=['GET', 'POST'])
def submit_form():
    # Define uma variável de sessão indicando que a rolagem para a seção de orçamento deve ocorrer
    session['scroll_to_contato'] = True
    session['scroll_to_orcamento'] = True

    return redirect('/')


@app.route('/', methods=['GET', 'POST'])

def index_email():
    mensagem_email_contato = None
    mensagem_email_orcamento = None
    erro_contato = None
    erro_orcamento = None
    scroll_to_contato = False
    scroll_to_orcamento = False
    conn = None

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM Clientes')
        Clientes = cursor.fetchall()

        if request.method == 'POST':
            nome = request.form.get('nome', 'Não informado')
            email = request.form.get('email', 'Email Padrão')
            mensagem = request.form.get('mensagem', 'Solicitando orçamento')
            qtd = request.form.get('qtde')
            qtde = '1' if qtd == "" else qtd
            js = 'Sim' if 'JS' in request.form else 'Não'
            lay = request.form.get('layout', 'Não informado')
            layout = 'sim' if lay == 'on' else 'Não'
            prazo = request.form.get('prazo')
            texto_prazo = f'{prazo} semana' if prazo == '1' else f'{prazo} semanas'        

            if 'btn-contato' in request.form:
                if validar_email(email):
                    msg = Message('*', sender='Contato através do portfólio', recipients=['Raffasadol@gmail.com'])
                    msg.body = f'Nome: {nome}\nEmail: {email}\nMensagem: {mensagem}'

                    mensagem_email_contato = 'E-mail enviado com sucesso!'
                    
                    mail.send(msg)                    
                    Salvar_info(nome, email, mensagem)

                    submit_form()
                else:
                    raise ValueError("Email inválido.")

            elif 'btn-orcamento' in request.form:
                if validar_email(email):
                    msg = Message('*', sender='Contato através do portfólio', recipients=['Raffasadol@gmail.com'])
                    msg.body = f'Mensagem: {mensagem}\nPáginas: {qtde}\nJavaScript: {js}\nLayout: {layout}\nPrazo: {texto_prazo}\nEmail: {email}\n'

                    mensagem_email_orcamento  = 'E-mail enviado com sucesso!'

                    mail.send(msg)
                    Salvar_info(nome, email, mensagem)

                    submit_form()
                else:
                    raise ValueError('Email inválido.')

         # Verifica se a variável de sessão está definida
        scroll_to_contato = session.pop('scroll_to_contato', False)
        scroll_to_orcamento = session.pop('scroll_to_orcamento', False)

        return render_template('index.html', Clientes=Clientes, mensagem_email_contato=mensagem_email_contato, mensagem_email_orcamento=mensagem_email_orcamento, scroll_to_contato=scroll_to_contato, scroll_to_orcamento=scroll_to_orcamento)

    except Exception as e:
        if conn:
            conn.rollback()
        mensagem_erro = f"Erro: {str(e)}"
        if "btn-contato" in request.form:
            erro_contato = mensagem_erro
        elif "btn-orcamento" in request.form:
            erro_orcamento = mensagem_erro
        return render_template('index.html', erro_contato=erro_contato, erro_orcamento=erro_orcamento)


if __name__ == '__main__':
    app.run(debug=True)
