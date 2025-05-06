# Update these sections in your custom_css.py file

# Fix for student names in card headers (maximum emphasis)
"""
/* Card header with maximum emphasis for student names */
.card-header {
    background-color: #094067;
    color: white !important;
    padding: 10px;
    text-align: center;
    font-weight: 900 !important; /* Maximum bold weight */
    font-size: 20px !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    text-shadow: 0 1px 2px rgba(0,0,0,0.3);
}
"""

# Fix for avatar images (fill entire container)
"""
/* Avatar styling for chat */
.gradio-chatbot .avatar-container {
    width: 48px !important;
    height: 48px !important;
    border-radius: 50% !important;
    overflow: hidden !important;
    border: 2px solid #094067 !important;
    margin: 0 !important;
    padding: 0 !important;
    background-color: transparent !important;
}

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
"""

# Fix for back button (changed to blue)
"""
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
"""
