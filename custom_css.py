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
   CHARACTER.AI STYLE HORIZONTAL LAYOUT
============================================ */

/* Age group titles */
.age-group-title {
    color: #2e285c !important;
    margin: 40px 0 20px 0 !important;
    text-align: center !important;
    font-weight: bold !important;
    font-size: 28px !important;
    border-bottom: 3px solid #bdbad4 !important;
    padding-bottom: 15px !important;
}

/* Subgroup titles with color coding */
.subgroup-title {
    color: #2e285c !important;
    margin: 30px 0 20px 0 !important;
    font-weight: 600 !important;
    font-size: 20px !important;
    text-align: left !important;
    padding-left: 15px !important;
}

.mental-health-issues {
    border-left: 5px solid #dc3545 !important;
    background: linear-gradient(90deg, rgba(220, 53, 69, 0.1) 0%, transparent 100%) !important;
    padding: 10px 0 10px 15px !important;
    border-radius: 0 8px 8px 0 !important;
}

.no-mental-health-issues {
    border-left: 5px solid #28a745 !important;
    background: linear-gradient(90deg, rgba(40, 167, 69, 0.1) 0%, transparent 100%) !important;
    padding: 10px 0 10px 15px !important;
    border-radius: 0 8px 8px 0 !important;
}

/* Character grid row - horizontal layout like Character.AI */
.character-grid-row {
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 20px !important;
    justify-content: flex-start !important;
    align-items: stretch !important;
    margin: 0 0 30px 0 !important;
    padding: 0 !important;
}

/* Individual character cards - Character.AI style */
.character-card {
    background: #bdbad4 !important;
    background-color: #bdbad4 !important;
    border-radius: 16px !important;
    overflow: hidden !important;
    box-shadow: 0 4px 12px rgba(46, 40, 92, 0.15) !important;
    transition: all 0.3s ease !important;
    border: 2px solid transparent !important;
    height: auto !important;
    display: flex !important;
    flex-direction: column !important;
    cursor: pointer !important;
    width: 220px !important;
    min-height: 320px !important;
    flex-shrink: 0 !important;
}

.character-card:hover {
    transform: translateY(-5px) !important;
    box-shadow: 0 8px 20px rgba(46, 40, 92, 0.25) !important;
    border-color: #2e285c !important;
}

/* Avatar styling - circular and centered */
.character-card .avatar-container {
    width: 80% !important;
    height: 140px !important;
    overflow: hidden !important;
    margin: 20px auto 15px auto !important;
    border: 3px solid white !important;
    border-radius: 50% !important;
    box-shadow: 0 4px 12px rgba(46, 40, 92, 0.2) !important;
    background-color: white !important;
    position: relative !important;
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
    background-color: white !important;
    border: none !important;
    box-shadow: none !important;
    margin: 0 !important;
    padding: 0 !important;
    border-radius: 50% !important;
}

/* Student info styling - compact and readable */
.student-name {
    font-size: 22px !important;
    font-weight: 900 !important;
    margin: 0 0 10px !important;
    text-align: center !important;
    color: white !important;
    letter-spacing: 0.5px !important;
    text-shadow: 0 1px 2px rgba(0,0,0,0.1) !important;
}

.student-description {
    padding: 0 15px !important;
    text-align: center !important;
    color: white !important;
    font-size: 14px !important;
    line-height: 1.4 !important;
    min-height: 50px !important;
    overflow: hidden !important;
    flex-grow: 1 !important;
    margin-bottom: 15px !important;
    display: -webkit-box !important;
    -webkit-line-clamp: 3 !important;
    -webkit-box-orient: vertical !important;
    font-weight: 500 !important;
}

/* Chat button styling */
.chat-btn {
    background-color: white !important;
    color: #2e285c !important;
    border: 2px solid transparent !important;
    border-radius: 25px !important;
    padding: 10px 0 !important;
    margin: 0 auto 20px auto !important;
    width: 85% !important;
    display: block !important;
    font-weight: bold !important;
    cursor: pointer !important;
    font-size: 15px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
}

.chat-btn:hover {
    background-color: #f0edfe !important;
    border-color: #2e285c !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
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
    margin: 0 auto 40px;
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

/* Responsive design for horizontal layout */
@media (max-width: 1200px) {
    .character-grid-row {
        justify-content: center !important;
    }
    
    .character-card {
        width: 200px !important;
    }
    
    .main-chat-container {
        flex-direction: column;
    }
    
    .chat-column, .info-column {
        width: 100%;
    }
}

@media (max-width: 992px) {
    .character-grid-row {
        gap: 15px !important;
    }
    
    .character-card {
        width: 180px !important;
        min-height: 300px !important;
    }
    
    .avatar-container {
        height: 120px !important;
    }
    
    .student-name {
        font-size: 20px !important;
    }
    
    .student-description {
        font-size: 13px !important;
        min-height: 45px !important;
    }
}

@media (max-width: 768px) {
    .container {
        padding: 0 15px;
    }
    
    .character-grid-row {
        flex-direction: column !important;
        align-items: center !important;
        gap: 20px !important;
    }
    
    .character-card {
        width: 250px !important;
        max-width: 90vw !important;
    }
    
    .age-group-title {
        font-size: 24px !important;
        margin: 30px 0 15px 0 !important;
    }
    
    .subgroup-title {
        font-size: 18px !important;
        margin: 20px 0 15px 0 !important;
    }
    
    .main-chat-container {
        flex-direction: column;
        padding: 0 10px;
    }
    
    .chat-column, .info-column {
        width: 100%;
    }
}

@media (max-width: 480px) {
    .character-card {
        width: 200px !important;
    }
    
    .selection-heading {
        font-size: 20px !important;
    }
    
    .project-description {
        font-size: 13px !important;
        margin: 0 auto 30px !important;
    }
}

/* Remove any old grid styles that might conflict */
.character-grid {
    display: none !important;
}

/* Ensure proper spacing between groups */
.age-group-title:first-of-type {
    margin-top: 20px !important;
}

/* Additional hover effects for better UX */
.character-card:hover .student-name {
    transform: scale(1.05) !important;
    transition: transform 0.2s ease !important;
}

.character-card:hover .avatar-container {
    transform: scale(1.05) !important;
    transition: transform 0.3s ease !important;
    border-color: white !important;
    box-shadow: 0 6px 16px rgba(46, 40, 92, 0.3) !important;
}

/* Fix for Gradio's default row behavior */
.character-grid-row > div {
    flex: none !important;
    width: auto !important;
    min-width: 220px !important;
}
"""
