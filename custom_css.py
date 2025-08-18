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

/* Chat page header styling */
.chat-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 15px 20px;
    border-bottom: 1px solid #bdbad4;
    background-color: #bdbad4 !important;
    color: white !important;
    border-radius: 12px 12px 0 0;
    margin-bottom: 20px;
    box-shadow: 0 2px 8px rgba(46, 40, 92, 0.1);
}

.page-title {
    color: white !important;
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

/* Left column: Chat interface */
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

.chat-column .gradio-chatbot {
    flex: 1 !important;
    min-height: 1150px !important;
}

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

/* Profile box styling */
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

/* Instructions box styling */
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

/* Scene box styling */
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

/* ============================================
   CHARACTER.AI STYLE TRUE HORIZONTAL LAYOUT
============================================ */

/* Age section titles - smaller and left aligned */
.age-section-title {
    color: #2e285c !important;
    margin: 30px 0 15px 0 !important;
    text-align: left !important;
    font-weight: bold !important;
    font-size: 20px !important;
    border-bottom: 2px solid #bdbad4 !important;
    padding-bottom: 8px !important;
}

/* Health section labels - small left-aligned text */
.health-section-label {
    color: #666 !important;
    margin: 15px 0 10px 0 !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    text-align: left !important;
    padding-left: 10px !important;
}

.mental-issues {
    border-left: 3px solid #dc3545 !important;
    background: rgba(220, 53, 69, 0.05) !important;
    padding: 5px 0 5px 10px !important;
    border-radius: 0 4px 4px 0 !important;
}

.no-mental-issues {
    border-left: 3px solid #28a745 !important;
    background: rgba(40, 167, 69, 0.05) !important;
    padding: 5px 0 5px 10px !important;
    border-radius: 0 4px 4px 0 !important;
}

/* Students row - horizontal layout 5 per row */
.students-row {
    display: flex !important;
    gap: 15px !important;
    margin: 10px 0 !important;
    justify-content: flex-start !important;
    align-items: stretch !important;
}

/* Student card wrapper */
.student-card-wrapper {
    flex: 1 !important;
    min-width: 0 !important;
    max-width: calc(20% - 12px) !important;
}

/* Horizontal student card */
.student-card-horizontal {
    background-color: #f8f9fa !important;
    border: 1px solid #dee2e6 !important;
    border-radius: 8px !important;
    padding: 12px !important;
    margin: 0 !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
    height: 100px !important;
    display: flex !important;
    align-items: center !important;
    gap: 12px !important;
}

.student-card-horizontal:hover {
    background-color: #e9ecef !important;
    border-color: #bdbad4 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 12px rgba(46, 40, 92, 0.1) !important;
}

/* Avatar section */
.avatar-section {
    flex-shrink: 0 !important;
    width: 60px !important;
}

/* Square avatar with rounded corners */
.square-avatar {
    width: 60px !important;
    height: 60px !important;
    border-radius: 8px !important;
    border: 2px solid #bdbad4 !important;
    object-fit: cover !important;
    background-color: white !important;
}

.square-avatar img {
    width: 100% !important;
    height: 100% !important;
    object-fit: cover !important;
    border-radius: 6px !important;
}

/* Info section */
.info-section {
    flex-grow: 1 !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    min-width: 0 !important;
}

/* Student name in horizontal layout */
.student-name-horizontal {
    color: #2e285c !important;
    margin: 0 0 4px 0 !important;
    font-weight: bold !important;
    font-size: 16px !important;
    line-height: 1.2 !important;
}

/* Student info in horizontal layout */
.student-info-horizontal {
    color: #666 !important;
    margin: 0 0 8px 0 !important;
    font-size: 12px !important;
    line-height: 1.2 !important;
}

/* Chat button in horizontal layout */
.chat-btn-horizontal {
    background-color: #bdbad4 !important;
    color: white !important;
    border: none !important;
    border-radius: 4px !important;
    padding: 4px 8px !important;
    font-weight: bold !important;
    cursor: pointer !important;
    font-size: 11px !important;
    transition: all 0.2s !important;
    align-self: flex-start !important;
    width: auto !important;
}

.chat-btn-horizontal:hover {
    background-color: #2e285c !important;
    transform: translateY(-1px) !important;
}

/* Back button styling */
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
    margin: 0 auto 30px;
    max-width: 800px;
    color: #2e285c;
    font-size: 14px;
    line-height: 1.5;
    padding: 0 20px;
    font-style: italic;
}

/* Selection heading styling */
.selection-heading {
    text-align: center;
    margin: 1px 0 10px;
    color: #2e285c;
    font-size: 24px;
    font-weight: bold;
}

/* Container for main content */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 24px;
    background-color: transparent !important;
}

/* Page background fixes */
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

/* Ensure dropdowns and textboxes have white backgrounds */
.gradio-dropdown, 
.gradio-textbox,
.gradio-dropdown > div,
.gradio-textbox > div {
    background-color: white !important;
}

select, textarea, input {
    background-color: white !important;
}

/* Chat page specific fixes */
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

.main-chat-container .chat-column .gradio-chatbot {
    flex: 1 !important;
    min-height: 850px !important;
    max-height: none !important;
    overflow-y: auto !important;
}

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

.gradio-chatbot > div,
.gradio-chatbot .chatbot,
.gradio-chatbot .chat-container,
.main-chat-container .gradio-chatbot > div {
    min-height: 850px !important;
    height: 850px !important;
    max-height: none !important;
}

.main-chat-container .chat-column > div:last-child {
    margin-top: auto !important;
    flex-shrink: 0 !important;
}

.main-chat-container .info-column > div,
.main-chat-container .info-column .gr-box,
.main-chat-container .info-column .gradio-group {
    background-color: white !important;
    border-radius: 12px !important;
    padding: 20px !important;
    border: 1px solid #bdbad4 !important;
    box-shadow: 0 4px 12px rgba(46, 40, 92, 0.1) !important;
