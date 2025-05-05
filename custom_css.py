# Enhanced CSS for better UI with updated color scheme and design
custom_css = """
/* Global styles for the entire application */
body {
    font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
    background-color: #f9f9f9;
}

/* Header styling with updated brand color */
.main-title {
    background-color: #094067;
    color: white;
    padding: 15px;
    margin: 0;
    text-align: center;
    font-size: 24px;
    font-weight: bold;
    border-radius: 8px 8px 0 0;
}

/* Character.ai style grid for selection page - 5 columns by default */
.character-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 20px;
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
}

/* Responsive breakpoints for character grid at different screen sizes */
@media (max-width: 1200px) {
    .character-grid {
        grid-template-columns: repeat(4, 1fr);
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
}

@media (max-width: 480px) {
    .character-grid {
        grid-template-columns: 1fr;
    }
}

/* Card styling - updated with rounded edges */
.character-card {
    background: white;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    transition: transform 0.2s, box-shadow 0.2s;
    border: 1px solid #e0e0e0;
    height: 100%;
    display: flex;
    flex-direction: column;
    cursor: pointer;
    max-width: 220px;
    margin: 0 auto;
}

.character-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 16px rgba(0,0,0,0.15);
}

.card-header {
    background-color: #094067;
    color: white;
    padding: 10px;
    text-align: center;
    font-weight: bold;
    font-size: 16px;
}

/* Student info styling - compact and readable */
.student-name {
    font-size: 16px;
    font-weight: bold;
    margin: 8px 0 4px;
    text-align: center;
}

.student-description {
    padding: 0 12px;
    text-align: center;
    color: #555;
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

/* Avatar styling - updated with circular design */
.avatar-container {
    width: 120px!important;
    height: 120px!important;
    overflow: hidden!important;
    margin: 15px auto!important;
    border: 2px solid #094067!important;
    border-radius: 50%!important; /* Circular avatars */
    box-shadow: 0 4px 8px rgba(0,0,0,0.1)!important;
}

.avatar-container img {
    width: 100%!important;
    height: 100%!important;
    object-fit: cover!important;
    display: block!important;
}

/* Chat button styling with updated brand color */
.chat-btn {
    background-color: #3da9fc !important;
    color: white !important;
    border: none !important;
    border-radius: 20px !important;
    padding: 8px 0 !important;
    margin: 10px auto 16px !important;
    width: 85% !important;
    display: block !important;
    font-weight: bold !important;
    cursor: pointer !important;
    font-size: 14px !important;
    transition: background-color 0.2s !important;
}

.chat-btn:hover {
    background-color: #2a93e0 !important;
}

/* Chat interface styling for better user experience */
.chat-header {
    display: flex;
    align-items: center;
    padding: 15px;
    border-bottom: 1px solid #e0e0e0;
    background-color: #f8f9fa;
}

.back-btn {
    background-color: #f5f5f5 !important;
    border: 1px solid #ddd !important;
    color: #555 !important;
    border-radius: 5px !important;
    margin-right: 15px !important;
    margin-left: 0 !important;
}

/* Input and buttons styling for better aesthetics */
.message-input {
    border-radius: 20px !important;
    padding: 10px 15px !important;
    border: 1px solid #e0e0e0 !important;
}

/* Button container for vertical layout */
.button-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
    width: 100%;
}

.send-btn {
    background-color: #3da9fc !important;
    color: white !important;
    border: none !important;
    border-radius: 20px !important;
    padding: 8px 15px !important;
    width: 100% !important;
}

.clear-btn {
    background-color: #f0f0f0 !important;
    color: #555 !important;
    border: 1px solid #ddd !important;
    border-radius: 20px !important;
    padding: 8px 15px !important;
    width: 100% !important;
}

/* Character info styling in chat - simplified header without avatar */
.character-info {
    display: flex;
    flex-direction: column;
    justify-content: center;
    margin-left: 5px;
}

/* Student name styling in header */
.student-name-header {
    font-size: 22px;
    font-weight: bold;
    margin: 0;
}

/* Model display styling - hidden by default */
.model-display {
    display: none;
}

/* Character.ai style chat container */
.character-ai-style {
    border-radius: 12px;
    background-color: white;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

/* Custom styling for chat rows */
.chatbot-row {
    display: flex;
    margin-bottom: 20px;
}

/* Chat avatar styling */
.gradio-chatbot .avatar {
    display: block !important;
    width: 32px !important;
    height: 32px !important;
    border-radius: 50% !important;
    margin-right: 8px !important;
    margin-top: 2px !important;
    flex-shrink: 0 !important;
    border: 1px solid #e0e0e0 !important;
    background-color: transparent !important;
    overflow: hidden !important;
}

/* Ensure avatars are visible and styled correctly */
.gradio-chatbot .message-wrap.user .avatar,
.gradio-chatbot .message-wrap.bot .avatar {
    display: inline-block !important;
    width: 32px !important;
    height: 32px !important;
    border-radius: 50% !important;
    overflow: hidden !important;
    margin-right: 8px !important;
    flex-shrink: 0 !important;
    box-shadow: none !important;
    border: 1px solid #e0e0e0 !important;
    padding: 0 !important;
    background-color: transparent !important;
}

/* Character.ai style chat bubbles */
.gradio-chatbot .message {
    border-radius: 18px !important;
    padding: 12px 16px !important;
    margin: 0 !important;
    line-height: 1.5 !important;
    max-width: 80% !important;
    display: inline-block !important;
    margin-top: 5px !important;
    word-wrap: break-word !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.1) !important;
}

/* User message styling with updated brand color */
.gradio-chatbot .message.user {
    background-color: #3da9fc !important;
    color: white !important;
    border-bottom-right-radius: 4px !important;
    margin-left: auto !important;
}

/* Bot message styling with light background */
.gradio-chatbot .message.bot {
    background-color: #f1f1f1 !important;
    color: #333 !important;
    border-bottom-left-radius: 4px !important;
    margin-right: auto !important;
}

/* Emotion tag styling for emotional context */
.emotion-tag {
    font-style: italic;
    display: block;
    margin-top: 5px;
    color: #888;
    font-size: 0.9em;
}

/* Custom styling for chat container to match Character.ai */
.chatbox-container {
    padding: 20px !important;
    background-color: #fff !important;
    border-radius: 12px !important;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05) !important;
}

/* Override default gradio chatbot styling for avatars */
.gradio-container .prose img.avatar-image {
    display: inline-block !important;
    margin: 0 !important;
    border-radius: 50% !important;
    width: 32px !important;  /* Smaller avatar size in chat */
    height: 32px !important; /* Smaller avatar size in chat */
    border: none !important;
    box-shadow: none !important;
    background-color: transparent !important;
}

/* Project description styling */
.project-description {
    text-align: center;
    margin: 0 auto 20px;
    max-width: 800px;
    color: #555;
    font-size: 14px;
    line-height: 1.5;
    padding: 0 20px;
    font-style: italic;
}

/* Selection page avatar containers - keep larger size with border */
.character-card .avatar-container {
    background-color: transparent !important;
    border: 2px solid #094067 !important;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1) !important;
    padding: 0 !important;
    border-radius: 50% !important;
    width: 120px !important;
    height: 120px !important;
    margin: 15px auto !important;
}

/* Chat avatar containers - smaller with subtle styling */
.gradio-chatbot .avatar-container {
    background-color: transparent !important;
    border: 1px solid #e0e0e0 !important;
    box-shadow: none !important;
    padding: 0 !important;
    border-radius: 50% !important;
    width: 32px !important;
    height: 32px !important;
    margin: 2px !important;
}

.message-row .avatar-image, 
.message-wrap .avatar-image {
    width: 32px !important;
    height: 32px !important;
    padding: 0 !important;
    margin: 0 !important;
    border: none !important;
    box-shadow: none !important;
    display: block !important;
}

/* Target specific avatar container in messages */
.message-row > .svelte-1y9ctm5,
.message-wrap > .svelte-1y9ctm5 {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin: 0 !important;
    width: 32px !important;
    height: 32px !important;
}

/* Target avatar in message bubbles */
.message-bubble .avatar-container,
.message .avatar-container {
    background: transparent !important;
    border: 1px solid #e0e0e0 !important;
    padding: 0 !important;
    margin: 2px !important;
    box-shadow: none !important;
    width: 32px !important;
    height: 32px !important;
    min-width: 32px !important;
    min-height: 32px !important;
}

/* Disable rectangular borders around avatar images */
img.avatar-image {
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
    background: transparent !important;
    padding: 0 !important;
}

/* Selection heading styling for clear hierarchy */
.selection-heading {
    text-align: center;
    margin: 20px 0 10px;
    color: #094067;
    font-size: 22px;
    font-weight: bold;
}

/* Container for main content with reasonable max width */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 24px;
}

/* Fix Gradio spacing issues */
.gradio-container {
    max-width: 100% !important;
}

/* Hide unnecessary margins in Gradio blocks */
.block {
    margin-bottom: 0 !important;
}

/* Center the name and model in the chat header */
.center-header {
    margin: 0 auto;
    text-align: center;
}

/* Add more whitespace around messages for readability */
.gradio-chatbot .message-wrap {
    margin-bottom: 10px !important;
}

/* Adjust spacing for better alignment with tiny avatars */
.gradio-chatbot .message-wrap > div {
    display: flex !important;
    align-items: flex-start !important;
}
"""
