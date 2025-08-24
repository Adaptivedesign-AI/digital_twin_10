# custom_css.py
# 修复了语法错误的CSS文件

custom_css = """
/* =============================================================================
   全局样式和变量 - 采用成功的暴力覆盖策略
   ============================================================================= */
:root {
    --primary-purple: #2e285c;
    --light-purple: #bdbad4;
    --cream-bg: #FEFCF3;
    --hover-purple: #f0edfe;
    --border-radius: 12px;
    --shadow: 0 4px 12px rgba(46, 40, 92, 0.1);
}

/* 暴力覆盖所有可能的背景 - 但排除特定组件 */
html, body, #root, #app, .app, .main, 
.gradio-app, .gradio-container,
.gradio-container > div:not(.character-card):not(.profile-box):not(.instructions-box):not(.scene-box):not(.chat-column):not(.info-column),
[class*="gradio"]:not(.character-card):not(.profile-box):not(.instructions-box):not(.scene-box), 
[class*="svelte"]:not(.character-card):not(.profile-box):not(.instructions-box):not(.scene-box), 
[class*="block"]:not(.character-card):not(.profile-box):not(.instructions-box):not(.scene-box) {
    background-color: #FEFCF3 !important;
    font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
}

/* 强制覆盖body元素 */
body {
    background: #FEFCF3 !important;
    background-color: #FEFCF3 !important;
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
    background-color: #2e285c;
    color: white;
    padding: 15px;
    text-align: center;
    font-size: 24px;
    font-weight: bold;
    border-radius: 12px 12px 0 0;
    margin: 0;
}

.chat-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 15px 20px;
    background-color: #bdbad4 !important;
    color: white !important;
    border-radius: 12px 12px 0 0;
    margin-bottom: 20px;
    box-shadow: 0 4px 12px rgba(46, 40, 92, 0.1);
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
    color: #2e285c;
    font-size: 22px;
    font-weight: bold;
}

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
    background-color: #FEFCF3 !important;
}

.character-card {
    background: #bdbad4 !important;
    background-color: #bdbad4 !important;
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

/* 强制角色卡片内部保持紫色 */
.character-card *, 
.character-card > div,
.character-card .student-name,
.character-card .student-description {
    background-color: #bdbad4 !important;
}

/* 但文字区域需要透明背景以显示卡片颜色 */
.character-card .student-name,
.character-card .student-description {
    background-color: transparent !important;
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

/* =============================================================================
   按钮样式
   ============================================================================= */
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

.chat-btn:hover, .back-btn:hover, .clear-btn:hover {
    background-color: #f0edfe !important;
    border-color: #2e285c !important;
}

.back-btn, .clear-btn {
    background-color: white !important;
    border: 2px solid #bdbad4 !important;
    color: #2e285c !important;
    border-radius: 20px !important;
    padding: 8px 15px !important;
    width: 100% !important;
    cursor: pointer !important;
    font-weight: bold !important;
    transition: all 0.2s !important;
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

/* =============================================================================
   表单元素样式
   ============================================================================= */
select, textarea, input, .gradio-dropdown, .gradio-textbox,
.message-input textarea, .scene-dropdown select, 
.custom-scene-input textarea {
    background-color: white !important;
    border: 1px solid #bdbad4 !important;
    border-radius: 8px !important;
    padding: 10px !important;
    font-size: 14px !important;
    color: #2e285c !important;
}

.message-input textarea {
    border-radius: 20px !important;
    padding: 12px 16px !important;
    resize: none !important;
}

.scene-description textarea {
    background-color: #f0edfe !important;
    min-height: 60px;
}

/* =============================================================================
   聊天页面布局 - 右侧面板强制纯白色
   ============================================================================= */
.main-chat-container {
    gap: 20px !important;
    padding: 0 20px;
    max-width: 1400px;
    margin: 0 auto;
}

.chat-column {
    background-color: white !important;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 12px rgba(46, 40, 92, 0.1);
    border: 1px solid #bdbad4;
    min-height: 1029px !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: space-between !important;
}

.chat-column .gradio-chatbot {
    flex: 1 !important;
    min-height: 850px !important;
    height: 850px !important;
    background-color: white !important;
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

/* 强制右侧信息面板为纯白色 */
.info-column > div, .profile-box, .instructions-box, .scene-box {
    background-color: white !important;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 12px rgba(46, 40, 92, 0.1);
    border: 1px solid #bdbad4 !important;
}

/* 强制信息面板内部所有元素为白色背景 */
.info-column *, 
.profile-box *, 
.instructions-box *, 
.scene-box *,
.info-column > div *,
.info-column .gradio-group,
.info-column .gradio-group *,
.info-column .gr-markdown,
.info-column .gr-markdown * {
    background-color: white !important;
}

.profile-name, .section-title {
    color: #2e285c !important;
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
    color: #2e285c;
    margin: 0 !important;
}

/* =============================================================================
   响应式设计
   ============================================================================= */
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

/* =============================================================================
   隐藏元素
   ============================================================================= */
.card-header, .model-tag {
    display: none;
}
"""
