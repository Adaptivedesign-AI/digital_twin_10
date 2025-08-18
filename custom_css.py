custom_css = """
/* Global styles for the entire application */
body {
    font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
    background: white !important;
    min-height: 100vh;
}

/* Make header transparent - remove white backgrounds */
.header-image-container, .header-image-container > div, .header-image, .header-image > div {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* More aggressive targeting of Gradio-generated containers */
.gradio-container .gradio-image, 
.gradio-container .gradio-image > div, 
.gradio-container [data-testid="image"], 
.gradio-container [data-testid="image"] > div,
.gradio-container [class*="image"],
.gradio-container [class*="image"] > div,
.gradio-container img[alt] {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* Ensure all image wrappers are transparent */
.gradio-container img {
    background-color: transparent !important;
}

/* Header styling with updated purple theme */
.main-title {
    background-color: #2e285c;
    color: white;
    padding: 15px;
    margin: 0;
    text-align: center;
    font-size: 24px;
    font-weight: bold;
    border-radius: 8px 8px 0 0;
}

/* Chat page header styling - 改成紫色背景 */
.chat-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 15px 20px;
    border-bottom: 1px solid #bdbad4;
    background-color: #bdbad4 !important;  /* 👈 white → #bdbad4 */
    color: white !important;               /* 👈 #2e285c → white */
    border-radius: 12px 12px 0 0;
    margin-bottom: 20px;
    box-shadow: 0 2px 8px rgba(46, 40, 92, 0.1);
}

.page-title {
    color: white !important;  /* 👈 #2e285c → white */
    margin: 0 !important;
    text-align: center;
    flex-grow: 1;
    font-weight: bold !important;
}

/* Main chat container - two column layout */
.main-chat-container {
    gap: 20px !important;
    padding: 0 20px;
    max-width: 1400px;
    margin: 0 auto;
}

/* Left column: Chat interface - 加长高度与右边对齐 */
.chat-column {
    background-color: white;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 12px rgba(46, 40, 92, 0.1);
    border: 1px solid #bdbad4;
    min-height: 123vh !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: space-between !important;
}

/* 确保聊天框占用大部分空间，输入框在底部 */
.chat-column .gradio-chatbot {
    flex: 1 !important;
    min-height: 1150px !important;
}

/* 输入框区域固定在底部 */
.chat-column > div:last-child {
    margin-top: auto !important;
    flex-shrink: 0 !important;
}

/* Right column: Information panels */
.info-column {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

/* Profile box styling - 保持白色不透明 */
.profile-box {
    background-color: white !important;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 12px rgba(46, 40, 92, 0.1);
    border: 1px solid #bdbad4 !important;
}

.profile-name {
    color: #2e285c !important;
    margin: 0 0 15px 0 !important;
    text-align: center;
    font-weight: bold !important;
}

.profile-image {
    border-radius: 12px;
    border: 2px solid #bdbad4;
}

.profile-text {
    font-size: 14px;
    line-height: 1.6;
    color: #2e285c;
    margin: 0 !important;
}

/* Instructions box styling - 保持白色不透明 */
.instructions-box {
    background-color: white !important;
    border-radius: 12px;
    padding: 20px;
    border: 1px solid #bdbad4 !important;
    box-shadow: 0 4px 12px rgba(46, 40, 92, 0.1);
}

.instructions-text {
    font-size: 14px;
    line-height: 1.6;
    color: #2e285c;
    margin: 0 !important;
}

/* Scene box styling - 保持白色不透明 */
.scene-box {
    background-color: white !important;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 12px rgba(46, 40, 92, 0.1);
    border: 1px solid #bdbad4 !important;
}

.section-title {
    color: #2e285c !important;
    margin: 0 0 15px 0 !important;
    font-weight: bold !important;
    font-size: 18px !important;
}

.scene-instruction {
    font-size: 14px;
    color: #2e285c;
    margin: 0 0 15px 0 !important;
}

.scene-dropdown select {
    border-radius: 8px;
    border: 1px solid #bdbad4;
    padding: 10px;
    font-size: 14px;
    background-color: white !important;
}

.custom-scene-input textarea {
    border-radius: 8px;
    border: 1px solid #bdbad4;
    padding: 10px;
    font-size: 14px;
    min-height: 80px;
    background-color: white !important;
}

.scene-description textarea {
    border-radius: 8px;
    border: 1px solid #bdbad4;
    padding: 10px;
    font-size: 14px;
    background-color: #f0edfe !important;
    min-height: 60px;
}

/* NEW: Main groups container for organized layout */
.main-groups-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    background-color: transparent !important;
}

/* NEW: Age group container styling */
.age-group-container {
    margin-bottom: 40px;
    padding: 20px;
    border: 2px solid #bdbad4;
    border-radius: 16px;
    background-color: #f8f7ff !important;
}

.age-group-title {
    color: #2e285c !important;
    text-align: center;
    margin: 0 0 25px 0 !important;
    font-weight: bold !important;
    font-size: 24px !important;
    border-bottom: 2px solid #bdbad4;
    padding-bottom: 10px;
}

/* NEW: Mental health group styling */
.mental-health-group {
    margin-bottom: 25px;
    padding: 15px;
    border-radius: 12px;
    background-color: rgba(255, 255, 255, 0.7) !important;
}

.mental-health-subtitle {
    color: #2e285c !important;
    margin: 0 0 15px 0 !important;
    font-weight: 600 !important;
    font-size: 16px !important;
    text-align: center;
    font-style: italic;
}

/* NEW: Character row styling for horizontal layout */
.character-row {
    display: flex;
    gap: 15px;
    justify-content: flex-start; /* 👈 改为左对齐，不再居中 */
    flex-wrap: wrap;
}

/* Updated character card styling - horizontal layout with avatar on right */
.character-card {
    background: #bdbad4 !important;
    background-color: #bdbad4 !important;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 3px 8px rgba(46, 40, 92, 0.15);
    transition: transform 0.2s, box-shadow 0.2s;
    border: 1px solid #bdbad4;
    height: 120px; /* 👈 固定高度 */
    display: flex; /* 👈 改为水平布局 */
    flex-direction: row; /* 👈 水平排列 */
    cursor: pointer;
    width: 320px; /* 👈 固定宽度，更宽以容纳水平布局 */
    margin: 0;
    flex: 0 0 auto;
}

.character-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(46, 40, 92, 0.25);
}

/* Remove card header - show student name directly */
.card-header {
    display: none;
}

/* 👈 NEW: Left content area for text */
.character-card-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 15px;
}

/* Student info styling - left aligned */
.student-name {
    font-size: 18px !important;
    font-weight: 900 !important;
    margin: 0 0 8px 0 !important;
    text-align: left !important; /* 👈 左对齐 */
    color: #2e285c !important;
    letter-spacing: 0.5px;
}

.student-description {
    text-align: left !important; /* 👈 左对齐 */
    color: #2e285c;
    font-size: 12px;
    line-height: 1.3;
    margin: 0 0 10px 0 !important;
    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
}

/* Hide model tag for cleaner interface */
.model-tag {
    display: none;
}

/* NEW: Avatar styling - positioned on the right side */
.character-card .avatar-container {
    width: 100px !important; /* 👈 固定宽度 */
    height: 100px !important; /* 👈 固定高度 */
    overflow: hidden !important;
    margin: 10px 15px 10px 0 !important; /* 👈 右边距，放在右侧 */
    border: 2px solid #2e285c !important;
    border-radius: 12px !important;
    box-shadow: 0 3px 6px rgba(46, 40, 92, 0.1) !important;
    background-color: transparent !important;
    flex-shrink: 0 !important; /* 👈 防止头像被压缩 */
}

.character-card .avatar-container img,
.character-card .avatar-container > div,
.character-card .avatar-img,
.character-card [data-testid="image"],
.character-card [data-testid="image"] > div {
    width: 100% !important;
    height: 100% !important;
    object-fit: cover !important;
    display: block !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    margin: 0 !important;
    padding: 0 !important;
    border-radius: 10px !important;
}

/* Chat button styling - positioned in content area */
.chat-btn {
    background-color: white !important;
    color: #2e285c !important;
    border: 2px solid #bdbad4 !important;
    border-radius: 16px !important;
    padding: 6px 12px !important;
    margin: 0 !important; /* 👈 移除margin，由父容器控制位置 */
    width: 80px !important; /* 👈 固定宽度 */
    display: block !important;
    font-weight: bold !important;
    cursor: pointer !important;
    font-size: 12px !important;
    transition: all 0.2s !important;
    align-self: flex-start !important; /* 👈 左对齐 */
}

.chat-btn:hover {
    background-color: #f0edfe !important;
    border-color: #2e285c !important;
}

/* Back button styling - 改成紫色 */
.back-btn {
    background-color: white !important;
    border: 2px solid #bdbad4 !important;
    color: #2e285c !important;
    border-radius: 8px !important;
    padding: 8px 16px !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    font-weight: bold !important;
}

.back-btn:hover {
    background-color: #f0edfe !important;
    border-color: #2e285c !important;
}

/* Input and buttons styling */
.message-input textarea {
    background-color: white !important;
    border: 1px solid #bdbad4 !important;
    border-radius: 20px !important;
    padding: 12px 16px !important;
    font-size: 14px !important;
    color: #2e285c !important;
    resize: none !important;
}

/* Button container for vertical layout */
.button-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
    width: 100%;
}

.send-btn {
    background-color: #bdbad4 !important;
    color: white !important;
    font-weight: bold !important;
    border-radius: 20px !important;
    padding: 8px 15px !important;
    width: 100% !important;
    border: none !important;
    cursor: pointer !important;
    transition: background-color 0.2s !important;
}

.send-btn:hover {
    background-color: #2e285c !important;
}

.clear-btn {
    background-color: white !important;
    color: #2e285c !important;
    font-weight: bold !important;
    border-radius: 20px !important;
    padding: 8px 15px !important;
    width: 100% !important;
    border: 2px solid #bdbad4 !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
}

.clear-btn:hover {
    background-color: #f0edfe !important;
    border-color: #2e285c !important;
}

/* Character.ai style chat container */
.character-ai-style {
    border-radius: 12px;
    background-color: white !important;
    box-shadow: 0 4px 12px rgba(46, 40, 92, 0.05);
}

/* Project description styling */
.project-description {
    text-align: center;
    margin: 0 auto 5px;
    max-width: 800px;
    color: #2e285c;
    font-size: 14px;
    line-height: 1.5;
    padding: 0 20px;
    font-style: italic;
}

/* Selection heading styling for clear hierarchy */
.selection-heading {
    text-align: center;
    margin: 1px 0 10px;
    color: #2e285c;
    font-size: 22px;
    font-weight: bold;
}

/* Container for main content with reasonable max width */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 24px;
    background-color: transparent !important;
}

/* 🎯 CRITICAL FIX: 页面背景修复 */
html, body, #root,
.gradio-app, .app, .main,
.gradio-container {
  background: #ffffff !important;
  background-color: #ffffff !important;
}

:root {
  --background-fill-primary: #ffffff !important;
  --background-fill-secondary: #ffffff !important;
  --block-background-fill: #ffffff !important;
  --panel-background-fill: #ffffff !important;
  --color-background: #ffffff !important;
  --color-background-secondary: #ffffff !important;
}

/* 确保所有dropdown和textbox有白色背景 */
.gradio-dropdown, 
.gradio-textbox,
.gradio-dropdown > div,
.gradio-textbox > div {
    background-color: white !important;
}

/* 确保所有表单元素有白色背景 */
select, textarea, input {
    background-color: white !important;
}

/* 🎯 Precise fix for chat page only */

/* 1. Fix left chat column height only on chat page */
.chat-page .chat-column,
.main-chat-container .chat-column {
    min-height: 1029px !important;
    height: auto !important;
    background-color: white !important;
    border-radius: 12px !important;
    padding: 20px !important;
    box-shadow: 0 4px 12px rgba(46, 40, 92, 0.1) !important;
    border: 1px solid #bdbad4 !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: space-between !important;
}

/* 确保聊天框在聊天页面占用大部分空间，并且可以随内容扩展 */
.main-chat-container .chat-column .gradio-chatbot {
    flex: 1 !important;
    min-height: 850px !important;
    max-height: none !important;
    overflow-y: auto !important;
}

/* 强制chatbot容器也跟着拉长 */
.main-chat-container .gradio-chatbot,
.chat-column .gradio-chatbot,
.gradio-chatbot,
[data-testid="chatbot"],
.chatbot-container {
    min-height: 850px !important;
    height: 850px !important;
    max-height: none !important;
    flex: 1 !important;
}

/* 更强力的chatbot内容区域控制 */
.gradio-chatbot > div,
.gradio-chatbot .chatbot,
.gradio-chatbot .chat-container,
.main-chat-container .gradio-chatbot > div {
    min-height: 850px !important;
    height: 850px !important;
    max-height: none !important;
}

/* 针对可能的chatbot wrapper */
.gradio-chatbot .overflow-y-auto,
.gradio-chatbot [class*="overflow"],
.gradio-chatbot [class*="scroll"] {
    min-height: 850px !important;
    height: 850px !important;
}

/* 确保输入框区域在聊天页面底部 */
.main-chat-container .chat-column > div:last-child {
    margin-top: auto !important;
    flex-shrink: 0 !important;
}

/* 2. Fix right info column only on chat page */
.chat-page .info-column > div,
.main-chat-container .info-column > div,
.chat-page .info-column .gr-box,
.chat-page .info-column .gradio-group {
    background-color: white !important;
    border-radius: 12px !important;
    padding: 20px !important;
    border: 1px solid #bdbad4 !important;
    box-shadow: 0 4px 12px rgba(46, 40, 92, 0.1) !important;
    margin-bottom: 20px !important;
}

/* 3. Fix text content only on chat page */
.chat-page .info-column div,
.chat-page .info-column p,
.chat-page .info-column span,
.main-chat-container .info-column .gr-markdown,
.main-chat-container .info-column .gradio-markdown {
    background-color: white !important;
    color: #2e285c !important;
}

/* 4. Fix input fields only on chat page */
.chat-page .info-column .gradio-dropdown,
.chat-page .info-column .gradio-textbox,
.main-chat-container .info-column select,
.main-chat-container .info-column textarea,
.main-chat-container .info-column input {
    background-color: white !important;
    border: 1px solid #bdbad4 !important;
    border-radius: 8px !important;
    color: #2e285c !important;
}

/* 5. Ensure selection page cards remain purple */
.selection-page .character-card,
.character-grid .character-card {
    background: #bdbad4 !important;
    background-color: #bdbad4 !important;
}

/* 6. Protect selection page from changes */
.selection-page *:not(.character-card) {
    background-color: transparent !important;
}

/* 7. More specific chat page targeting */
.main-chat-container .info-column *:not(img):not(.gradio-image) {
    background-color: white !important;
}

/* Responsive design for grouped layout */
@media (max-width: 1200px) {
    .main-chat-container {
        flex-direction: column;
    }
    
    .chat-column, .info-column {
        width: 100%;
    }
    
    .character-row {
        gap: 12px;
    }
    
    .character-card {
        width: 300px; /* 👈 调整宽度 */
    }
}

@media (max-width: 992px) {
    .character-row {
        justify-content: flex-start;
    }
    
    .character-card {
        width: 280px; /* 👈 进一步缩小 */
    }
    
    .age-group-container {
        padding: 15px;
    }
}

@media (max-width: 768px) {
    .main-chat-container {
        padding: 0 10px;
    }
    
    .profile-box, .instructions-box, .scene-box {
        padding: 15px;
    }
    
    .character-row {
        flex-direction: column;
        align-items: flex-start; /* 👈 左对齐 */
    }
    
    .character-card {
        width: 100%; /* 👈 全宽 */
        max-width: 400px;
    }
    
    .age-group-container {
        margin-bottom: 25px;
        padding: 12px;
    }
    
    .age-group-title {
        font-size: 20px !important;
    }
}

@media (max-width: 480px) {
    .main-groups-container {
        padding: 10px;
    }
    
    .character-card {
        width: 100%;
        max-width: none;
        height: auto; /* 👈 自动高度 */
        flex-direction: column; /* 👈 小屏幕时改为垂直布局 */
    }
    
    .character-card .avatar-container {
        width: 80px !important;
        height: 80px !important;
        margin: 10px auto !important;
    }
    
    .character-card-content {
        text-align: center;
    }
    
    .student-name {
        text-align: center !important;
    }
    
    .student-description {
        text-align: center !important;
    }
    
    .chat-btn {
        align-self: center !important;
    }
    
    .mental-health-group {
        padding: 10px;
    }
}
"""
