document.addEventListener('DOMContentLoaded', function() {
    const chatBody = document.getElementById('chat-body');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const suggestionChips = document.querySelectorAll('.chip');
    const serverStatus = document.getElementById('server-status');
    
    // API endpoint - make sure this matches your server
    const API_URL = 'http://localhost:5000/api';
    let isServerConnected = false;

    // Function to update server status display
    function updateServerStatus(status) {
        serverStatus.className = 'server-status';
        
        if (status === 'connected') {
            serverStatus.textContent = 'Connected to server';
            serverStatus.classList.add('connected');
            isServerConnected = true;
            userInput.disabled = false;
            sendBtn.disabled = false;
        } else if (status === 'disconnected') {
            serverStatus.textContent = 'Server disconnected. Please restart the Flask server.';
            serverStatus.classList.add('disconnected');
            isServerConnected = false;
            userInput.disabled = true;
            sendBtn.disabled = true;
        } else if (status === 'connecting') {
            serverStatus.textContent = 'Connecting to server...';
            serverStatus.classList.add('connecting');
            isServerConnected = false;
        }
    }

    // Check server status
    async function checkServerStatus() {
        updateServerStatus('connecting');
        
        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 5000);
            
            const response = await fetch('http://localhost:5000/', {
                signal: controller.signal
            });
            
            clearTimeout(timeoutId);
            
            if (response.ok) {
                updateServerStatus('connected');
                return true;
            } else {
                updateServerStatus('disconnected');
                return false;
            }
        } catch (error) {
            console.error('Server connection error:', error);
            updateServerStatus('disconnected');
            
            // Show error in chat
            addMessage('Server is not running. Please start the Flask server with "python app.py" and refresh this page.', false);
            return false;
        }
    }

    // Function to add a message to the chat
    function addMessage(message, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(isUser ? 'user-message' : 'bot-message');

        const messageContent = document.createElement('div');
        messageContent.classList.add('message-content');
        
        // Handle messages with line breaks
        if (message.includes('\n')) {
            message.split('\n').forEach(line => {
                if (line.trim() !== '') {
                    const p = document.createElement('p');
                    p.textContent = line;
                    messageContent.appendChild(p);
                }
            });
        } else {
            messageContent.textContent = message;
        }

        messageDiv.appendChild(messageContent);
        chatBody.appendChild(messageDiv);
        
        // Scroll to the bottom of the chat
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    // Function to send message to the backend and get response
    async function sendMessage(message) {
        if (!isServerConnected) {
            const isConnected = await checkServerStatus();
            if (!isConnected) {
                return;
            }
        }
        
        // Show loading indicator
        const loadingDiv = document.createElement('div');
        loadingDiv.classList.add('message', 'bot-message');
        
        const loadingContent = document.createElement('div');
        loadingContent.classList.add('message-content');
        loadingContent.textContent = 'Typing...';
        
        loadingDiv.appendChild(loadingContent);
        chatBody.appendChild(loadingDiv);
        chatBody.scrollTop = chatBody.scrollHeight;

        try {
            // Check if server is reachable first with a timeout
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 5000);
            
            // Call the backend API
            const response = await fetch(`${API_URL}/message`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message }),
                signal: controller.signal
            });
            
            clearTimeout(timeoutId);
            
            if (!response.ok) {
                throw new Error(`Server responded with status: ${response.status}`);
            }

            const data = await response.json();
            
            // Remove loading indicator
            chatBody.removeChild(loadingDiv);
            
            // Add bot response to chat
            addMessage(data.response, false);
            
        } catch (error) {
            console.error('Error sending message:', error);
            // Remove loading indicator
            chatBody.removeChild(loadingDiv);
            
            // Show a more specific error message
            if (error.name === 'AbortError') {
                addMessage('Request timed out. The server may not be running or is unreachable.', false);
                updateServerStatus('disconnected');
            } else if (error.message.includes('Failed to fetch')) {
                addMessage('Unable to connect to the server. Please make sure the Flask server is running at http://localhost:5000', false);
                updateServerStatus('disconnected');
            } else {
                addMessage(`Error: ${error.message}. Please check the server console for more details.`, false);
            }
        }
    }

    // Function to load place suggestions from backend
    async function loadPlaceSuggestions() {
        if (!isServerConnected) {
            return;
        }
        
        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 5000);
            
            const response = await fetch(`${API_URL}/places`, {
                signal: controller.signal
            });
            
            clearTimeout(timeoutId);
            
            if (!response.ok) {
                throw new Error(`Server responded with status: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Would be used for autocomplete in a more complex implementation
            console.log("Available places:", data.places);
        } catch (error) {
            console.error('Error loading place suggestions:', error);
            // We don't show this error to the user since it's not critical for the UI
        }
    }

    // Event listener for send button
    sendBtn.addEventListener('click', function() {
        if (!isServerConnected) {
            checkServerStatus();
            return;
        }
        
        const message = userInput.value.trim();
        if (message) {
            addMessage(message, true);
            userInput.value = '';
            sendMessage(message);
        }
    });

    // Event listener for Enter key
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            if (!isServerConnected) {
                checkServerStatus();
                return;
            }
            
            const message = userInput.value.trim();
            if (message) {
                addMessage(message, true);
                userInput.value = '';
                sendMessage(message);
            }
        }
    });

    // Event listeners for suggestion chips
    suggestionChips.forEach(chip => {
        chip.addEventListener('click', function() {
            if (!isServerConnected) {
                checkServerStatus();
                return;
            }
            
            const message = this.textContent;
            addMessage(message, true);
            sendMessage(message);
        });
    });

    // Check server status on page load
    checkServerStatus().then(isConnected => {
        if (isConnected) {
            // Load place suggestions when server is available
            loadPlaceSuggestions();
        }
    });
}); 