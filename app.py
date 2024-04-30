from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

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
