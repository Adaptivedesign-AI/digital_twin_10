// chat.js - 聊天界面功能

class ChatInterface {
    constructor(studentId, studentName) {
        this.studentId = studentId;
        this.studentName = studentName;
        this.isTyping = false;
        this.messageQueue = [];
        this.retryCount = 0;
        this.maxRetries = 3;
        
        this.initializeElements();
        this.initializeEventListeners();
        this.initializeSceneControl();
        this.loadChatHistory();
        
        console.log(`Chat interface initialized for ${studentName} (${studentId})`);
    }
    
    initializeElements() {
        this.elements = {
            messageInput: document.getElementById('message-input'),
            sendBtn: document.getElementById('send-btn'),
            clearBtn: document.getElementById('clear-btn'),
            chatMessages: document.getElementById('chat-messages'),
            sceneDropdown: document.getElementById('scene-dropdown'),
            customInput: document.getElementById('custom-input'),
            sceneDisplay: document.getElementById('scene-display'),
            typingIndicator: document.getElementById('typing-indicator'),
            errorToast: document.getElementById('error-toast')
        };
        
        // 验证必要元素存在
        const required = ['messageInput', 'sendBtn', 'chatMessages'];
        required.forEach(key => {
            if (!this.elements[key]) {
                console.error(`Required element not found: ${key}`);
            }
        });
    }
    
    initializeEventListeners() {
        // 发送消息
        this.elements.sendBtn?.addEventListener('click', () => this.sendMessage());
        
        // 清空聊天
        this.elements.clearBtn?.addEventListener('click', () => this.clearChat());
        
        // 输入框回车发送
        this.elements.messageInput?.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // 输入框自动调整高度
        this.elements.messageInput?.addEventListener('input', (e) => {
            this.autoResizeInput(e.target);
            this.updateSendButtonState();
        });
        
        // 初始状态
        this.updateSendButtonState();
    }
    
    initializeSceneControl() {
        if (!this.elements.sceneDropdown) return;
        
        // 场景下拉框变化
        this.elements.sceneDropdown.addEventListener('change', (e) => {
            this.handleSceneChange(e.target.value);
        });
        
        // 自定义场景输入
        this.elements.customInput?.addEventListener('input', 
            Utils.debounce(() => this.updateSceneDisplay(), 300)
        );
        
        // 初始化场景显示
        this.handleSceneChange(this.elements.sceneDropdown.value);
    }
    
    handleSceneChange(selectedScene) {
        const isCustom = selectedScene === 'Custom scenario';
        const customScene = document.getElementById('custom-scene');
        
        if (customScene) {
            customScene.style.display = isCustom ? 'block' : 'none';
        }
        
        if (isCustom) {
            this.updateSceneDisplay();
        } else {
            this.elements.sceneDisplay.textContent = selectedScene;
        }
        
        // 记录场景变化
        this.logUserAction('scene_change', {
            selected_scene: selectedScene,
            is_custom: isCustom
        });
    }
    
    updateSceneDisplay() {
        if (this.elements.sceneDropdown.value === 'Custom scenario') {
            const customText = this.elements.customInput?.value.trim() || 'No custom scenario provided';
            this.elements.sceneDisplay.textContent = customText;
        }
    }
    
    autoResizeInput(textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
    }
    
    updateSendButtonState() {
        const hasText = this.elements.messageInput?.value.trim().length > 0;
        const sendBtn = this.elements.sendBtn;
        
        if (sendBtn) {
            sendBtn.disabled = !hasText || this.isTyping;
            sendBtn.textContent = this.isTyping ? 'Sending...' : 'Send';
        }
    }
    
    async sendMessage() {
        const message = this.elements.messageInput?.value.trim();
        
        if (!message || this.isTyping) return;
        
        // 设置发送状态
        this.isTyping = true;
        this.updateSendButtonState();
        
        // 添加用户消息到界面
        this.addMessage(message, 'user');
        
        // 清空输入框
        this.elements.messageInput.value = '';
        this.autoResizeInput(this.elements.messageInput);
        
        // 显示打字指示器
        this.showTypingIndicator();
        
        try {
            // 发送到后端
            const response = await this.callChatAPI(message);
            
            if (response.success) {
                this.addMessage(response.reply, 'bot');
                this.retryCount = 0; // 重置重试计数
            } else {
                throw new Error(response.error || 'Unknown error');
            }
        } catch (error) {
            console.error('Chat error:', error);
            this.handleChatError(error, message);
        } finally {
            // 恢复状态
            this.isTyping = false;
            this.updateSendButtonState();
            this.hideTypingIndicator();
        }
    }
    
    async callChatAPI(message) {
        const sceneContext = this.elements.sceneDisplay?.textContent || '';
        
        const response = await fetch('/api/send_message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                student_id: this.studentId,
                scene_context: sceneContext
            })
        });
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
        }
        
        return await response.json();
    }
    
    handleChatError(error, originalMessage) {
        let errorMessage = 'Sorry, I encountered an error. Please try again.';
        
        if (error.message.includes('API')) {
            errorMessage = 'There was an issue with the AI service. Please try again in a moment.';
        } else if (error.message.includes('network') || error.message.includes('fetch')) {
            errorMessage = 'Network error. Please check your connection and try again.';
        }
        
        // 添加错误消息到聊天
        this.addMessage(errorMessage, 'bot', true);
        
        // 显示错误提示
        Utils.showError(error.message);
        
        // 如果重试次数未超限，提供重试选项
        if (this.retryCount < this.maxRetries) {
            this.offerRetry(originalMessage);
        }
        
        this.retryCount++;
    }
    
    offerRetry(originalMessage) {
        const retryMessage = document.createElement('div');
        retryMessage.className = 'retry-offer';
        retryMessage.innerHTML = `
            <button class="retry-btn" onclick="chatInterface.retryMessage('${Utils.escapeHtml(originalMessage)}')">
                🔄 Retry message
            </button>
        `;
        
        const lastBotMessage = this.elements.chatMessages.querySelector('.message-row:last-child');
        if (lastBotMessage) {
            lastBotMessage.appendChild(retryMessage);
        }
    }
    
    async retryMessage(message) {
        // 移除重试按钮
        document.querySelectorAll('.retry-offer').forEach(el => el.remove());
        
        // 重新发送消息
        this.elements.messageInput.value = message;
        await this.sendMessage();
    }
    
    addMessage(text, sender, isError = false) {
        const messageRow = document.createElement('div');
        messageRow.className = `message-row ${sender}`;
        
        const avatar = document.createElement('div');
        avatar.className = 'avatar';
        
        const avatarImg = document.createElement('img');
        if (sender === 'user') {
            avatarImg.src = '/static/images/user_avatar.png';
            avatarImg.alt = 'User';
        } else {
            avatarImg.src = `/static/images/avatar/${this.studentId}.png`;
            avatarImg.alt = this.studentName;
        }
        
        // 头像加载错误处理
        avatarImg.onerror = function() {
            this.src = '/static/images/default_avatar.png';
        };
        
        avatar.appendChild(avatarImg);
        
        const messageBubble = document.createElement('div');
        messageBubble.className = `message-bubble ${sender}`;
        
        if (isError) {
            messageBubble.classList.add('error');
        }
        
        // 处理消息文本（支持简单的格式化）
        messageBubble.innerHTML = this.formatMessage(text);
        
        messageRow.appendChild(avatar);
        messageRow.appendChild(messageBubble);
        
        // 添加到消息容器
        this.elements.chatMessages.appendChild(messageRow);
        
        // 滚动到底部
        this.scrollToBottom();
        
        // 添加进入动画
        requestAnimationFrame(() => {
            messageRow.style.opacity = '0';
            messageRow.style.transform = 'translateY(20px)';
            messageRow.style.transition = 'all 0.3s ease';
            
            requestAnimationFrame(() => {
                messageRow.style.opacity = '1';
                messageRow.style.transform = 'translateY(0)';
            });
        });
    }
    
    formatMessage(text) {
        // 简单的文本格式化
        return Utils.escapeHtml(text)
            .replace(/\n/g, '<br>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>');
    }
    
    showTypingIndicator() {
        if (this.elements.typingIndicator) {
            this.elements.typingIndicator.style.display = 'flex';
            this.scrollToBottom();
        }
    }
    
    hideTypingIndicator() {
        if (this.elements.typingIndicator) {
            this.elements.typingIndicator.style.display = 'none';
        }
    }
    
    scrollToBottom() {
        if (this.elements.chatMessages) {
            this.elements.chatMessages.scrollTop = this.elements.chatMessages.scrollHeight;
        }
    }
    
    async clearChat() {
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
                    student_id: this.studentId
                })
            });
            
            if (response.ok) {
                // 清空界面
                const messages = this.elements.chatMessages.querySelectorAll('.message-row:not(.welcome-message)');
                messages.forEach(msg => msg.remove());
                
                // 重置状态
                this.retryCount = 0;
                
                console.log('Chat cleared successfully');
            } else {
                throw new Error('Failed to clear chat');
            }
        } catch (error) {
            console.error('Clear chat error:', error);
            Utils.showError('Failed to clear chat. Please try again.');
        }
    }
    
    async loadChatHistory() {
        try {
            const response = await fetch(`/api/get_chat_history/${this.studentId}`);
            
            if (response.ok) {
                const data = await response.json();
                const history = data.history || [];
                
                // 清空现有消息（除了欢迎消息）
                const messages = this.elements.chatMessages.querySelectorAll('.message-row:not(.welcome-message)');
                messages.forEach(msg => msg.remove());
                
                // 添加历史消息
                history.forEach(([userMsg, botMsg]) => {
                    this.addMessage(userMsg, 'user');
                    this.addMessage(botMsg, 'bot');
                });
                
                if (history.length > 0) {
                    this.scrollToBottom();
                }
            }
        } catch (error) {
            console.error('Failed to load chat history:', error);
        }
    }
    
    // 用户行为日志记录
    logUserAction(actionType, actionData = {}) {
        // 可以发送到后端进行分析
        console.log('User action:', actionType, actionData);
    }
    
    // 响应式处理
    handleResize() {
        // 重新调整聊天区域高度
        if (this.elements.chatMessages) {
            const container = this.elements.chatMessages.closest('.chat-left');
            if (container) {
                // 触发重新布局
                container.style.height = 'auto';
                requestAnimationFrame(() => {
                    this.scrollToBottom();
                });
            }
        }
    }
    
    // 暂停更新（页面不可见时）
    pauseUpdates() {
        this.updatesPaused = true;
    }
    
    // 恢复更新
    resumeUpdates() {
        this.updatesPaused = false;
        // 可能需要刷新某些状态
    }
    
    // 网络恢复处理
    handleNetworkRestore() {
        console.log('Network restored, refreshing chat interface');
        // 可以重新加载聊天历史或重新连接
    }
}

// 全局错误隐藏函数
window.hideError = function() {
    Utils.hideError();
};

// 初始化函数
window.initializeChat = function(studentId, studentName) {
    // 创建全局聊天界面实例
    window.ChatInterface = new ChatInterface(studentId, studentName);
    window.chatInterface = window.ChatInterface; // 向后兼容
    
    console.log('Chat interface ready');
};