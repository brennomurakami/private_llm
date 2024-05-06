document.addEventListener('DOMContentLoaded', () => {

const chatContainer = document.getElementById('chat-container');
const userInput = document.getElementById('chat-input');
const toggleBtn = document.getElementById('toggle-btn');
const sidebar = document.getElementById('sidebar');
const enviarBtn = document.getElementById('send-btn');
enviarBtn.addEventListener('click', handleUserMessage);
const centralText = document.getElementById('central-content');

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
        centralText.style.display = 'none';
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
    if (sidebar.style.left === '0px') {
        sidebar.style.left = '-250px'
        toggleBtn.style.marginLeft = '0'
        toggleBtn.style.width = '40px'
        toggleBtn.textContent = 'chevron_right'
    } else {
        toggleBtn.textContent = 'chevron_left'
        toggleBtn.style.width = '525px'
        sidebar.style.left = '0px'
    }
});

userInput.addEventListener('keypress', handleUserMessage);

});

const chats = document.getElementById('chats');
let contador = 0;

function handleCardClick(cardId) {
    // Lógica para lidar com o clique no card
    console.log("Card clicado:", cardId);
}

function deletar(cardId){
    // Obtém o elemento pai do botão de delete, que é o card a ser removido
    var cardToRemove = cardId.parentNode.parentNode;
    
    // Obtém o elemento pai do card, que é o contêiner de chats
    var chats = cardToRemove.parentNode;
    
    // Remove o card do contêiner de chats
    chats.removeChild(cardToRemove);
}

function alterar(){
    console.log("alterou")
}

function criarCard() {
    contador++; // Incrementa o contador para gerar um novo ID único para o card
    const novoCard = document.createElement('div');
    novoCard.classList.add('card');
    novoCard.setAttribute('id', 'card' + contador); // Define o ID único para o novo card
    novoCard.innerHTML = `
        <p>Chat ${contador}</p>
        <div id="card-op">
            <span class="material-symbols-outlined" onclick="alterar()" id="edit">edit</span>
            <span class="material-symbols-outlined" onclick="deletar(this)" id="delete">delete</span>
        </div>
    `;
    chats.appendChild(novoCard);
}
