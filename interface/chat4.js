document.getElementById('send-button').addEventListener('click', function() {
    var input = document.getElementById('chat-input');
    var message = input.value.trim();

    if (message) {
        addToChatWindow(message, "my-message", "user-avatar-url.png");
        input.value = '';

        apiCall(message, function(response) {
            displayTypingIndicator();
            let delay = displayResponseInRealTime(response.traces);

            setTimeout(() => {
                addToChatWindow(response.reply, "bot-message", "bot-avatar-url.png");
            }, delay - 2000)

        });
    }
});

function addToChatWindow(text, className, avatarUrl) {
    var chatWindow = document.getElementById('chat-window');
    var messageDiv = document.createElement('div');
    messageDiv.classList.add("message", className);

    var avatar = document.createElement('img');
    avatar.src = avatarUrl;
    avatar.classList.add("avatar");

    var messageText = document.createElement('div');
    messageText.classList.add("message-text");
    messageText.textContent = text;

    if (className === "my-message") {
        messageDiv.appendChild(messageText);
        messageDiv.appendChild(avatar);
    } else {
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(messageText);
    }

    chatWindow.appendChild(messageDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight; // Auto-scroll to latest message
}

function addToTraceWindow(text, className, avatarUrl) {
    var traceWindow = document.getElementById('trace-window');
    var messageDiv = document.createElement('div');
    messageDiv.classList.add("message", className);

    var avatar = document.createElement('img');
    avatar.src = avatarUrl;
    avatar.classList.add("avatar");

    var messageText = document.createElement('div');
    messageText.classList.add("message-text");
    messageText.innerHTML = text;
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(messageText);

    traceWindow.appendChild(messageDiv);
    traceWindow.scrollTop = traceWindow.scrollHeight; // Auto-scroll to latest message
}

function displayTypingIndicator() {
    // Add a 'thinking...' message or similar indicator
    addToTraceWindow("...", "bot-message", "thought-tracer.png");
}

function displayResponseInRealTime(response) {
    const lines = response.split('\n');
    let delay = 0;
    const delayIncrement = 2000; // Adjust as needed

    lines.forEach((line, index) => {
        setTimeout(() => {
            if (index === 0) {
                removeTypingIndicator(); // Remove the indicator before displaying the first line
            } 
            addToTraceWindow(formatLine(line), "bot-message", "thought-tracer.png");
            setTimeout(()=>{
                displayTypingIndicator()
            },500);
            setTimeout(() => {
                removeTypingIndicator()
            }, 1500)
        }, delay);
        delay += delayIncrement;
        
    });
    return delay;
}

function removeTypingIndicator() {
    const chatWindow = document.getElementById('trace-window');
    if (chatWindow.lastChild && chatWindow.lastChild.textContent === "...") {
        chatWindow.removeChild(chatWindow.lastChild);
    }
}

function formatLine(line) {
    return line.replace(/(Thought:|Action:|Observation:)/g, "<span class='highlight'>$1</span>");
}

function apiCall(message, callback) {
    fetch('http://localhost:5001/message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message }),
    })
    .then(response => response.json())
    .then(data => {
        setTimeout(function() {
            callback(data);

            console.log("TRACES :",data.traces.split('\n'));
        }, 1000);
        
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
