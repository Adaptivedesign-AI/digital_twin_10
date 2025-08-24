# custom_css.py
# 简化版 - 直接有效的修复方案

custom_css = """
/* =============================================================================
   页面背景 - 简单暴力但有效
   ============================================================================= */
html, body, #root, .gradio-container {
    background-color: #FEFCF3 !important;
}

/* 强制页面背景覆盖 - 学习你朋友的成功方法 */
.gradio-container *, 
[class*="gradio"], [class*="svelte"], [class*="block"] {
    background-color: #FEFCF3 !important;
}

/* =============================================================================
   角色卡片 - 紫色背景恢复
   ============================================================================= */
.character-card {
    background: #bdbad4 !important;
    background-color: #bdbad4 !important;
    border-radius: 16px;
    box-shadow: 0 4px 10px rgba(46, 40, 92, 0.15);
    transition: transform 0.2s, box-shadow 0.2s;
    border: 1px solid #bdbad4;
    height: 100%;
    display: flex;
    flex-direction: column;
    cursor: pointer;
    max-width: 220px;
    margin: 0 auto;
    overflow: hidden;
}

.character-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 16px rgba(46, 40, 92, 0.25);
}

/* 角色卡片网格 */
.character-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 20px;
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
    background-color: #FEFCF3 !important;
}

/* 角色卡片内容样式 */
.student-name {
    background-color: transparent !important;
    font-size: 20px !important;
    font-weight: 900 !important;
    margin: 15px 0 8px !important;
    text-align: center;
    color: #2e285c !important;
    letter-spacing: 0.5px;
}

.student-description {
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
    background-color: transparent !important;
    width: 80% !important;
    height: 120px !important;
    overflow: hidden !important;
    margin: 20px auto 10px auto !important;
    border: 3px solid #bdbad4 !important;
    border-radius: 50% !important;
    box-shadow: 0 4px 8px rgba(46, 40, 92, 0.1) !important;
}

.character-card .avatar-container img,
.character-card .avatar-container > div,
.character-card [data-testid="image"] {
    background-color: transparent !important;
    width: 100% !important;
    height: 100% !important;
    object-fit: cover !important;
    border: none !important;
}

/* =============================================================================
   聊天按钮
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

.chat-btn:hover {
    background-color: #f0edfe !important;
    border-color: #2e285c !important;
}

/* =============================================================================
   聊天页面 - 右侧面板纯白
   ============================================================================= */
.chat-column {
    background-color: white !important;
}

.info-column > div,
.profile-box, 
.instructions-box, 
.scene-box {
    background-color: white !important;
    border-radius: 12px !important;
    padding: 20px !important;
    box-shadow: 0 4px 12px rgba(46, 40, 92, 0.1) !important;
    border: 1px solid #bdbad4 !important;
    margin-bottom: 20px !important;
}

/* 页面头部样式 */
.main-title {
    background-color: #2e285c !important;
    color: white !important;
    padding: 15px !important;
    text-align: center !important;
    font-size: 24px !important;
    font-weight: bold !important;
    border-radius: 12px 12px 0 0 !important;
    margin: 0 !important;
}

.chat-header {
    background-color: #bdbad4 !important;
    color: white !important;
    padding: 15px 20px !important;
    border-radius: 12px 12px 0 0 !important;
    margin-bottom: 20px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
}

.page-title {
    color: white !important;
    font-weight: bold !important;
    margin: 0 !important;
    flex-grow: 1 !important;
    text-align: center !important;
}

.selection-heading {
    text-align: center !important;
    margin: 1px 0 10px !important;
    color: #2e285c !important;
    font-size: 22px !important;
    font-weight: bold !important;
}

.project-description {
    text-align: center !important;
    margin: 0 auto 5px !important;
    max-width: 800px !important;
    color: #2e285c !important;
    font-size: 14px !important;
    line-height: 1.5 !important;
    padding: 0 20px !important;
    font-style: italic !important;
}

/* 移除图片背景 */
.header-image-container, .gradio-image, [data-testid="image"], img {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
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

/* 隐藏不需要的元素 */
.card-header, .model-tag {
    display: none;
}
"""
