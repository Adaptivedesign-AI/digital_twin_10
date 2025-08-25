// main.js - 主要交互功能

// 工具函数
const Utils = {
    // 防抖函数
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    // 显示错误提示
    showError(message) {
        const toast = document.getElementById('error-toast');
        const messageEl = toast.querySelector('.toast-message');
        messageEl.textContent = message;
        toast.style.display = 'block';
        
        // 3秒后自动隐藏
        setTimeout(() => {
            this.hideError();
        }, 3000);
    },

    // 隐藏错误提示
    hideError() {
        const toast = document.getElementById('error-toast');
        toast.style.display = 'none';
    },

    // 格式化时间
    formatTime(date) {
        return date.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            hour12: true
        });
    },

    // 安全的HTML转义
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    },

    // 检查是否为移动设备
    isMobile() {
        return window.innerWidth <= 768;
    }
};

// 全局错误处理
window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
    Utils.showError('An unexpected error occurred. Please refresh the page.');
});

// 网络请求错误处理
window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
    Utils.showError('Network error. Please check your connection and try again.');
});

// 页面加载完成后的初始化
document.addEventListener('DOMContentLoaded', function() {
    // 添加全局样式增强
    initializeGlobalEnhancements();
    
    // 如果是选择页面，初始化角色卡片交互
    if (document.querySelector('.character-grid')) {
        initializeCharacterSelection();
    }
    
    // 添加键盘导航支持
    initializeKeyboardNavigation();
    
    // 初始化可访问性功能
    initializeAccessibility();
});

// 全局样式增强
function initializeGlobalEnhancements() {
    // 添加平滑滚动
    document.documentElement.style.scrollBehavior = 'smooth';
    
    // 为所有按钮添加焦点样式
    const style = document.createElement('style');
    style.textContent = `
        button:focus, 
        select:focus, 
        textarea:focus, 
        input:focus {
            outline: 2px solid #DBA39A;
            outline-offset: 2px;
        }
        
        .character-card:focus {
            outline: 3px solid #DBA39A;
            outline-offset: 4px;
        }
    `;
    document.head.appendChild(style);
}

// 角色选择页面交互
function initializeCharacterSelection() {
    const cards = document.querySelectorAll('.character-card');
    
    cards.forEach(card => {
        // 添加键盘支持
        card.setAttribute('tabindex', '0');
        card.setAttribute('role', 'button');
        
        // 鼠标交互
        card.addEventListener('mouseenter', function() {
            this.classList.add('hover');
            // 预加载头像
            const img = this.querySelector('img');
            if (img && !img.complete) {
                const preloader = new Image();
                preloader.src = img.src;
            }
        });
        
        card.addEventListener('mouseleave', function() {
            this.classList.remove('hover');
        });
        
        // 点击交互
        card.addEventListener('click', function(e) {
            if (e.target.classList.contains('chat-btn')) return;
            
            const studentId = this.dataset.studentId;
            const studentName = this.querySelector('.student-name').textContent;
            
            selectStudentWithAnimation(studentId, studentName, this);
        });
        
        // 键盘交互
        card.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });
        
        // 添加动画就绪类
        card.classList.add('animation-ready');
    });
}

// 带动画的学生选择
function selectStudentWithAnimation(studentId, studentName, cardElement) {
    // 防止重复点击
    if (cardElement.classList.contains('selecting')) return;
    
    cardElement.classList.add('selecting');
    
    // 添加选中效果
    document.querySelectorAll('.character-card').forEach(card => {
        if (card !== cardElement) {
            card.style.opacity = '0.5';
            card.style.transform = 'scale(0.95)';
        }
    });
    
    cardElement.classList.add('selected');
    
    // 显示加载动画
    const loadingOverlay = document.getElementById('loading-overlay');
    if (loadingOverlay) {
        loadingOverlay.style.display = 'flex';
        
        // 更新加载文本
        const loadingText = loadingOverlay.querySelector('p');
        if (loadingText) {
            loadingText.textContent = `Loading chat with ${studentName}...`;
        }
    }
    
    // 延迟跳转以显示动画
    setTimeout(() => {
        window.location.href = `/chat/${studentId}`;
    }, 800);
}

// 键盘导航支持
function initializeKeyboardNavigation() {
    document.addEventListener('keydown', function(e) {
        // ESC键关闭错误提示
        if (e.key === 'Escape') {
            Utils.hideError();
        }
        
        // 角色选择页面的键盘导航
        if (document.querySelector('.character-grid')) {
            const cards = document.querySelectorAll('.character-card');
            const currentIndex = Array.from(cards).findIndex(card => 
                document.activeElement === card
            );
            
            let newIndex = currentIndex;
            
            switch(e.key) {
                case 'ArrowRight':
                    e.preventDefault();
                    newIndex = (currentIndex + 1) % cards.length;
                    break;
                case 'ArrowLeft':
                    e.preventDefault();
                    newIndex = (currentIndex - 1 + cards.length) % cards.length;
                    break;
                case 'ArrowDown':
                    e.preventDefault();
                    // 计算每行的卡片数量
                    const cardsPerRow = Math.floor(window.innerWidth / 240); // 大约卡片宽度
                    newIndex = Math.min(currentIndex + cardsPerRow, cards.length - 1);
                    break;
                case 'ArrowUp':
                    e.preventDefault();
                    const cardsPerRowUp = Math.floor(window.innerWidth / 240);
                    newIndex = Math.max(currentIndex - cardsPerRowUp, 0);
                    break;
            }
            
            if (newIndex !== currentIndex && newIndex >= 0 && newIndex < cards.length) {
                cards[newIndex].focus();
            }
        }
    });
}

// 可访问性功能
function initializeAccessibility() {
    // 为角色卡片添加ARIA标签
    const cards = document.querySelectorAll('.character-card');
    cards.forEach((card, index) => {
        const studentName = card.querySelector('.student-name').textContent;
        const description = card.querySelector('.student-description').textContent;
        
        card.setAttribute('aria-label', 
            `Chat with ${studentName}. ${description}. Press Enter to start conversation.`
        );
        card.setAttribute('aria-describedby', `card-desc-${index}`);
        
        // 添加描述元素
        const descElement = document.createElement('div');
        descElement.id = `card-desc-${index}`;
        descElement.className = 'sr-only';
        descElement.textContent = `Student ${index + 1} of ${cards.length}`;
        card.appendChild(descElement);
    });
    
    // 为错误提示添加ARIA属性
    const errorToast = document.getElementById('error-toast');
    if (errorToast) {
        errorToast.setAttribute('role', 'alert');
        errorToast.setAttribute('aria-live', 'polite');
    }
    
    // 添加屏幕阅读器专用样式
    const srStyle = document.createElement('style');
    srStyle.textContent = `
        .sr-only {
            position: absolute;
            width: 1px;
            height: 1px;
            padding: 0;
            margin: -1px;
            overflow: hidden;
            clip: rect(0, 0, 0, 0);
            white-space: nowrap;
            border: 0;
        }
    `;
    document.head.appendChild(srStyle);
}

// 全局函数导出
window.Utils = Utils;
window.hideError = Utils.hideError;

// 性能监控
if ('performance' in window) {
    window.addEventListener('load', () => {
        setTimeout(() => {
            const perfData = performance.timing;
            const loadTime = perfData.loadEventEnd - perfData.navigationStart;
            console.log(`Page loaded in ${loadTime}ms`);
        }, 0);
    });
}
