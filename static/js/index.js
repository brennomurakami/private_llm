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

const themeBtn = document.getElementById('theme-btn');
const chats = document.getElementById('chats');
const body = document.querySelector('body');
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
    let nomeCard = 'Novo chat';
    const novoCard = document.createElement('div');
    novoCard.classList.add('card');
    novoCard.setAttribute('id', 'card' + contador); // Define o ID único para o novo card
    novoCard.innerHTML = `
        <p>${nomeCard}</p>
        <div id="card-op">
            <span class="material-symbols-outlined" onclick="alterar()" id="edit">edit</span>
            <span class="material-symbols-outlined" onclick="deletar(this)" id="delete">delete</span>
        </div>
    `;
    chats.appendChild(novoCard);

     // Envia o ID do card para o servidor Flask
     fetch('/salvar-card', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({nome_card: nomeCard })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Erro ao salvar card no servidor.');
        }
        console.log('ID do card enviado com sucesso para o servidor.');
    })
    .catch(error => {
        console.error('Erro ao enviar ID do card para o servidor:', error);
    });
}

function carregarCards() {
    fetch('/cards')
        .then(response => response.json())
        .then(cards => {
            // Para cada card retornado, crie um novo elemento de card no DOM
            cards.forEach(card => {
                const novoCard = document.createElement('div');
                novoCard.classList.add('card');
                novoCard.setAttribute('id', 'card' + card.idconversa); // Define o ID do card
                novoCard.innerHTML = `
                    <p>${card.nome_conversa}</p>
                    <div id="card-op">
                        <span class="material-symbols-outlined" onclick="alterar()" id="edit">edit</span>
                        <span class="material-symbols-outlined" onclick="deletar(this)" id="delete">delete</span>
                    </div>
                `;
                chats.appendChild(novoCard);  // Adiciona o novo card ao contêiner de chats
            });
        })
        .catch(error => {
            console.error('Erro ao carregar cards do servidor:', error);
        });
}

document.addEventListener('DOMContentLoaded', carregarCards);

function toggleTheme() {
    // Verifica se a classe 'light-mode' está presente no body
    var isLightMode = body.classList.contains('light-mode');

    // Se estiver no modo claro, alterna para o modo escuro; caso contrário, alterna para o modo claro
    if (isLightMode) {
        body.classList.remove('light-mode');
        // Adicione a classe 'dark-mode' para ativar o modo escuro
        body.classList.add('dark-mode');
        themeBtn.textContent = 'light_mode'
    } else {
        // Remove a classe 'dark-mode' para desativar o modo escuro
        body.classList.remove('dark-mode');
        // Adicione a classe 'light-mode' para ativar o modo claro
        body.classList.add('light-mode');
        themeBtn.textContent = 'dark_mode'
    }
}
