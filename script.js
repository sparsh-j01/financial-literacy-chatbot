const chatMessages = document.getElementById('chat-messages');
const messageInput = document.getElementById('message-input');
const teluguToggle = document.getElementById('telugu-toggle');
const loadingIndicator = document.getElementById('loading');

function addMessage(text, isUser) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    messageDiv.textContent = text;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;

    // Add language tag if Telugu is selected
    const finalMessage = teluguToggle.checked ? message + " #te" : message;

    addMessage(message, true);
    messageInput.value = '';
    loadingIndicator.style.display = 'block';

    try {
        const response = await fetch('http://localhost:5000/webhook', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: `Body=${encodeURIComponent(finalMessage)}`
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        if (data.response === "Rate limit exceeded. Please wait a minute before trying again.") {
            addMessage('Rate limit exceeded. Please wait a minute before trying again.', false);
        } else {
            addMessage(data.response, false);
        }
    } catch (error) {
        if (error.message.includes('HTTP error! status: 429')) {
            addMessage('Rate limit exceeded. Please wait a minute before trying again.', false);
        } else {
            addMessage('Error: Could not connect to the server. Please make sure the backend is running.', false);
        }
        console.error('Error:', error);
    } finally {
        loadingIndicator.style.display = 'none';
    }
}

messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Add placeholder text based on language selection
teluguToggle.addEventListener('change', (e) => {
    messageInput.placeholder = e.target.checked ?
        "మీ సందేశాన్ని టైప్ చేయండి..." :
        "Type your message...";
});
