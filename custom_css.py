# custom_css.py
# CSS样式定义文件

custom_css = """
/* =============================================================================
   全局样式和变量
   ============================================================================= */
:root {
    --primary-purple: #2e285c;
    --light-purple: #bdbad4;
    --cream-bg: #FEFCF3;
    --hover-purple: #f0edfe;
    --border-radius: 12px;
    --shadow: 0 4px 12px rgba(46, 40, 92, 0.1);
    
    /* 覆盖 Gradio 系统变量（兼容所有主题系统） */
    --background-fill-primary: #FEFCF3 !important;
    --background-fill-secondary: #FEFCF3 !important;
    --block-background-fill: white !important;
    --panel-background-fill: white !important;
    --color-background: #FEFCF3 !important;
    --color-background-secondary: #FEFCF3 !important;
    --body-background-fill: #FEFCF3 !important;
}

/* 全局背景色 - 强制覆盖所有层级 */
html, body, #root, .gradio-app, .app, .main, .gradio-container,
.gradio-container > div, .gradio-container > div > div, 
.gradio-container > div > div > div,
.selection-page, .character-grid {
    background-color: var(--cream-bg) !important;
    font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
}

/* 统一 Gradio Block 背景为透明 */
.gr-block {
    background-color: transparent !important;
}

/* 移除图片容器的背景和边框 */
.header-image-container, .header-image-container > div, .header-image, 
.gradio-image, .gradio-image > div, [data-testid="image"], 
[class*="image"], img {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* =============================================================================
   页面头部样式
   ============================================================================= */
.main-title {
    background-color: var(--primary-purple);
    color: white;
    padding: 15px;
    text-align: center;
    font-size: 24px;
    font-weight: bold;
    border-radius: var(--border-radius) var(--border-radius) 0 0;
    margin: 0;
}

.chat-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 15px 20px;
    background-color: var(--light-purple) !important;
    color: white !important;
    border-radius: var(--border-radius) var(--border-radius) 0 0;
    margin-bottom: 20px;
    box-shadow: var(--shadow);
}

.page-title {
    color: white !important;
    margin: 0 !important;
    text-align: center;
    flex-grow: 1;
    font-weight: bold !important;
}

.selection-heading {
    text-align: center;
    margin: 1px 0 10px;
    color: var(--primary-purple);
    font-size: 22px;
    font-weight: bold;
}

.project-description {
    text-align: center;
    margin: 0 auto 5px;
    max-width: 800px;
    color: var(--primary-purple);
    font-size: 14px;
    line-height: 1.5;
    padding: 0 20px;
    font-style: italic;
}

/* =============================================================================
   聊天页面布局
   ============================================================================= */
.main-chat-container {
    gap: 20px !important;
    padding: 0 20px;
    max-width: 1400px;
    margin: 0 auto;
}

.chat-column {
    background-color: white;
    border-radius: var(--border-radius);
    padding: 20px;
    box-shadow: var(--shadow);
    border: 1px solid var(--light-purple);
    min-height: 1029px !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: space-between !important;
}

.chat-column .gradio-chatbot {
    flex: 1 !important;
    min-height: 850px !important;
    height: 850px !important;
}

.chat-column > div:last-child {
    margin-top: auto !important;
    flex-shrink: 0 !important;
}

.info-column {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.info-column > div, .profile-box, .instructions-box, .scene-box {
    background-color: white !important;
    border-radius: var(--border-radius);
    padding: 20px;
    box-shadow: var(--shadow);
    border: 1px solid var(--light-purple) !important;
}

.profile-name, .section-title {
    color: var(--primary-purple) !important;
    margin: 0 0 15px 0 !important;
    text-align: center;
    font-weight: bold !important;
}

.section-title {
    font-size: 18px !important;
}

.profile-text, .instructions-text, .scene-instruction {
    font-size: 14px;
    line-height: 1.6;
    color: var(--primary-purple);
    margin: 0 !important;
}

/* =============================================================================
   角色选择页面 - 网格布局
   ============================================================================= */
.character-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 20px;
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
}

.character-card {
    background: var(--light-purple) !important;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 4px 10px rgba(46, 40, 92, 0.15);
    transition: transform 0.2s, box-shadow 0.2s;
    border: 1px solid var(--light-purple);
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

.student-name {
    font-size: 20px !important;
    font-weight: 900 !important;
    margin: 15px 0 8px !important;
    text-align: center;
    color: var(--primary-purple) !important;
    letter-spacing: 0.5px;
}

.student-description {
    padding: 0 12px;
    text-align: center;
    color: var(--primary-purple);
    font-size: 13px;
    min-height: 45px;
    overflow: hidden;
    flex-grow: 1;
    margin-bottom: 8px;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
}

.character-card .avatar-container {
    width: 80% !important;
    height: 120px !important;
    overflow: hidden !important;
    margin: 20px auto 10px auto !important;
    border: 3px solid var(--light-purple) !important;
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

/* =============================================================================
   按钮样式
   ============================================================================= */
.chat-btn {
    background-color: white !important;
    color: var(--primary-purple) !important;
    border: 2px solid var(--light-purple) !important;
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

.chat-btn:hover, .back-btn:hover, .clear-btn:hover {
    background-color: var(--hover-purple) !important;
    border-color: var(--primary-purple) !important;
}

.back-btn, .clear-btn {
    background-color: white !important;
    border: 2px solid var(--light-purple) !important;
    color: var(--primary-purple) !important;
    border-radius: 20px !important;
    padding: 8px 15px !important;
    width: 100% !important;
    border: none !important;
    cursor: pointer !important;
    font-weight: bold !important;
    transition: all 0.2s !important;
}

.send-btn {
    background-color: var(--light-purple) !important;
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
    background-color: var(--primary-purple) !important;
}

/* =============================================================================
   表单元素样式
   ============================================================================= */
select, textarea, input, .gradio-dropdown, .gradio-textbox,
.message-input textarea, .scene-dropdown select, 
.custom-scene-input textarea {
    background-color: white !important;
    border: 1px solid var(--light-purple) !important;
    border-radius: 8px !important;
    padding: 10px !important;
    font-size: 14px !important;
    color: var(--primary-purple) !important;
}

.message-input textarea {
    border-radius: 20px !important;
    padding: 12px 16px !important;
    resize: none !important;
}

.scene-description textarea {
    background-color: var(--hover-purple) !important;
    min-height: 60px;
}

/* =============================================================================
   响应式设计
   ============================================================================= */
@media (max-width: 1200px) {
    .character-grid { grid-template-columns: repeat(4, 1fr); }
    .main-chat-container { flex-direction: column; }
    .chat-column, .info-column { width: 100%; }
}

@media (max-width: 992px) {
    .character-grid { grid-template-columns: repeat(3, 1fr); }
}

@media (max-width: 768px) {
    .character-grid { grid-template-columns: repeat(2, 1fr); }
    .main-chat-container { padding: 0 10px; }
    .profile-box, .instructions-box, .scene-box { padding: 15px; }
}

@media (max-width: 480px) {
    .character-grid { grid-template-columns: 1fr; }
}

/* =============================================================================
   隐藏元素
   ============================================================================= */
.card-header, .model-tag {
    display: none;
}
"""

# 如果你需要导出多个样式主题，可以这样定义：
digital_adolescents_theme = custom_css

# 也可以定义其他主题变体
dark_theme = """
:root {
    --primary-color: #1a1a1a;
    --cream-bg: #0f0f0f;
    /* ... 其他暗色主题变量 */
}
/* ... 暗色主题CSS */
"""
