from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import sys
import os
from dotenv import load_dotenv

# Adiciona o diretório raiz do projeto ao caminho de pesquisa de módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

key = os.getenv('API_KEY')
database_url = os.getenv('DATABASE_URL')

# Importa e inicializa os modelos
from models.conta import db
from models.conversa import db
from models.historico_conversa import db
from models.conversa import Conversa
from models.historico_conversa import HistoricoConversa

app = Flask(__name__)
client = OpenAI(api_key = key)

assistant = client.beta.assistants.create(
  name="Teste",
  instructions="Você possui 3 perfis: veterinário, especialista em vendas e poeta. \
        Dessa forma ocê deve escolher 1 destes 3 perfis para elaborar a resposta com base no contexto da pergunta. \
        Por último, você deve responder as mensagens como se eu me chamasse Brenno Murakami",
  tools=[{"type": "code_interpreter"}],
  model="gpt-4-turbo",
)

# Configurações do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
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
    thread = request.form['thread']
    print('thread recebida:', thread)
    
    message = client.beta.threads.messages.create(
    thread_id=thread,
    role="user",
    content=pergunta
    )

    run = client.beta.threads.runs.create_and_poll(
    thread_id=thread,
    assistant_id=assistant.id
    )

    if run.status == 'completed': 
        messages = client.beta.threads.messages.list(
        thread_id=thread
        )
        # print(messages)
    else:
        print(run.status)

    resposta = messages.data[0].content[0].text.value
    print(resposta)

    return jsonify({'resposta': resposta})

@app.route('/salvar-card', methods=['POST'])
def salvar_card():
    data = request.json
    nome_card = data.get('nome_card')
    thread = client.beta.threads.create()
    # Crie um novo card no banco de dados
    novo_card = Conversa(nome_conversa = nome_card, thread = thread.id)
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
    
@app.route('/get-thread/<card_id>', methods=['GET'])
def get_thread(card_id):
    card = Conversa.query.filter_by(idconversa=card_id).first()
    if card:
        return jsonify({'thread': card.thread}), 200
    else:
        return 'Card não encontrado no banco de dados.', 404
    
@app.route('/salvar-pergunta', methods=['POST'])
def salvar_pergunta():
    data = request.json
    pergunta = data['pergunta']
    idconversa = data['idconversa']

    # Crie um novo registro na tabela historico_conversa
    nova_pergunta = HistoricoConversa(pergunta=pergunta, idconversa=idconversa)
    db.session.add(nova_pergunta)
    db.session.commit()

    return 'Pergunta salva com sucesso no banco de dados.', 200

@app.route('/salvar-resposta', methods=['POST'])
def salvar_resposta():
    data = request.json
    resposta = data['resposta']
    idconversa = data['idconversa']

    # Crie um novo registro na tabela historico_conversa para a resposta
    nova_resposta = HistoricoConversa(resposta=resposta, idconversa=idconversa)
    db.session.add(nova_resposta)
    db.session.commit()

    return 'Resposta salva com sucesso no banco de dados.', 200

@app.route('/mensagens/<card_id>', methods=['GET'])
def get_mensagens(card_id):
    historico = HistoricoConversa.query.filter_by(idconversa=card_id).order_by(HistoricoConversa.idhistorico).all()
     # Lista para armazenar as mensagens
    mensagens = []
    # Percorre cada elemento do histórico
    for mensagem in historico:
        # Verifica se é uma pergunta ou resposta e adiciona à lista de mensagens
        if mensagem.pergunta:
            mensagens.append({'tipo': 'pergunta', 'conteudo': mensagem.pergunta})
        elif mensagem.resposta:
            mensagens.append({'tipo': 'resposta', 'conteudo': mensagem.resposta})
    return jsonify(mensagens), 200


if __name__ == '__main__':
    app.run(debug=True)
