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

/* Chat page header styling - 改成白色背景 */
.chat-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 15px 20px;
    border-bottom: 1px solid #bdbad4;
    background-color: white !important;
    color: #2e285c !important;
    border-radius: 12px 12px 0 0;
    margin-bottom: 20px;
    box-shadow: 0 2px 8px rgba(46, 40, 92, 0.1);
}

.page-title {
    color: #2e285c !important;
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
    min-height: 100vh !important;
    display: flex !important;
    flex-direction: column !important;
}

/* Right column: Information panels */
.info-column {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

/* Profile box styling - 移除边框，纯白色 */
.profile-box {
    background-color: white !important;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 12px rgba(46, 40, 92, 0.1);
    border: none !important;
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

/* Instructions box styling - 移除边框，纯白色 */
.instructions-box {
    background-color: white !important;
    border-radius: 12px;
    padding: 20px;
    border: none !important;
    box-shadow: 0 4px 12px rgba(46, 40, 92, 0.1);
}

.instructions-text {
    font-size: 14px;
    line-height: 1.6;
    color: #2e285c;
    margin: 0 !important;
}

/* Scene box styling - 移除边框，纯白色 */
.scene-box {
    background-color: white !important;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 12px rgba(46, 40, 92, 0.1);
    border: none !important;
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
}

.custom-scene-input textarea {
    border-radius: 8px;
    border: 1px solid #bdbad4;
    padding: 10px;
    font-size: 14px;
    min-height: 80px;
}

.scene-description textarea {
    border-radius: 8px;
    border: 1px solid #bdbad4;
    padding: 10px;
    font-size: 14px;
    background-color: #f0edfe;
    min-height: 60px;
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
    
    .main-chat-container {
        flex-direction: column;
    }
    
    .chat-column, .info-column {
        width: 100%;
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
    
    .main-chat-container {
        padding: 0 10px;
    }
    
    .profile-box, .instructions-box, .scene-box {
        padding: 15px;
    }
}

@media (max-width: 480px) {
    .character-grid {
        grid-template-columns: 1fr;
    }
}

/* Card styling - updated with purple theme */
.character-card {
    background: #bdbad4;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 4px 10px rgba(46, 40, 92, 0.15);
    transition: transform 0.2s, box-shadow 0.2s;
    border: 1px solid #bdbad4;
    height: 100%;
    display: flex;
    flex-direction: column;
    cursor: pointer;
    max-width: 220px;
    margin: 0 auto;
}

.character-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 16px rgba(46, 40, 92, 0.25);
}

/* Remove card header - show student name directly */
.card-header {
    display: none;
}

/* Student info styling - compact and readable */
.student-name {
    font-size: 20px !important;
    font-weight: 900 !important;
    margin: 15px 0 8px !important;
    text-align: center;
    color: #2e285c !important;
    letter-spacing: 0.5px;
}

.student-description {
    padding: 0 12px;
    text-align: center;
    color: #2e285c;
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

/* Avatar styling - circular and centered, 80% width */
.character-card .avatar-container {
    width: 80% !important;
    height: 120px !important;
    overflow: hidden !important;
    margin: 20px auto 10px auto !important;
    border: 3px solid #bdbad4 !important;
    border-radius: 50% !important;
    box-shadow: 0 4px 8px rgba(46, 40, 92, 0.1) !important;
    background-color: transparent !important;
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
}

/* Chat button styling - white background with purple text */
.chat-btn {
    background-color: white !important;
    color: #2e285c !important;
    border: 2px solid #bdbad4 !important;
    border-radius: 20px !important;
    padding: 8px 0 !important;
    margin: 10px auto 16px !important;
    width: 85% !important;
    display: block !important;
    font-weight: bold !important;
    cursor: pointer !important;
    font-size: 14px !important;
    transition: all 0.2s !important;
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

/* Chat avatar styling */
.gradio-chatbot .avatar img {
    width: 100% !important;
    height: 100% !important;
    border-radius: 50% !important;
    border: none !important;
    object-fit: cover !important;
}

/* Ensure avatars are visible and styled correctly */
.gradio-chatbot .message-wrap.user .avatar,
.gradio-chatbot .message-wrap.bot .avatar {
    display: inline-block !important;
    width: 48px !important;
    height: 48px !important;
    border-radius: 50% !important;
    overflow: hidden !important;
    margin-right: 8px !important;
    flex-shrink: 0 !important;
    box-shadow: none !important;
    border: 2px solid #bdbad4 !important;
    padding: 0 !important;
    background-color: transparent !important;
}

/* Chat bubbles: AI is purple with 50% transparency, user is white - 强制覆盖主题 */
.gradio-chatbot .message.bot,
.gradio-chatbot .message-wrap.bot .message,
.gradio-chatbot .bot .message,
.gradio-chatbot [data-testid="bot"] .message {
    background-color: rgba(189, 186, 212, 0.5) !important;
    color: #2e285c !important;
    border-bottom-left-radius: 6px !important;
    border-top-left-radius: 18px !important;
    border-top-right-radius: 18px !important;
    border-bottom-right-radius: 18px !important;
    margin-left: 12px !important;
    margin-right: auto !important;
    max-width: 80% !important;
    box-shadow: 0 1px 3px rgba(46, 40, 92, 0.1) !important;
    padding: 12px 16px !important;
    word-wrap: break-word !important;
    border: 1px solid rgba(189, 186, 212, 0.3) !important;
}

.gradio-chatbot .message.user,
.gradio-chatbot .message-wrap.user .message,
.gradio-chatbot .user .message,
.gradio-chatbot [data-testid="user"] .message {
    background-color: white !important;
    color: #2e285c !important;
    border-bottom-right-radius: 6px !important;
    border-top-left-radius: 18px !important;
    border-top-right-radius: 18px !important;
    border-bottom-left-radius: 18px !important;
    margin-right: 12px !important;
    margin-left: auto !important;
    max-width: 80% !important;
    border: 1px solid #bdbad4 !important;
    box-shadow: 0 1px 3px rgba(46, 40, 92, 0.05) !important;
    padding: 12px 16px !important;
    word-wrap: break-word !important;
}

/* 更强力的选择器覆盖主题颜色 */
.gradio-chatbot .message-row.bot .message,
.gradio-chatbot .message-row[data-testid="bot"] .message {
    background-color: rgba(189, 186, 212, 0.5) !important;
    color: #2e285c !important;
}

.gradio-chatbot .message-row.user .message,
.gradio-chatbot .message-row[data-testid="user"] .message {
    background-color: white !important;
    color: #2e285c !important;
}

/* Chat area overall background (white) */
.character-ai-style.chatbox-container {
    background-color: white !important;
    padding: 20px !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 12px rgba(46, 40, 92, 0.05) !important;
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

/* Chat avatar containers */
.gradio-chatbot .avatar-container {
    width: 48px !important;
    height: 48px !important;
    border-radius: 50% !important;
    overflow: hidden !important;
    border: 2px solid #bdbad4 !important;
    margin: 0 !important;
    padding: 0 !important;
    background-color: transparent !important;
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
}

/* Fix Gradio spacing issues */
.gradio-container {
    max-width: 100% !important;
}

/* Hide unnecessary margins in Gradio blocks */
.block {
    margin-bottom: 0 !important;
}

/* Avatar image styling to ensure it fills the container */
.gradio-chatbot .avatar-container img,
.gradio-chatbot .avatar img,
.gradio-chatbot img.avatar-image {
    width: 100% !important;
    height: 100% !important;
    object-fit: cover !important;
    border-radius: 50% !important;
    border: none !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* Remove image backgrounds - target all image and container elements */
.gradio-container .gradio-image, 
.gradio-container img, 
.gradio-container [data-testid="image"],
.gradio-container [class*="image"],
.gradio-container [class*="avatar"],
.character-card .gradio-image,
.character-card img,
.character-card [data-testid="image"] {
    background-color: transparent !important;
    background: transparent !important;
}

/* Override any image background styles with !important */
img, [data-testid="image"], [class*="image"] {
    background-color: transparent !important;
    background: transparent !important;
}

/* Additional fixes for Gradio's image component containers */
.gradio-image > div, .gradio-image > div > div, .gradio-image > div > img {
    background-color: transparent !important;
    background: transparent !important;
    box-shadow: none !important;
    border: none !important;
}

/* Profile image specific styling */
.profile-image img {
    border-radius: 12px !important;
    border: 2px solid #bdbad4 !important;
    width: 100% !important;
    height: 100% !important;
    object-fit: cover !important;
}

/* Additional profile box styling */
.profile-box .gradio-image {
    border-radius: 12px;
    overflow: hidden;
}

/* Ensure dropdown and textbox styling consistency */
.gradio-dropdown, .gradio-textbox {
    margin-bottom: 10px !important;
}

/* Custom scrollbar for chat area */
.gradio-chatbot::-webkit-scrollbar {
    width: 6px;
}

.gradio-chatbot::-webkit-scrollbar-track {
    background: #f0edfe;
    border-radius: 10px;
}

.gradio-chatbot::-webkit-scrollbar-thumb {
    background: #bdbad4;
    border-radius: 10px;
}

.gradio-chatbot::-webkit-scrollbar-thumb:hover {
    background: #2e285c;
}

/* 🎯 CRITICAL FIX: Remove white bars and fix gray background */
/* 1) 撤销"把所有直系子元素刷白"的副作用（避免白条） */
.gradio-container > * {
  background: transparent !important;
  background-color: transparent !important;
}

/* 2) 彻底把最外层背景改白（覆盖主题的 secondary 背景） */
html, body, #root,
.gradio-app, .app, .main,
.gradio-container {
  background: #ffffff !important;
  background-color: #ffffff !important;
}

/* 3) 同时覆盖可能使用的主题变量（不同 gradio 版本变量名略有差异） */
:root {
  --background-fill-primary: #ffffff !important;
  --background-fill-secondary: #ffffff !important;
  --block-background-fill: #ffffff !important;
  --panel-background-fill: #ffffff !important;

  /* 部分版本还用这些变量名 */
  --color-background: #ffffff !important;
  --color-background-secondary: #ffffff !important;
}

/* 彻底移除所有Gradio组件的默认样式 */
.gradio-container * {
    border-color: transparent !important;
}

/* 确保只有我们想要的元素有边框 */
.character-card, .profile-image, .avatar-container {
    border-color: #bdbad4 !important;
}
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

/* 你的其他所有现有 CSS 规则... */

/* 🎯 CRITICAL FIX: 在最后添加这些强制白色背景的规则 */

/* 1) 撤销"把所有直系子元素刷白"的副作用（避免白条） */
.gradio-container > * {
  background: transparent !important;
  background-color: transparent !important;
}

/* 2) 彻底把最外层背景改白（覆盖主题的 secondary 背景） */
html, body, #root,
.gradio-app, .app, .main,
.gradio-container {
  background: #ffffff !important;
  background-color: #ffffff !important;
}

/* 3) 同时覆盖可能使用的主题变量（不同 gradio 版本变量名略有差异） */
:root {
  --background-fill-primary: #ffffff !important;
  --background-fill-secondary: #ffffff !important;
  --block-background-fill: #ffffff !important;
  --panel-background-fill: #ffffff !important;
  
  /* 部分版本还用这些变量名 */
  --color-background: #ffffff !important;
  --color-background-secondary: #ffffff !important;
}

/* 确保所有容器都是白色背景 */
.gradio-container, .gradio-container > div {
  background: #ffffff !important;
  background-color: #ffffff !important;
}

/* 彻底移除所有Gradio组件的默认灰色样式 */
.gradio-container * {
    background-color: transparent !important;
}

/* 确保只有你想要的元素有背景色 */
.character-card, .profile-box, .instructions-box, .scene-box {
    background-color: white !important;
}
"""
