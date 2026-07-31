document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.querySelector('#chat-box');
    const chatForm = document.querySelector('#chat-form');
    const messageInput = document.querySelector('#message-input');
    const sendButton = document.querySelector('#send-button');

    chatForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const message = messageInput.value.trim(); // 입력 메세지를 읽기.
        if (!message) return;

        appendMessage(message, 'user-message');
        messageInput.value = '';
        toggleForm(true);

        let aiMessageElement = null;
        
        // SSE 요청 -> EventSource(요청 url)
        // encodeURIComponent(str): URL 인코딩 처리.

        const eventSource = new EventSource(`/chat/stream/?message=${encodeURIComponent(message)}`);

        // EventSource에 Event Hander를 추가.
        // onmessage: 서버에서 답변이 올때마다 호출. 답변은 event.data 
        // onerror: 실행도중 Error가 발생하면 호출
        eventSource.onmessage = (event) => {
            if (event.data === '[DONE]') {
                eventSource.close();
                toggleForm(false);
                return;
            }

            if (!aiMessageElement) {
                aiMessageElement = appendMessage('', 'ai-message');
            }

            if (event.data.startsWith('[ERROR]')) {
                aiMessageElement.innerHTML += `<span style="color: red;">${event.data}</span>`;
                eventSource.close();
                toggleForm(false);
            } else {
                aiMessageElement.innerHTML += event.data;
            }
            chatBox.scrollTop = chatBox.scrollHeight;
        };

        eventSource.onerror = (err) => {
            console.error('EventSource 실패:', err);
            if (aiMessageElement) {
                aiMessageElement.innerHTML += `<span style="color: red;">[Error] 연결 실패</span>`;
            } else {
                appendMessage('<span style="color: red;">[Error] 연결 실패</span>', 'ai-message');
            }
            eventSource.close();
            toggleForm(false);
        };
    });

    function appendMessage(content, className) {
        const messageElement = document.createElement('div');
        messageElement.setAttribute("class", `message ${className}`);
        messageElement.innerHTML = content;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
        return messageElement;
    }

    function toggleForm(disabled) {
        messageInput.disabled = disabled;
        sendButton.disabled = disabled;
        if (!disabled) {
            messageInput.focus();
        }
    }
});
