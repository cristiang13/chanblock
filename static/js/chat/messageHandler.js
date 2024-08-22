

document.addEventListener('DOMContentLoaded', function() {
    var sendButton = document.querySelector('.send-button');
    var messageInput = document.querySelector('.message-input');
    var coinName = document.querySelector(".coin_name");
    var messageList = document.querySelector('.message-list');
    var spinnerChat = document.querySelector('.spinner-chat');

    sendButton.addEventListener('click', function() {
        var message = messageInput.value.trim();
        var asset = coinName.value.trim()
        if (message) {
            addMessage('sent', message);
            sendButton.disabled = true;
            sendButton.style.display = 'none';
            spinnerChat.style.display = 'block';
            sendMessageToServer(message,asset);
            messageInput.value = '';
        }
    });

    function addMessage(type, message) {
        var li = document.createElement('li');
        li.classList.add(type);
        li.textContent = message;
        messageList.appendChild(li);
    }

    function sendMessageToServer(message, asset) {
        fetch('/asset/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')  // Asegúrate de manejar CSRF token si es necesario
            },
            body: JSON.stringify({ message: message, asset:asset })
        })
        .then(response => response.json())
        .then(data => {
            addMessage('received', data.reply); // Asume que la respuesta es un objeto JSON con una propiedad 'reply'
            sendButton.disabled = false;
            sendButton.style.display = 'block';
            spinnerChat.style.display = 'none';
        
        })
        .catch(error => {
            console.error('Error:', error);
            sendButton.disabled = false; // Habilita el botón de enviar
            sendButton.style.display = 'block';
            spinnerChat.style.display = 'none'; // Oculta el spinner
        });
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
