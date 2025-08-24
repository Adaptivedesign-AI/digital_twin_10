# custom_css.py
# 专门为你的Digital Adolescents项目设计的CSS

custom_css = """
/* =============================================================================
   页面背景修复 - 简单直接
   ============================================================================= */
body {
    background-color: #FEFCF3 !important;
}

.gradio-container {
    background-color: #FEFCF3 !important;
}

/* =============================================================================
   你的角色选择页面
   ============================================================================= */
.character-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 20px;
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
    background-color: transparent;
}

.character-card {
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

/* 头像样式 */
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

.character-card .avatar-container img {
    width: 100% !important;
    height: 100% !important;
    object-fit: cover !important;
    background-color: transparent !important;
    border: none !important;
}

/* =============================================================================
   你的聊天页面
   ============================================================================= */
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

/* 右侧信息面板为白色 */
.info-column > div {
    background-color: white !important;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 12px rgba(46, 40, 92, 0.1);
    border: 1px solid #bdbad4 !important;
    margin-bottom: 20px;
}

.profile-name, .section-title {
    color: #2e285c !important;
    margin: 0 0 15px 0 !important;
    text-align: center;
    font-weight: bold !important;
}

/* 左侧聊天区域也是白色 */
.chat-column {
    background-color: white !important;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 12px rgba(46, 40, 92, 0.1);
    border: 1px solid #bdbad4;
}

/* =============================================================================
   页面标题样式
   ============================================================================= */
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
"""
