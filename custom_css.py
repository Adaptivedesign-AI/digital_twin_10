# custom_css.py
# 分层方案：第一步暴力背景，第二步精确元素

custom_css = """
/* =============================================================================
   第一层：暴力背景设定 - 所有东西都是米白色
   ============================================================================= */

/* 最暴力的背景覆盖 - 不管什么都先改成米白色 */
html, body, #root, div, span, section, article, main {
    background-color: #FEFCF3 !important;
}

/* Gradio所有容器都强制米白色 */
.gradio-container,
.gradio-container div,
.gradio-app,
.gradio-app div,
[class*="gradio"],
[class*="svelte"],
[data-testid],
[id*="component"] {
    background-color: #FEFCF3 !important;
}

/* 所有可能的wrapper和container */
[class*="container"],
[class*="wrapper"],
[class*="block"],
[class*="group"],
[class*="column"],
[class*="row"] {
    background-color: #FEFCF3 !important;
}

/* =============================================================================
   第二层：精确恢复需要的元素颜色和样式
   ============================================================================= */

/* 角色卡片 - 紫色背景 */
.character-card {
    background-color: #bdbad4 !important;
    border-radius: 16px !important;
    box-shadow: 0 4px 10px rgba(46, 40, 92, 0.15) !important;
    transition: transform 0.2s, box-shadow 0.2s !important;
    border: 1px solid #bdbad4 !important;
    height: 100% !important;
    display: flex !important;
    flex-direction: column !important;
    cursor: pointer !important;
    max-width: 220px !important;
    margin: 0 auto !important;
    overflow: hidden !important;
}

.character-card:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 16px rgba(46, 40, 92, 0.25) !important;
}

/* 角色卡片内的文字 - 透明背景让紫色透过来 */
.character-card .student-name,
.character-card .student-description,
.character-card div,
.character-card span,
.character-card p {
    background-color: transparent !important;
}

.student-name {
    font-size: 20px !important;
    font-weight: 900 !important;
    margin: 15px 0 8px !important;
    text-align: center !important;
    color: #2e285c !important;
    letter-spacing: 0.5px !important;
}

.student-description {
    padding: 0 12px !important;
    text-align: center !important;
    color: #2e285c !important;
    font-size: 13px !important;
    min-height: 45px !important;
    overflow: hidden !important;
    flex-grow: 1 !important;
    margin-bottom: 8px !important;
    display: -webkit-box !important;
    -webkit-line-clamp: 3 !important;
    -webkit-box-orient: vertical !important;
}

/* 头像容器 - 透明背景 */
.character-card .avatar-container,
.character-card .avatar-container div,
.character-card .avatar-container img {
    background-color: transparent !important;
}

.character-card .avatar-container {
    width: 80% !important;
    height: 120px !important;
    overflow: hidden !important;
    margin: 20px auto 10px auto !important;
    border: 3px solid #bdbad4 !important;
    border-radius: 50% !important;
    box-shadow: 0 4px 8px rgba(46, 40, 92, 0.1) !important;
}

.character-card .avatar-container img {
    width: 100% !important;
    height: 100% !important;
    object-fit: cover !important;
    border: none !important;
}

/* 按钮 - 白色背景 */
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

/* =============================================================================
   第三层：聊天页面的白色面板
   ============================================================================= */

/* 聊天页面头部 - 紫色 */
.chat-header {
    background-color: #bdbad4 !important;
    color: white !important;
    padding: 15px 20px !important;
    border-radius: 12px 12px 0 0 !important;
    margin-bottom: 20px !important;
    box-shadow: 0 4px 12px rgba(46, 40, 92, 0.1) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
}

.page-title {
    color: white !important;
    margin: 0 !important;
    text-align: center !important;
    flex-grow: 1 !important;
    font-weight: bold !important;
}

/* 聊天区域 - 白色背景 */
.chat-column {
    background-color: white !important;
    border-radius: 12px !important;
    padding: 20px !important;
    box-shadow: 0 4px 12px rgba(46, 40, 92, 0.1) !important;
    border: 1px solid #bdbad4 !important;
}

/* 右侧信息面板 - 白色背景 */
.info-column > div {
    background-color: white !important;
    border-radius: 12px !important;
    padding: 20px !important;
    box-shadow: 0 4px 12px rgba(46, 40, 92, 0.1) !important;
    border: 1px solid #bdbad4 !important;
    margin-bottom: 20px !important;
}

/* 信息面板内的文字保持白色背景 */
.info-column div,
.info-column span,
.info-column p {
    background-color: white !important;
}

/* =============================================================================
   第四层：布局和响应式
   ============================================================================= */

/* 角色网格布局 */
.character-grid {
    background-color: transparent !important;
    display: grid !important;
    grid-template-columns: repeat(5, 1fr) !important;
    gap: 20px !important;
    padding: 20px !important;
    max-width: 1200px !important;
    margin: 0 auto !important;
}

/* 页面标题 - 透明背景 */
.selection-heading {
    background-color: transparent !important;
    text-align: center !important;
    margin: 1px 0 10px !important;
    color: #2e285c !important;
    font-size: 22px !important;
    font-weight: bold !important;
}

.project-description {
    background-color: transparent !important;
    text-align: center !important;
    margin: 0 auto 5px !important;
    max-width: 800px !important;
    color: #2e285c !important;
    font-size: 14px !important;
    line-height: 1.5 !important;
    padding: 0 20px !important;
    font-style: italic !important;
}

/* 响应式设计 */
@media (max-width: 1200px) {
    .character-grid { grid-template-columns: repeat(4, 1fr) !important; }
}

@media (max-width: 992px) {
    .character-grid { grid-template-columns: repeat(3, 1fr) !important; }
}

@media (max-width: 768px) {
    .character-grid { grid-template-columns: repeat(2, 1fr) !important; }
}

@media (max-width: 480px) {
    .character-grid { grid-template-columns: 1fr !important; }
}

/* 隐藏不需要的元素 */
.card-header, .model-tag {
    display: none !important;
}
"""
