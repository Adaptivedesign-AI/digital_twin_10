custom_css = """
/* Global styles for the entire application */
body {
    font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
    background-color: #f9f9f9;
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

/* Header styling with updated brand color and reduced opacity */
.main-title {
    background-color: rgba(9, 64, 103, 0.85); /* Reduced opacity blue header */
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

/* Card header with title case for student names and reduced opacity */
.card-header {
    background-color: #315d6e;
    color: white !important;
    padding: 10px;
    text-align: center;
    font-weight: 900 !important; /* Maximum bold weight */
    font-size: 25px !important;
    letter-spacing: 1px;
    text-shadow: 0 1px 2px rgba(0,0,0,0.3);
    text-transform: capitalize !important; /* Changed from uppercase to capitalize */
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

/* Avatar styling - updated with circular design and transparent background */
.character-card .avatar-container {
    width: 120px!important;
    height: 120px!important;
    overflow: hidden!important;
    margin: 15px auto!important;
    border: 2px solid rgba(9, 64, 103, 0.85)!important; /* Reduced opacity blue */
    border-radius: 50%!important; /* Circular avatars */
    box-shadow: 0 4px 8px rgba(0,0,0,0.1)!important;
    background-color: #fce5be !important;
}

.character-card .avatar-container img,
.character-card .avatar-container > div,
.character-card .avatar-img,
.character-card [data-testid="image"],
.character-card [data-testid="image"] > div {
    width: 100%!important;
    height: 100%!important;
    object-fit: cover!important;
    display: block!important;
    background-color: transparent!important;
    border: none!important;
    box-shadow: none!important;
    margin: 0!important;
    padding: 0!important;
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
    background-color: rgba(9, 64, 103, 0.85); /* Reduced opacity blue header */
    color: white;
    border-radius: 12px 12px 0 0;
}

.back-btn {
    background-color: #3da9fc !important;
    border: none !important;
    color: #fffffe !important;
    border-radius: 5px !important;
    padding: 5px 10px !important;
    margin-right: 15px !important;
    margin-left: 0 !important;
    cursor: pointer !important;
    transition: background-color 0.2s !important;
    font-weight: bold !important;
}

.back-btn:hover {
    background-color: #2a93e0 !important;
}

/* Input and buttons styling for better aesthetics */
.message-input textarea {
    background-color: #fffffe !important;
    border: 1px solid #90b4ce !important;
    border-radius: 20px !important;
    padding: 12px 16px !important;
    font-size: 14px !important;
    color: #094067 !important;
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
    background-color: #3da9fc !important;
    color: #fffffe !important;
    font-weight: bold !important;
    border-radius: 20px !important;
    padding: 8px 15px !important;
    width: 100% !important;
    border: none !important;
    cursor: pointer !important;
    transition: background-color 0.2s !important;
}

.send-btn:hover {
    background-color: #2a93e0 !important;
}

.clear-btn {
    background-color: rgba(9, 64, 103, 0.85) !important; /* Reduced opacity blue */
    color: #fffffe !important;
    font-weight: bold !important;
    border-radius: 20px !important;
    padding: 8px 15px !important;
    width: 100% !important;
    border: none !important;
    cursor: pointer !important;
    transition: background-color 0.2s !important;
}

.clear-btn:hover {
    background-color: #073050 !important;
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
    color: #fffffe !important;
    font-size: 24px !important;
    font-weight: bold !important;
    margin: 0 auto !important;
    text-align: center !important;
}

/* Model display styling - hidden by default */
.model-display {
    display: none;
}

/* Character.ai style chat container */
.character-ai-style {
    border-radius: 12px;
    background-color: #d8eefe !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

/* Custom styling for chat rows */
.chatbot-row {
    display: flex;
    margin-bottom: 20px;
}

/* Chat avatar styling */
.gradio-chatbot .avatar img {
    width: 100% !important;
    height: 100% !important;
    border-radius: 50% !important;
    border: none !important;
    object-fit: cover !important;
}

/* Ensure avatars are visible and styled correctly */
.gradio-chatbot .message-wrap.user .avatar,
.gradio-chatbot .message-wrap.bot .avatar {
    display: inline-block !important;
    width: 48px !important;
    height: 48px !important;
    border-radius: 50% !important;
    overflow: hidden !important;
    margin-right: 8px !important;
    flex-shrink: 0 !important;
    box-shadow: none !important;
    border: 2px solid rgba(9, 64, 103, 0.85) !important; /* Reduced opacity blue */
    padding: 0 !important;
    background-color: transparent !important;
}

/* Chat bubbles: AI is blue, user is white */
.gradio-chatbot .message.bot {
    background-color: #3da9fc !important;
    color: #fffffe !important;
    border-bottom-left-radius: 6px !important;
    border-top-left-radius: 18px !important;
    border-top-right-radius: 18px !important;
    border-bottom-right-radius: 18px !important;
    margin-left: 12px !important;
    margin-right: auto !important;
    max-width: 80%;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
    padding: 12px 16px !important;
    word-wrap: break-word !important;
}

.gradio-chatbot .message.user {
    background-color: #fffffe !important;
    color: #094067 !important;
    border-bottom-right-radius: 6px !important;
    border-top-left-radius: 18px !important;
    border-top-right-radius: 18px !important;
    border-bottom-left-radius: 18px !important;
    margin-right: 12px !important;
    margin-left: auto !important;
    max-width: 80%;
    border: 1px solid #90b4ce !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
    padding: 12px 16px !important;
    word-wrap: break-word !important;
}

/* Chat area overall background (light blue) */
.character-ai-style.chatbox-container {
    background-color: #d8eefe !important;
    padding: 20px !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
}

/* Emotion tag styling for emotional context */
.emotion-tag {
    font-style: italic !important;
    font-size: 12px !important;
    color: #666 !important;
    margin-top: 4px !important;
    display: block !important;
}

/* Project description styling */
.project-description {
    text-align: center;
    margin: 0 auto 5px;
    max-width: 800px;
    color: #555;
    font-size: 14px;
    line-height: 1.5;
    padding: 0 20px;
    font-style: italic;
}

/* Chat avatar containers */
.gradio-chatbot .avatar-container {
    width: 48px !important;
    height: 48px !important;
    border-radius: 50% !important;
    overflow: hidden !important;
    border: 2px solid rgba(9, 64, 103, 0.85) !important; /* Reduced opacity blue */
    margin: 0 !important;
    padding: 0 !important;
    background-color: transparent !important;
}

/* Ensure proper message wrapping and alignment */
.gradio-chatbot .message-wrap {
    margin-bottom: 16px !important;
    display: flex !important;
    align-items: flex-start !important;
}

/* Selection heading styling for clear hierarchy */
.selection-heading {
    text-align: center;
    margin: 1px 0 10px;
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

/* Input row: transparent background, vertically centered */
.gradio-container .row {
    background-color: transparent !important;
    align-items: center !important;
}

/* Avatar image styling to ensure it fills the container */
.gradio-chatbot .avatar-container img,
.gradio-chatbot .avatar img,
.gradio-chatbot img.avatar-image {
    width: 100% !important;
    height: 100% !important;
    object-fit: cover !important;
    border-radius: 50% !important;
    border: none !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* Remove image backgrounds - target all image and container elements */
.gradio-container .gradio-image, 
.gradio-container img, 
.gradio-container [data-testid="image"],
.gradio-container [class*="image"],
.gradio-container [class*="avatar"],
.character-card .gradio-image,
.character-card img,
.character-card [data-testid="image"] {
    background-color: transparent !important;
    background: transparent !important;
}

/* Override any image background styles with !important */
img, [data-testid="image"], [class*="image"] {
    background-color: transparent !important;
    background: transparent !important;
}

/* Additional fixes for Gradio's image component containers */
.gradio-image > div, .gradio-image > div > div, .gradio-image > div > img {
    background-color: transparent !important;
    background: transparent !important;
    box-shadow: none !important;
    border: none !important;
}
"""
