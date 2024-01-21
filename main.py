from flask import Flask, render_template, request
from flask_mail import Mail, Message
import re

app = Flask(__name__)

# Configuração para Flask-Mail
app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'raffasadol@live.com'
app.config['MAIL_PASSWORD'] = 'Miguel072017'

mail = Mail(app)

def validar_email(email):
    padrao = r'^[\w\.]+@[a-zA-Z\d\.]+\.(com|edu|gov|org)$'
    return re.match(padrao, email)



@app.route('/', methods=['GET', 'POST'])
def index_email():
    mensagem_email = None
    msg = None

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

                mensagem_email = 'E-mail enviado com sucesso!'
                print(f'\033[34m{msg.body}\033[m')
    
                mail.send(msg.body)  # Envia o e-mail
    
            else:
                None

        elif 'btn-orcamento' in request.form:
            # O botão "Enviar Orçamento" na seção de Orçamento foi clicado

            msg = Message('*', sender='Contato através do portfólio', recipients=['Raffasadol@gmail.com'])
            msg.body = f'Mensagem: {mensagem}\nPáginas: {qtde}\nJavaScript: {js}\nLayout: {layout}\nPrazo: {texto_prazo}\nEmail: {email}\n'

            mensagem_email = 'E-mail enviado com sucesso!'
            print(f'\033[34m{msg.body}\033[m')

            mail.send(msg.body)  # Envia o e-mail
    
    return render_template('index.html', mensagem_email=mensagem_email)


if __name__ == '__main__':
    app.run(debug=True)
