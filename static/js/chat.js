// 简化版聊天功能
let currentStudentId = '';
let currentStudentName = '';
let isTyping = false;

// 初始化聊天功能
function initializeChat(studentId, studentName) {
    currentStudentId = studentId;
    currentStudentName = studentName;
    
    console.log(`Chat initialized for ${studentName} (${studentId})`);
    
    // 绑定事件
    const sendBtn = document.getElementById('send-btn');
    const clearBtn = document.getElementById('clear-btn');
    const messageInput = document.getElementById('message-input');
    
    if (sendBtn) {
        sendBtn.addEventListener('click', sendMessage);
    }
    
    if (clearBtn) {
        clearBtn.addEventListener('click', clearChat);
    }
    
    if (messageInput) {
        messageInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
        
        messageInput.addEventListener('input', updateSendButton);
    }
    
    // 场景控制
    const sceneDropdown = document.getElementById('scene-dropdown');
    if (sceneDropdown) {
        sceneDropdown.addEventListener('change', handleSceneChange);
    }
    
    updateSendButton();
    console.log('Chat interface ready');
}

// 发送消息
async function sendMessage() {
    const messageInput = document.getElementById('message-input');
    const message = messageInput.value.trim();
    
    if (!message || isTyping) return;
    
    console.log('Sending message:', message);
    
    // 设置发送状态
    isTyping = true;
    updateSendButton();
    
    // 添加用户消息
    addMessage(message, 'user');
    
    // 清空输入框
    messageInput.value = '';
    
    // 显示打字状态
    showTyping();
    
    try {
        // 获取场景上下文
        const sceneDisplay = document.getElementById('scene-display');
        const sceneContext = sceneDisplay ? sceneDisplay.textContent : '';
        
        console.log('API request data:', {
            message: message,
            student_id: currentStudentId,
            scene_context: sceneContext
        });
        
        // 发送到API
        const response = await fetch('/api/send_message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                student_id: currentStudentId,
                scene_context: sceneContext
            })
        });
        
        console.log('API response status:', response.status);
        
        const data = await response.json();
        console.log('API response data:', data);
        
        if (data.success) {
            addMessage(data.reply, 'bot');
        } else {
            throw new Error(data.error || 'Unknown error');
        }
        
    } catch (error) {
        console.error('Send message error:', error);
        addMessage('Sorry, I encountered an error. Please try again.', 'bot', true);
        showError('Failed to send message: ' + error.message);
    } finally {
        isTyping = false;
        updateSendButton();
        hideTyping();
    }
}

// 添加消息到聊天区域
function addMessage(text, sender, isError = false) {
    const chatMessages = document.getElementById('chat-messages');
    if (!chatMessages) return;
    
    const messageRow = document.createElement('div');
    messageRow.className = `message-row ${sender}`;
    
    // 创建头像
    const avatar = document.createElement('div');
    avatar.className = 'avatar';
    
    const avatarImg = document.createElement('img');
    if (sender === 'user') {
        avatarImg.src = '/static/images/avatar/user_avatar.png';
        avatarImg.alt = 'User';
    } else {
        avatarImg.src = `/static/images/avatar/${currentStudentId}.png`;
        avatarImg.alt = currentStudentName;
    }
    
    // 头像加载错误处理
    avatarImg.onerror = function() {
        console.log('Avatar loading failed for:', sender === 'user' ? 'user' : currentStudentId);
        console.log('Failed URL:', this.src);
        // 显示一个默认的文字标识
        this.style.display = 'none';
        const textFallback = document.createElement('div');
        textFallback.style.width = '40px';
        textFallback.style.height = '40px';
        textFallback.style.borderRadius = '50%';
        textFallback.style.backgroundColor = '#F0DBDB';
        textFallback.style.display = 'flex';
        textFallback.style.alignItems = 'center';
        textFallback.style.justifyContent = 'center';
        textFallback.style.fontSize = '12px';
        textFallback.style.color = '#2e285c';
        textFallback.textContent = sender === 'user' ? 'U' : currentStudentName.charAt(0);
        avatar.appendChild(textFallback);
    };
    
    avatar.appendChild(avatarImg);
    
    // 创建消息气泡
    const messageBubble = document.createElement('div');
    messageBubble.className = `message-bubble ${sender}`;
    if (isError) messageBubble.classList.add('error');
    
    messageBubble.textContent = text;
    
    messageRow.appendChild(avatar);
    messageRow.appendChild(messageBubble);
    
    chatMessages.appendChild(messageRow);
    
    // 滚动到底部
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// 清空聊天
async function clearChat() {
    if (!confirm('Are you sure you want to clear the chat history?')) {
        return;
    }
    
    try {
        const response = await fetch('/api/clear_chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                student_id: currentStudentId
            })
        });
        
        if (response.ok) {
            // 清空界面（保留欢迎消息）
            const chatMessages = document.getElementById('chat-messages');
            const messages = chatMessages.querySelectorAll('.message-row:not(.welcome-message)');
            messages.forEach(msg => msg.remove());
            console.log('Chat cleared');
        }
    } catch (error) {
        console.error('Clear chat error:', error);
        showError('Failed to clear chat');
    }
}

// 更新发送按钮状态
function updateSendButton() {
    const messageInput = document.getElementById('message-input');
    const sendBtn = document.getElementById('send-btn');
    
    if (messageInput && sendBtn) {
        const hasText = messageInput.value.trim().length > 0;
        sendBtn.disabled = !hasText || isTyping;
        sendBtn.textContent = isTyping ? 'Sending...' : 'Send';
    }
}

// 显示打字状态
function showTyping() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.style.display = 'flex';
        // 滚动到底部
        const chatMessages = document.getElementById('chat-messages');
        if (chatMessages) {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }
}

// 隐藏打字状态
function hideTyping() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.style.display = 'none';
    }
}

// 场景变化处理
function handleSceneChange() {
    const sceneDropdown = document.getElementById('scene-dropdown');
    const customScene = document.getElementById('custom-scene');
    const sceneDisplay = document.getElementById('scene-display');
    
    if (!sceneDropdown || !sceneDisplay) return;
    
    const selectedValue = sceneDropdown.value;
    const isCustom = selectedValue === 'Custom scenario';
    
    // 显示/隐藏自定义输入
    if (customScene) {
        customScene.style.display = isCustom ? 'block' : 'none';
    }
    
    // 更新场景显示
    if (isCustom) {
        const customInput = document.getElementById('custom-input');
        const customText = customInput ? customInput.value.trim() : '';
        sceneDisplay.textContent = customText || 'Please describe your custom scenario above';
    } else {
        sceneDisplay.textContent = selectedValue;
    }
}

// 显示错误提示
function showError(message) {
    const errorToast = document.getElementById('error-toast');
    if (errorToast) {
        const messageEl = errorToast.querySelector('.toast-message');
        if (messageEl) {
            messageEl.textContent = message;
        }
        errorToast.style.display = 'block';
        
        // 3秒后自动隐藏
        setTimeout(() => {
            errorToast.style.display = 'none';
        }, 3000);
    } else {
        // 备用方案
        alert(message);
    }
}

// 全局错误隐藏函数
window.hideError = function() {
    const errorToast = document.getElementById('error-toast');
    if (errorToast) {
        errorToast.style.display = 'none';
    }
};

// 导出给模板使用
window.initializeChat = initializeChat;
