# 定义自定义CSS样式
custom_css = """
/* Global styles with light blue background */
body {
    font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
    background-color: #d8eefe;
}

/* Hide the hover overlay and buttons for image viewer */
.no-interaction .svelte-1ipelgc,
.no-interaction .svelte-1ipelgc > button,
.no-interaction .download, 
.no-interaction .expand {
    display: none !important;
}

/* Ensure the image is shown with transparent background */
.title-image img {
    background-color: transparent !important;
    box-shadow: none !important;
}

/* Container for main content with light blue background */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 24px;
    background-color: #d8eefe;
}

/* Header container styling */
.header-container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    background-color: #d8eefe;
    border-radius: 8px 8px 0 0;
    padding: 15px 0;
    margin: 0;
}

/* Combined logo and title image container */
.logo-title-container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
}

/* Title image styling */
.title-image {
    max-width: 80%;
    height: auto;
    margin: 0 auto;
}

/* Selection heading styling */
.selection-heading {
    text-align: center;
    margin: 20px 0 10px;
    color: #094067;
    font-size: 20px;
}

/* Description text styling */
.description-text {
    text-align: center;
    margin: 10px auto 20px;
    max-width: 800px;
    color: #094067;
    font-size: 14px;
    line-height: 1.5;
}

/* Character.ai style grid for selection page - 5 columns by default */
.character-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 15px;
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
}

/* Responsive breakpoints for character grid at different screen sizes */
@media (max-width: 1200px) {
    .character-grid {
        grid-template-columns: repeat(4, 1fr);
    }
}

@media (max-width: 992px) {
    .character-grid {
        grid-template-columns: repeat(3, 1fr);
    }
}

@media (max-width: 768px) {
    .character-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 480px) {
    .character-grid {
        grid-template-columns: 1fr;
    }
}

.character-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 15px rgba(0,0,0,0.15);
}

.character-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 15px rgba(0,0,0,0.15);
}

/* 更广泛的卡片头部选择器 - 确保名字显示为白色加粗 */
.card-header,
.character-card > div:first-child,
.character-card > div:first-of-type,
.character-card > .markdown-text > h3,
.character-card > .markdown-text > p:first-child,
.character-card .markdown-text,
.character-grid .character-card > div:nth-child(1) {
    background-color: #094067 !important;
    color: #fffffe !important; /* 纯白色文字 */
    padding: 10px !important;
    text-align: center !important;
    font-weight: bold !important; /* 加粗 */
    font-size: 16px !important; /* 稍微增大字号 */
    letter-spacing: 0.5px !important; /* 增加字母间距提高可读性 */
    text-shadow: 0 1px 2px rgba(0,0,0,0.2) !important; /* 添加轻微文字阴影增强对比度 */
}

/* 额外添加更多可能的卡片头部选择器 */
.character-card div:first-of-type,
.character-card .svelte-1pw0mi9,
.character-card > .svelte-1adtsa9,
.gradio-card-header,
.character-card [class*="card-header"],
.character-card [class*="header"] {
    background-color: #094067 !important;
    color: #fffffe !important;
    font-weight: bold !important;
}

/* 学生信息样式 */
.student-name {
    font-size: 18px;
    font-weight: bold;
    margin: 10px 0 5px;
    text-align: center;
    color: #094067;
}

/* 学生信息样式 - 改为与页面相同的浅蓝色背景 */
.student-description {
    color: #000000 !important;  /* 黑色文字 */
    padding: 10px !important;
    margin: 8px 12px !important;
    background-color: transparent !important;  /* 透明背景 */
    box-shadow: none !important;  /* 无阴影 */
    border: none !important;  /* 无边框 */
    text-align: center !important;
}

/* Also update the character-card style to ensure it uses the page background */
.character-card {
    background-color: #d8eefe !important;
    border: none !important;
    box-shadow: none !important;
}

/* 隐藏模型标签 */
.model-tag {
    display: none;
}

/* 选择页面头像样式 - 圆形 */
.character-card .avatar-container {
    width: 100px !important;
    height: 100px !important;
    overflow: hidden !important;
    margin: 15px auto !important;
    border: 2px solid rgba(9,64,103,0.3) !important;
    border-radius: 50% !important;
    background-color: transparent !important;
}

.character-card .avatar-container img {
    width: 100% !important;
    height: 100% !important;
    object-fit: cover !important;
    display: block !important;
}

/* 聊天按钮样式 */
.chat-btn {
    background-color: #3da9fc !important;
    color: #fffffe !important;
    border: none !important;
    border-radius: 20px !important;
    padding: 6px 0 !important;
    margin: 6px auto 10px !important;
    width: 85% !important;
    display: block !important;
    font-weight: bold !important;
    cursor: pointer !important;
    font-size: 13px !important;
}

.chat-btn:hover {
    background-color: #90b4ce !important;
}

/* 聊天页面头部 */
.chat-header {
    display: flex;
    align-items: center;
    padding: 15px;
    border-bottom: 1px solid #90b4ce;
    background-color: #d8eefe;
    color: #094067;
    border-radius: 8px 8px 0 0;
}

.back-btn {
    background-color: #094067 !important;
    border: none !important;
    color: #fffffe !important;
    border-radius: 5px !important;
    margin-right: 15px !important;
    margin-left: 0 !important;
}

/* 居中头部标题 */
.center-header {
    margin: 0 auto;
    text-align: center;
}

/* 聊天区域名称标题 */
.student-name-header {
    font-size: 22px;
    font-weight: bold;
    margin: 0;
    color: #094067;
}

/* ==== 聊天界面核心样式修复 ==== */

/* 聊天区整体样式 */
.character-ai-style.chatbox-container {
    background-color: #d8eefe !important;
    padding: 20px !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
}

/* 聊天容器 */
.gradio-chatbot {
    background-color: #d8eefe !important;
}

/* 消息行容器 */
.gradio-chatbot .message-wrap {
    display: flex !important;
    align-items: flex-start !important;
    margin-bottom: 15px !important;
    position: relative !important;
    width: 100% !important;
}

/* 用户消息行反向排列 */
.gradio-chatbot .message-wrap.user {
    flex-direction: row-reverse !important;
}

/* 头像大小增加50% - 从30px增至45px */
.gradio-chatbot .avatar,
.gradio-chatbot .avatar img,
.gradio-chatbot img.avatar-image,
.gradio-chatbot .message-wrap img,
.gradio-chatbot .message-wrap .svelte-1y9ctm5 img,
.gradio-chatbot .message-wrap > div:first-child img {
    width: 45px !important;
    height: 45px !important;
    border-radius: 50% !important;
    border: 2px solid #094067 !important;
    object-fit: cover !important;
    display: block !important;
    box-shadow: none !important;
}

/* 头像容器尺寸同步增加 */
.gradio-chatbot .avatar-container,
.gradio-chatbot .message-wrap > div:first-child,
.gradio-chatbot .message-wrap .svelte-1y9ctm5 {
    width: 45px !important;
    height: 45px !important;
    min-width: 45px !important;
    min-height: 45px !important;
    max-width: 45px !important;
    max-height: 45px !important;
    border-radius: 50% !important;
    overflow: hidden !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* 消息气泡通用样式 */
.gradio-chatbot .message {
    padding: 12px 16px !important;
    margin: 0 8px !important;
    max-width: 80% !important;
    word-wrap: break-word !important;
    line-height: 1.5 !important;
}

/* 强制设置用户消息气泡样式 - 白色背景深蓝文字 */
.gradio-chatbot .message.user,
.gradio-chatbot .message-wrap.user .message {
    background-color: #fffffe !important;
    color: #094067 !important;
    border: 1px solid #90b4ce !important;
    border-radius: 18px 18px 4px 18px !important;
    margin-right: 8px !important;
    margin-left: auto !important;
}

/* 强制设置机器人消息气泡样式 - 蓝色背景白色文字 */
.gradio-chatbot .message.bot,
.gradio-chatbot .message-wrap.bot .message {
    background-color: #3da9fc !important;
    color: #fffffe !important;
    border: none !important;
    border-radius: 18px 18px 18px 4px !important;
    margin-left: 8px !important;
    margin-right: auto !important;
}

/* 情感标签样式 */
.emotion-tag {
    font-style: italic !important;
    display: block !important;
    margin-top: 5px !important;
    font-size: 0.9em !important;
    color: #094067 !important;
}

/* 聊天输入区域样式 */
.message-input {
    background-color: #fffffe !important;
    border-radius: 20px !important;
    border: 1px solid #90b4ce !important;
    margin-bottom: 10px !important;
}

.message-input textarea {
    background-color: #fffffe !important;
    border: none !important;
    border-radius: 20px !important;
    padding: 12px 16px !important;
    font-size: 14px !important;
    color: #094067 !important;
    resize: none !important;
    width: 100% !important;
    box-shadow: none !important;
}

/* 按钮容器样式 */
.button-container {
    display: flex !important;
    flex-direction: column !important;
    gap: 10px !important;
}

/* 发送按钮样式 */
.send-btn {
    background-color: #3da9fc !important;
    color: #fffffe !important;
    font-weight: bold !important;
    border-radius: 20px !important;
    padding: 10px 20px !important;
    border: none !important;
    width: 100% !important;
}

/* 清除按钮样式 */
.clear-btn {
    background-color: #094067 !important;
    color: #fffffe !important;
    font-weight: bold !important;
    border-radius: 20px !important;
    padding: 10px 20px !important;
    border: none !important;
    width: 100% !important;
}

/* 移除可能的行背景 */
.gradio-container .row {
    background-color: transparent !important;
}

/* 额外修复 - 消除所有可能干扰的样式 */
.prose img, 
.prose .avatar, 
.prose .avatar-image, 
.svelte-1adtsa9, 
.svelte-1u4fftl {
    border-radius: 50% !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* 移除chatbot中任何可能的padding和margin */
.gradio-chatbot {
    padding: 0 !important;
    margin: 0 !important;
}

/* 强制修复JavaScript可能添加的样式 */
.svelte-1adtsa9,
.svelte-1y9ctm5 {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

/* 确保所有聊天气泡内容有正确的颜色 */
.gradio-chatbot .message.bot *,
.gradio-chatbot .message-wrap.bot .message * {
    color: #fffffe !important;
}

.gradio-chatbot .message.user *,
.gradio-chatbot .message-wrap.user .message * {
    color: #094067 !important;
}

/* 确保任何可能的内嵌元素也正确着色 */
.gradio-chatbot .bot .message p,
.gradio-chatbot .bot .message div,
.gradio-chatbot .bot .message span {
    color: #fffffe !important;
}

.gradio-chatbot .user .message p,
.gradio-chatbot .user .message div,
.gradio-chatbot .user .message span {
    color: #094067 !important;
}
"""
