from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv('API_KEY')

client = OpenAI(api_key = key)

assistant = client.beta.assistants.create(
  name="Teste",
  instructions="Você possui 3 perfis: veterinário, especialista em vendas e poeta. \
        Dessa forma ocê deve escolher 1 destes 3 perfis para elaborar a resposta com base no contexto da pergunta. \
        Por último, você deve responder as mensagens como se eu me chamasse Brenno Murakami",
  tools=[{"type": "code_interpreter"}],
  model="gpt-4-turbo",
)
