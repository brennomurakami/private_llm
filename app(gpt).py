from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import sys
import os

# Adiciona o diretório raiz do projeto ao caminho de pesquisa de módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importa e inicializa os modelos
from models.conta import db
from models.conversa import db
from models.historico_conversa import db

app = Flask(__name__)
client = OpenAI(api_key='sk-proj-6KVxQwSLaXo0bQm7cxTtT3BlbkFJEwYSLT2n88ePXgPAMrn9')

# Configurações do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:28072003xennox@localhost/llm'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco de dados com o aplicativo Flask
db.init_app(app)

# Cria todas as tabelas do banco de dados
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gerar-resposta', methods=['POST'])
def gerar_resposta():
    pergunta = request.form['pergunta']
    
    response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[
        {"role": "user", "content": pergunta}
    ])
    resposta = response.choices[0].message.content
    print(resposta)
    resposta = resposta
    return jsonify({'resposta': resposta})

if __name__ == '__main__':
    app.run(debug=True)
