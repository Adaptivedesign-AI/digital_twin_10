# custom_css.py
# 核弹级方案 - 强制覆盖所有可能的背景

custom_css = """
/* =============================================================================
   智能背景覆盖 - 保护重要元素
   ============================================================================= */

/* 强制页面背景为米白色 */
html, body, #root {
    background: #FEFCF3 !important;
    background-color: #FEFCF3 !important;
}

/* Gradio容器背景覆盖 */
.gradio-container,
.gradio-app,
[class*="gradio"]:not(.character-card),
[class*="svelte"]:not(.character-card) {
    background: #FEFCF3 !important;
    background-color: #FEFCF3 !important;
}

/* 然后恢复需要特定颜色的元素 */
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

.character-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 16px rgba(46, 40, 92, 0.25);
}

/* 聊天页面的白色面板 - 保持白色但添加边框和阴影 */
.chat-column {
    background: white !important;
    background-color: white !important;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 12px rgba(46, 40, 92, 0.1);
    border: 1px solid #bdbad4;
}

.info-column > div {
    background: white !important;
    background-color: white !important;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 12px rgba(46, 40, 92, 0.1);
    border: 1px solid #bdbad4;
    margin-bottom: 20px;
}

/* 紫色头部 */
.chat-header {
    background: #bdbad4 !important;
    background-color: #bdbad4 !important;
    color: white !important;
    padding: 15px 20px;
    border-radius: 12px 12px 0 0;
    margin-bottom: 20px;
    box-shadow: 0 4px 12px rgba(46, 40, 92, 0.1);
}

/* 按钮样式 */
.chat-btn {
    background: white !important;
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
    background: #f0edfe !important;
    background-color: #f0edfe !important;
    border-color: #2e285c !important;
}

/* 文字样式 */
.student-name {
    background: transparent !important;
    background-color: transparent !important;
    font-size: 20px !important;
    font-weight: 900 !important;
    margin: 15px 0 8px !important;
    text-align: center;
    color: #2e285c !important;
    letter-spacing: 0.5px;
}

.student-description {
    background: transparent !important;
    background-color: transparent !important;
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

/* 头像容器 */
.character-card .avatar-container {
    background: transparent !important;
    background-color: transparent !important;
    width: 80% !important;
    height: 120px !important;
    overflow: hidden !important;
    margin: 20px auto 10px auto !important;
    border: 3px solid #bdbad4 !important;
    border-radius: 50% !important;
    box-shadow: 0 4px 8px rgba(46, 40, 92, 0.1) !important;
}

.character-card .avatar-container img {
    background: transparent !important;
    background-color: transparent !important;
    width: 100% !important;
    height: 100% !important;
    object-fit: cover !important;
    border: none !important;
}

/* 网格布局 */
.character-grid {
    background: transparent !important;
    background-color: transparent !important;
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 20px;
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
}

/* 页面标题 */
.selection-heading {
    background: transparent !important;
    background-color: transparent !important;
    text-align: center;
    margin: 1px 0 10px;
    color: #2e285c;
    font-size: 22px;
    font-weight: bold;
}

.project-description {
    background: transparent !important;
    background-color: transparent !important;
    text-align: center;
    margin: 0 auto 5px;
    max-width: 800px;
    color: #2e285c;
    font-size: 14px;
    line-height: 1.5;
    padding: 0 20px;
    font-style: italic;
}

/* 响应式 */
@media (max-width: 1200px) {
    .character-grid { grid-template-columns: repeat(4, 1fr); }
}
@media (max-width: 992px) {
    .character-grid { grid-template-columns: repeat(3, 1fr); }
}
@media (max-width: 768px) {
    .character-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 480px) {
    .character-grid { grid-template-columns: 1fr; }
}
"""
