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

/* Character.ai style grid for selection page - 5 columns by default */
.character-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 20px;
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
    background-color: transparent !important;
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

/* 重要：Card styling - 强制保持紫色背景 */
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
"""
# 在你的 custom_css 末尾添加这些强制规则：

additional_css = """

/* 🎯 强制修复聊天页面布局 */

/* 1. 强制左边聊天区域拉长 */
.main-chat-container .chat-column,
.gradio-container .chat-column,
div[class*="chat-column"] {
    min-height: 800px !important;
    height: auto !important;
    background-color: white !important;
    border-radius: 12px !important;
    padding: 20px !important;
    box-shadow: 0 4px 12px rgba(46, 40, 92, 0.1) !important;
    border: 1px solid #bdbad4 !important;
}

/* 2. 强制右边所有信息框白色背景 */
.info-column > div,
.info-column .gr-box,
.info-column .gradio-group,
div[class*="profile-box"],
div[class*="instructions-box"], 
div[class*="scene-box"] {
    background-color: white !important;
    border-radius: 12px !important;
    padding: 20px !important;
    border: 1px solid #bdbad4 !important;
    box-shadow: 0 4px 12px rgba(46, 40, 92, 0.1) !important;
    margin-bottom: 20px !important;
}

/* 3. 强制所有文字内容白色背景 */
.info-column div,
.info-column p,
.info-column span,
.info-column .gr-markdown,
.info-column .gradio-markdown {
    background-color: white !important;
    color: #2e285c !important;
}

/* 4. 强制右侧所有输入框白色背景 */
.info-column .gradio-dropdown,
.info-column .gradio-textbox,
.info-column select,
.info-column textarea,
.info-column input {
    background-color: white !important;
    border: 1px solid #bdbad4 !important;
    border-radius: 8px !important;
    color: #2e285c !important;
}

/* 5. 强制右侧所有容器白色背景 */
.info-column .gradio-dropdown > div,
.info-column .gradio-textbox > div,
.info-column .gradio-group > div,
.info-column .gr-form > div {
    background-color: white !important;
}

/* 6. 特别针对标题区域 */
.info-column h1,
.info-column h2, 
.info-column h3,
.info-column .section-title {
    background-color: white !important;
    color: #2e285c !important;
    padding: 10px !important;
    margin: 0 !important;
}

/* 7. 确保Profile信息完全白色 */
.profile-name,
.profile-text,
.student-name,
.student-description {
    background-color: white !important;
    color: #2e285c !important;
}

/* 8. 针对具体的gradio组件类名 */
.gr-box,
.gr-panel,
.gr-form,
.gradio-group,
.gradio-box {
    background-color: white !important;
}

/* 9. 强制覆盖任何灰色背景 */
.info-column * {
    background-color: white !important;
}

/* 10. 但排除图片 */
.info-column img,
.info-column .gradio-image {
    background-color: transparent !important;
}

"""

# 将这个添加到你的 custom_css 字符串末尾
custom_css = custom_css + additional_css
