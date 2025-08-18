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
   NEW COMPACT CARD-BASED LAYOUT
============================================ */

/* Age group containers */
.age-group {
    background-color: #f8f9fc !important;
    border-radius: 16px !important;
    padding: 25px !important;
    margin: 20px 0 !important;
    border: 2px solid #e6e8f2 !important;
}

.age-group-title {
    color: #2e285c !important;
    margin: 0 0 20px 0 !important;
    text-align: center !important;
    font-weight: bold !important;
    font-size: 24px !important;
    border-bottom: 2px solid #bdbad4 !important;
    padding-bottom: 10px !important;
}

/* Mental health subgroups */
.mental-health-subgroup {
    background-color: white !important;
    border-radius: 12px !important;
    padding: 20px !important;
    margin: 15px 0 !important;
    border: 1px solid #bdbad4 !important;
    box-shadow: 0 2px 8px rgba(46, 40, 92, 0.05) !important;
}

.subgroup-title {
    color: #2e285c !important;
    margin: 0 0 15px 0 !important;
    font-weight: 600 !important;
    font-size: 18px !important;
    text-align: center !important;
}

.mental-health-issues {
    border-left: 4px solid #dc3545 !important;
    padding-left: 15px !important;
}

.no-mental-health-issues {
    border-left: 4px solid #28a745 !important;
    padding-left: 15px !important;
}

/* Student cards container */
.student-cards-container {
    display: flex !important;
    flex-direction: column !important;
    gap: 12px !important;
}

/* Individual student card row */
.student-card-row {
    background-color: #fafbfd !important;
    border: 1px solid #e6e8f2 !important;
    border-radius: 12px !important;
    padding: 15px !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
    display: flex !important;
    align-items: center !important;
    gap: 15px !important;
}

.student-card-row:hover {
    background-color: #f0f2f8 !important;
    border-color: #bdbad4 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(46, 40, 92, 0.1) !important;
}

/* Avatar column in card */
.avatar-column {
    flex-shrink: 0 !important;
    width: 80px !important;
}

.card-avatar {
    width: 80px !important;
    height: 80px !important;
    border-radius: 12px !important;
    border: 2px solid #bdbad4 !important;
    object-fit: cover !important;
    background-color: white !important;
}

.card-avatar img {
    width: 100% !important;
    height: 100% !important;
    object-fit: cover !important;
    border-radius: 10px !important;
}

/* Info column in card */
.info-column-card {
    flex-grow: 1 !important;
    display: flex !important;
    flex-direction: column !important;
    gap: 8px !important;
}

.card-student-name {
    color: #2e285c !important;
    margin: 0 !important;
    font-weight: bold !important;
    font-size: 18px !important;
}

.card-student-info {
    color: #666 !important;
    margin: 0 !important;
    font-size: 14px !important;
    line-height: 1.4 !important;
}

.card-chat-btn {
    background-color: #bdbad4 !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 8px 16px !important;
    font-weight: bold !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    align-self: flex-start !important;
    font-size: 14px !important;
}

.card-chat-btn:hover {
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
    margin: 0 auto 25px;
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
    font-size: 22px;
    font-weight: bold;
}

/* Container for main content */
.container {
    max-width: 900px;
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

.gradio-chatbot .overflow-y-auto,
.gradio-chatbot [class*="overflow"],
.gradio-chatbot [class*="scroll"] {
    min-height: 850px !important;
    height: 850px !important;
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
    margin-bottom: 20px !important;
}

.main-chat-container .info-column .gr-markdown,
.main-chat-container .info-column .gradio-markdown {
    background-color: white !important;
    color: #2e285c !important;
}

.main-chat-container .info-column select,
.main-chat-container .info-column textarea,
.main-chat-container .info-column input {
    background-color: white !important;
    border: 1px solid #bdbad4 !important;
    border-radius: 8px !important;
    color: #2e285c !important;
}

/* Remove old grid styles for selection page */
.character-grid {
    display: none !important;
}

.character-card {
    display: none !important;
}

/* Responsive design */
@media (max-width: 768px) {
    .container {
        padding: 0 15px;
        max-width: 100%;
    }
    
    .age-group {
        padding: 15px !important;
        margin: 15px 0 !important;
    }
    
    .mental-health-subgroup {
        padding: 15px !important;
    }
    
    .student-card-row {
        flex-direction: column !important;
        text-align: center !important;
        gap: 10px !important;
    }
    
    .avatar-column {
        width: 100% !important;
    }
    
    .card-avatar {
        width: 60px !important;
        height: 60px !important;
        margin: 0 auto !important;
    }
    
    .main-chat-container {
        flex-direction: column;
        padding: 0 10px;
    }
    
    .chat-column, .info-column {
        width: 100%;
    }
    
    .age-group-title {
        font-size: 20px !important;
    }
    
    .subgroup-title {
        font-size: 16px !important;
    }
}

@media (max-width: 1200px) {
    .main-chat-container {
        flex-direction: column;
    }
    
    .chat-column, .info-column {
        width: 100%;
    }
}
"""
