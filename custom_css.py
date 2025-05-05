custom_css = """
/* Global styles for the entire application */
body {
    font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
    background-color: #ffffff;
}

/* Header styling with updated brand color */
.main-title {
    background-color: #094067;
    color: white;
    padding: 15px;
    margin: 0;
    text-align: center;
    font-size: 24px;
    font-weight: bold;
    border-radius: 8px 8px 0 0;
}

/* 隐藏图片上的放大和下载按钮 */
.gr-image-actions {
    display: none !important;
}

/* Character.ai style grid for selection page - 5 columns by default */
.character-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 20px;
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

/* Card styling - updated with rounded edges */
.character-card {
    background: white;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    transition: transform 0.2s, box-shadow 0.2s;
    border: 1px solid #e0e0e0;
    height: 100%;
    display: flex;
    flex-direction: column;
    cursor: pointer;
    max-width: 220px;
    margin: 0 auto;
}

.character-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 16px rgba(0,0,0,0.15);
}





/* Student info styling - compact and readable */
.student-name {
    font-size: 16px;
    font-weight: bold;
    margin: 8px 0 4px;
    text-align: center;
}

.student-description {
    padding: 0 12px;
    text-align: center;
    color: #555;
    font-size: 13px;
    min-height: 45px;
    overflow: hidden;
    flex-grow: 1;
    margin-bottom: 8px;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
}

/* Hide model tag for cleaner interface */
.model-tag {
    display: none;
}

/* Avatar styling - updated with circular design */
.character-card .avatar-container {
    width: 100px !important;
    height: 100px !important;
    background-color: #fbe5bd !important;  /* 底色 */
    border-radius: 50% !important;
    overflow: hidden !important;
    margin: 12px auto 8px !important;  /* 垂直居中 */
    box-shadow: 0 2px 6px rgba(0,0,0,0.1) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    flex-shrink: 0 !important;
}

.character-card .avatar-container img {
    width: 100% !important;
    height: 100% !important;
    object-fit: cover !important;
    border-radius: 50% !important;
    display: block !important;
}

/* 移除嵌套层和按钮图标 */
.character-card .avatar-container .gr-image,
.character-card .avatar-container .gr-image * {
    all: unset !important;
    display: block !important;
    border-radius: 50% !important;
}

/* Chat button styling with updated brand color */
.chat-btn {
    background-color: #3da9fc !important;
    color: white !important;
    border: none !important;
    border-radius: 20px !important;
    padding: 8px 0 !important;
    margin: 10px auto 16px !important;
    width: 85% !important;
    display: block !important;
    font-weight: bold !important;
    cursor: pointer !important;
    font-size: 14px !important;
    transition: background-color 0.2s !important;
}

.card-header {
    background-color: #094067 !important;
    color: white !important;
    font-weight: 900 !important;
    font-size: 14px !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    height: 40px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-family: 'Inter', sans-serif !important;
}

.card-header * {
    color: white !important;
}



.chat-btn:hover {
    background-color: #2a93e0 !important;
}

/* Chat interface styling for better user experience */
.chat-header {
    display: flex;
    align-items: center;
    padding: 15px;
    border-bottom: 1px solid #e0e0e0;
    background-color: #094067;
    color: white;
    border-radius: 12px 12px 0 0;
}

.back-btn {
    background-color: #3da9fc !important;
    border: none !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 5px 15px !important;
    margin-right: 15px !important;
    font-weight: bold !important;
    font-size: 14px !important;
    cursor: pointer !important;
    transition: background-color 0.2s !important;
}

.back-btn:hover {
    background-color: #2a93e0 !important;
}

/* Input and buttons styling for better aesthetics */
/* 移除输入区域的背景白色块 */
.message-input {
    background-color: transparent !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* 输入框本身内部是白色 */
.message-input textarea {
    background-color: #fffffe !important;
    border: 1px solid #90b4ce !important;
    border-radius: 20px !important;
    padding: 12px 16px !important;
    font-size: 14px !important;
    color: #094067 !important;
    resize: none !important;
    height: 70px !important;  /* 你想要更高一点就调这个 */
}

/* Button container for vertical layout */
.button-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
    width: 100%;
}

.send-btn {
    background-color: #3da9fc !important;
    color: #fffffe !important;
    font-weight: bold !important;
    border-radius: 20px !important;
    padding: 8px 15px !important;
    width: 100% !important;
    border: none !important;
    cursor: pointer !important;
    transition: background-color 0.2s !important;
}

.send-btn:hover {
    background-color: #2a93e0 !important;
}

.clear-btn {
    background-color: #094067 !important;
    color: #fffffe !important;
    font-weight: bold !important;
    border-radius: 20px !important;
    padding: 8px 15px !important;
    width: 100% !important;
    border: none !important;
    cursor: pointer !important;
    transition: background-color 0.2s !important;
}

.clear-btn:hover {
    background-color: #073050 !important;
}

/* Character info styling in chat - simplified header without avatar */
.character-info {
    display: flex;
    flex-direction: column;
    justify-content: center;
    margin-left: 5px;
}

/* Student name styling in header */
.student-name-header {
    color: #fffffe !important;
    font-size: 24px !important;
    font-weight: bold !important;
    margin: 0 auto !important;
    text-align: center !important;
}

/* Model display styling - hidden by default */
.model-display {
    display: none;
}

/* Character.ai style chat container */
.character-ai-style {
    border-radius: 12px;
    background-color: #ffffff !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

/* 正确仅选中头像容器，而不是任意第一个 div */
.message-wrap .avatar {
    width: 60px !important;
    height: 60px !important;
    border-radius: 50% !important;
    overflow: hidden !important;
    border: 2px solid #094067 !important;
    flex-shrink: 0 !important;
    background-color: transparent !important;
}

.message-wrap .avatar img {
    width: 100% !important;
    height: 100% !important;
    object-fit: cover !important;
    border-radius: 50% !important;
    display: block !important;
}




/* Custom styling for chat rows */
.chatbot-row {
    display: flex;
    margin-bottom: 20px;
}




/* Chat bubbles: AI is blue, user is white */
.gradio-chatbot .message.bot {
    background-color: #3da9fc !important;
    color: #fffffe !important;
    border-bottom-left-radius: 6px !important;
    border-top-left-radius: 18px !important;
    border-top-right-radius: 18px !important;
    border-bottom-right-radius: 18px !important;
    margin-left: 12px !important;
    margin-right: auto !important;
    max-width: 80%;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
    padding: 12px 16px !important;
    word-wrap: break-word !important;
}

.gradio-chatbot .message.user {
    background-color: #fffffe !important;
    color: #094067 !important;
    border-bottom-right-radius: 6px !important;
    border-top-left-radius: 18px !important;
    border-top-right-radius: 18px !important;
    border-bottom-left-radius: 18px !important;
    margin-right: 12px !important;
    margin-left: auto !important;
    max-width: 80%;
    border: 1px solid #90b4ce !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
    padding: 12px 16px !important;
    word-wrap: break-word !important;
}

/* Chat area overall background (light blue) */
.character-ai-style.chatbox-container {
    background-color: #ffffff !important;
    padding: 20px !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
}

/* Emotion tag styling for emotional context */
.emotion-tag {
    font-style: italic !important;
    font-size: 12px !important;
    color: #666 !important;
    margin-top: 4px !important;
    display: block !important;
}

/* Project description styling */
.project-description {
    text-align: center;
    margin: 0 auto 10px;
    max-width: 800px;
    color: #555;
    font-size: 14px;
    line-height: 1.5;
    padding: 0 20px;
    font-style: italic;
}



/* Ensure proper message wrapping and alignment */
.gradio-chatbot .message-wrap {
    margin-bottom: 16px !important;
    display: flex !important;
    align-items: flex-start !important;
}

/* Selection heading styling for clear hierarchy */
.selection-heading {
    text-align: center;
    margin: 11px 0 10px;
    color: #094067;
    font-size: 22px;
    font-weight: bold;
}

/* Container for main content with reasonable max width */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 24px;
}

/* Fix Gradio spacing issues */
.gradio-container {
    max-width: 100% !important;
}

/* Hide unnecessary margins in Gradio blocks */
.block {
    margin-bottom: 0 !important;
}

/* Center the name and model in the chat header */
.center-header {
    margin: 0 auto;
    text-align: center;
}






/* 强制隐藏所有图片上的放大和下载按钮 */
.gr-image-actions,
.gr-image-actions * {
    display: none !important;
}

/* Input row: transparent background, vertically centered */
.gradio-container .row {
    background-color: #ffffff !important;  /* 或你想要的灰色 */
    align-items: center !important;
    padding: 16px 12px !important;
}

.character-ai-style.chatbox-container + .gr-box {
    background-color: transparent !important;
    box-shadow: none !important;
    border: none !important;
}

/* 更强匹配 */
div[class*="image-actions"] {
    display: none !important;
}

button[aria-label="Download"], button[aria-label="Fullscreen"] {
    display: none !important;
}

/* 强力隐藏所有放大/下载按钮 */
div[class*="image-actions"],
div[class*="image-actions"] * {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
}
"""
