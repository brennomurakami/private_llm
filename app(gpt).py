from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key='sk-proj-6KVxQwSLaXo0bQm7cxTtT3BlbkFJEwYSLT2n88ePXgPAMrn9')

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
