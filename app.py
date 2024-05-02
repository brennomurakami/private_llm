from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import sys
import os

# Adiciona o diretório raiz do projeto ao caminho de pesquisa de módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importa e inicializa os modelos
from models.conta import db
from models.conversa import db
from models.historico_conversa import db

app = Flask(__name__)

# Configurações do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:28072003xennox@localhost/llm'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco de dados com o aplicativo Flask
db.init_app(app)

# Cria todas as tabelas do banco de dados
with app.app_context():
    db.create_all()

genai.configure(api_key="AIzaSyBtEoIS8axNc2dqpVMNAy7Dap2XYoAwWUk")
model = genai.GenerativeModel("gemini-pro")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gerar-resposta', methods=['POST'])
def gerar_resposta():
    pergunta = request.form['pergunta']
    response = model.generate_content(pergunta)
    resposta = response.text
    return jsonify({'resposta': resposta})

if __name__ == '__main__':
    app.run(debug=True)
