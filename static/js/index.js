document.addEventListener('DOMContentLoaded', () => {

const chatContainer = document.getElementById('chat-container');
const userInput = document.getElementById('chat-input');
const toggleBtn = document.getElementById('toggle-btn');
const sidebar = document.getElementById('sidebar');
const enviarBtn = document.getElementById('send-btn');
enviarBtn.addEventListener('click', handleUserMessage);

// Função para adicionar mensagem do usuário à interface
function addUserMessage(message) {
    const userMessageDiv = document.createElement('div');
    userMessageDiv.className = 'message user-message';
    userMessageDiv.innerHTML = `<p>${message}</p>`;
    chatContainer.appendChild(userMessageDiv);
}

// Função para adicionar mensagem da IA à interface
function addBotMessage(message) {
    const botMessageDiv = document.createElement('div');
    botMessageDiv.className = 'message bot-message';
    botMessageDiv.innerHTML = message;
    chatContainer.appendChild(botMessageDiv);
}

// Função para lidar com a submissão da mensagem do usuário
function handleUserMessage(event) {
    if (event.key === 'Enter' || event.target.id === 'send-btn') {
        const pergunta = userInput.value;
        if (pergunta == '') {
            return
        }
        addUserMessage(pergunta);

        // Envia a pergunta para o servidor
        fetch('/gerar-resposta', {
            method: 'POST',
            headers: {
                 'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'pergunta=' + encodeURIComponent(pergunta)
        })
        .then(response => response.json())
        .then(data => {
            let resposta = data.resposta;
            console.log("Resposta recebida.")
            resposta = marked.parse(resposta)
            addBotMessage(resposta);
        })
        .catch(error => console.error('Erro ao enviar pergunta:', error));

        userInput.value = '';
    }
}

toggleBtn.addEventListener('click', () => {
    if (sidebar.style.width === '250px') {
        sidebar.style.width = '0';
        // content.style.marginLeft = '0';
    } else {
        sidebar.style.width = '250px';
        // content.style.marginLeft = '250px';
    }
});

userInput.addEventListener('keypress', handleUserMessage);

});

function handleCardClick(cardId) {
    // Lógica para lidar com o clique no card
    console.log("Card clicado:", cardId);
}

function deletar(){
    console.log("deletou")
}

function alterar(){
    console.log("alterou")
}
