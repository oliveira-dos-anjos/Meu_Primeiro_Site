from flask import Flask, render_template, request
from flask_mail import Mail, Message
import re
import sqlite3

app = Flask(__name__)

# Conexao com o banco de dados
conn = sqlite3.connect('Clientes.db')
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
app.config['MAIL_USERNAME'] = 'e958d96b2b17f3'
app.config['MAIL_PASSWORD'] = '0bfa1545e72e3a'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = 'raffasadol@gmail.com'

mail = Mail(app)

def validar_email(email):
    padrao = r'^[\w\.-]+@[a-zA-Z\d\.-]+\.(com|edu|gov|org)$'
    return re.match(padrao, email) is not None

def Salvar_info(nome, email, mensagem):
    conn = sqlite3.connect('Clientes.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Clientes (nome, email,mensagem)
        VALUES(?, ?, ?)
    ''', (nome, email,mensagem))
    conn.commit()  # Salvar
    conn.close()  # Fechar

@app.route('/', methods=['GET', 'POST'])

def index_email():
    mensagem_email = None
    msg = None

    mensagem_email_contato = None
    mensagem_email_orcamento = None

    conn = sqlite3.connect('Clientes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Clientes')  # all
    Clientes = cursor.fetchall()
    conn.close()
    

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
            # O botão "Enviar" na seção de Contato foi clicado

            if validar_email(email):

                # Configura a mensagem de e-mail

                msg = Message('*', sender='Contato através do portfólio', recipients=['Raffasadol@gmail.com'])
                msg.body = f'Nome: {nome}\nEmail: {email}\nMensagem: {mensagem}'

                mensagem_email_contato = 'E-mail enviado com sucesso!'
                print(f'\033[34m{msg.body}\033[m')
    
                try:
                    mail.send(msg)  # Envia o e-mail
                    Salvar_info(nome, email, mensagem)

                except Exception as e:
                    return f"Erro ao enviar o e-mail: {str(e)}"
            
        elif 'btn-orcamento' in request.form:
            # O botão "Enviar Orçamento" na seção de Orçamento foi clicado

            msg = Message('*', sender='Contato através do portfólio', recipients=['Raffasadol@gmail.com'])
            msg.body = f'Mensagem: {mensagem}\nPáginas: {qtde}\nJavaScript: {js}\nLayout: {layout}\nPrazo: {texto_prazo}\nEmail: {email}\n'

            mensagem_email_orcamento  = 'E-mail enviado com sucesso!'
            print(f'\033[34m{msg.body}\033[m')
            try:
                mail.send(msg)  # Envia o e-mail
                Salvar_info(nome, email, mensagem)

            except Exception as e:            
                return f"Erro ao enviar o e-mail: {str(e)}"
            

    return render_template('index.html', Clientes=Clientes, mensagem_email_contato=mensagem_email_contato, mensagem_email_orcamento=mensagem_email_orcamento)


if __name__ == '__main__':
    app.run(debug=True)

