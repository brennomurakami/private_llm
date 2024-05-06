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
from models.conversa import Conversa

app = Flask(__name__)

# Configurações do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:p3o4s2t1@localhost/llm'
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

@app.route('/salvar-card', methods=['POST'])
def salvar_card():
    data = request.json
    nome_card = data.get('nome_card')

    # Crie um novo card no banco de dados
    novo_card = Conversa(nome_conversa=nome_card)
    db.session.add(novo_card)
    db.session.commit()

    # Retorne o ID do card na resposta
    return jsonify({'id_card': novo_card.idconversa}), 200

@app.route('/cards', methods=['GET'])
def get_cards():
    cards = Conversa.query.all()  # Consulta todos os cards do banco de dados
    print("cards")
    print(cards)
    cards_data = [{'idconversa': card.idconversa, 'nome_conversa': card.nome_conversa} for card in cards]  # Formata os dados dos cards
    return jsonify(cards_data)  # Retorna os dados dos cards como JSON

@app.route('/deletar-card', methods=['POST'])
def deletar_card():
    data = request.json
    card_id = data['card_id']

    # Remove o card do banco de dados
    print("id: ", card_id)
    card = Conversa.query.filter_by(idconversa=card_id).first()
    print("card encontrado:", card)
    if card:
        db.session.delete(card)
        db.session.commit()
        return 'Card excluído com sucesso do banco de dados.'
    else:
        return 'Card não encontrado no banco de dados.', 404

if __name__ == '__main__':
    app.run(debug=True)
