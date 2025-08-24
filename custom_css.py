# custom_css.py  
# 精确打击方案 - 只修复背景，保护卡片内容

custom_css = """
/* =============================================================================
   精确背景修复 - 只针对页面容器，不影响卡片内容
   ============================================================================= */

/* 页面最外层背景 */
html, body {
    background-color: #FEFCF3 !important;
}

/* 只针对Gradio的主容器，不影响其内容 */
.gradio-container {
    background-color: #FEFCF3 !important;
}

/* 只针对可能的页面背景容器，不用通配符 */
.gradio-app {
    background-color: #FEFCF3 !important;
}

/* =============================================================================
   完整的角色卡片定义 - 一次性设置所有样式
   ============================================================================= */

/* 角色网格布局 */
.character-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 20px;
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
    background-color: transparent;
}

/* 完整的角色卡片样式 */
.character-card {
    background-color: #bdbad4;
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

/* 学生姓名样式 */
.student-name {
    background-color: transparent;
    font-size: 20px;
    font-weight: 900;
    margin: 15px 0 8px;
    text-align: center;
    color: #2e285c;
    letter-spacing: 0.5px;
}

/* 学生描述样式 */
.student-description {
    background-color: transparent;
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
    background-color: transparent;
    width: 80%;
    height: 120px;
    overflow: hidden;
    margin: 20px auto 10px auto;
    border: 3px solid #bdbad4;
    border-radius: 50%;
    box-shadow: 0 4px 8px rgba(46, 40, 92, 0.1);
}

.character-card .avatar-container img {
    background-color: transparent;
    width: 100%;
    height: 100%;
    object-fit: cover;
    border: none;
}

/* 聊天按钮 */
.chat-btn {
    background-color: white;
    color: #2e285c;
    border: 2px solid #bdbad4;
    border-radius: 20px;
    padding: 8px 0;
    margin: 10px auto 16px;
    width: 85%;
    display: block;
    font-weight: bold;
    cursor: pointer;
    font-size: 14px;
    transition: all 0.2s;
}

.chat-btn:hover {
    background-color: #f0edfe;
    border-color: #2e285c;
}

/* =============================================================================
   聊天页面样式
   ============================================================================= */

/* 聊天页面头部 */
.chat-header {
    background-color: #bdbad4;
    color: white;
    padding: 15px 20px;
    border-radius: 12px 12px 0 0;
    margin-bottom: 20px;
    box-shadow: 0 4px 12px rgba(46, 40, 92, 0.1);
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.page-title {
    color: white;
    margin: 0;
    text-align: center;
    flex-grow: 1;
    font-weight: bold;
}

/* 聊天区域 */
.chat-column {
    background-color: white;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 12px rgba(46, 40, 92, 0.1);
    border: 1px solid #bdbad4;
}

/* 右侧信息面板 */
.info-column > div {
    background-color: white;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 12px rgba(46, 40, 92, 0.1);
    border: 1px solid #bdbad4;
    margin-bottom: 20px;
}

/* =============================================================================
   页面标题和描述
   ============================================================================= */

.selection-heading {
    background-color: transparent;
    text-align: center;
    margin: 1px 0 10px;
    color: #2e285c;
    font-size: 22px;
    font-weight: bold;
}

.project-description {
    background-color: transparent;
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
   响应式设计
   ============================================================================= */

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

/* =============================================================================
   如果还有灰色背景，用这个终极方案
   ============================================================================= */

/* 只在必要时使用 - 针对可能遗漏的Gradio容器 */
[data-testid*="block"],
[class*="gradio-container"] {
    background-color: #FEFCF3 !important;
}

/* 但保护角色卡片不被影响 */
.character-card,
.character-card * {
    background-color: inherit !important;
}

.character-card {
    background-color: #bdbad4 !important;
}
"""
