import gradio as gr
import json
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Load shared_prompt.txt
with open("shared_prompt.txt", "r") as f:
    shared_prompt = f.read().strip()

# Load all prompts (combining shared + individual)
def load_prompts():
    prompts = {}
    for i in range(1, 11):
        path = f"prompts/{i}.json"
        if os.path.exists(path):
            with open(path, "r") as f:
                data = json.load(f)
                prompts[f"student{i:03d}"] = shared_prompt + "\n\n" + data["prompt"]
    return prompts

all_prompts = load_prompts()

# Student ID to name mapping
name_dict = {
    "student001": "Jaden",
    "student002": "Elijah",
    "student003": "Caleb",
    "student004": "Aiden",
    "student005": "Ava",
    "student006": "Brooklyn",
    "student007": "Zoe",
    "student008": "Kayla",
    "student009": "Maya",
    "student010": "Isaiah"
}

# Student descriptions (personality, background, etc.)
student_descriptions = {
    "student001": "16 years old, excels in science and math, introverted but helpful",
    "student002": "15 years old, loves sports especially basketball, outgoing and energetic",
    "student003": "17 years old, enjoys music and art, creative but somewhat sensitive",
    "student004": "16 years old, good at debate and writing, quick thinker",
    "student005": "15 years old, passionate about natural sciences, very curious",
    "student006": "17 years old, strong social skills, interested in fashion and design",
    "student007": "16 years old, loves reading and writing, shy but thoughtful",
    "student008": "15 years old, has leadership qualities, involved in many school activities",
    "student009": "17 years old, math genius, enjoys solving complex problems",
    "student010": "16 years old, athletic, optimistic and cheerful"
}

# Models used by each student
model_info = {
    "student001": "GPT-4",
    "student002": "GPT-4",
    "student003": "GPT-4",
    "student004": "GPT-4",
    "student005": "GPT-4",
    "student006": "GPT-4",
    "student007": "GPT-4",
    "student008": "GPT-4",
    "student009": "GPT-4",
    "student010": "GPT-4"
}

# Initialize empty chat history for all students
def get_empty_history_dict():
    return {student_id: [] for student_id in name_dict.keys()}

# Chat function
def chat(message, history, student_id, history_dict):
    if not message or not message.strip():
        return "", history, history_dict
        
    system_prompt = all_prompts.get(student_id, "You are a helpful assistant.")

    messages = [{"role": "system", "content": system_prompt}]
    for user_msg, bot_reply in history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": bot_reply})
    messages.append({"role": "user", "content": message})

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7
        )
        reply = response.choices[0].message.content.strip()
        history.append([message, reply])
        # Update history dictionary
        history_dict[student_id] = history
        return "", history, history_dict
    except Exception as e:
        history.append([message, f"⚠️ Error: {str(e)}"])
        history_dict[student_id] = history
        return "", history, history_dict

# Clear chat history for current student
def clear_current_chat(student_id, history_dict):
    history_dict[student_id] = []
    return [], history_dict

# Function to get student model info
def get_student_model(student_id):
    return f"Powered by {model_info.get(student_id, 'Unknown Model')}"

# Direct student selection function
def select_student_direct(student_id, history_dict):
    student_name = name_dict.get(student_id, "Unknown")
    student_avatar = f"avatar/{student_id}.png"
    student_history = history_dict.get(student_id, [])
    student_model = get_student_model(student_id)
    
    return (
        gr.update(visible=False),  # Hide selection page
        gr.update(visible=True),   # Show chat page
        student_id,                # Update selected student ID
        f"# {student_name}",       # Update student name display
        student_model,             # Update model display
        student_avatar,            # Update avatar display
        student_history            # Update chat history
    )

# Return to selection page
def return_to_selection():
    return (
        gr.update(visible=True),   # Show selection page
        gr.update(visible=False)   # Hide chat page
    )

# This CSS has been completely redesigned to look like character.ai
custom_css = """
/* Global styles */
body {
    font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
    background-color: #f9f9f9;
}

/* Card styling for selection page */
.character-card {
    background: white;
    border-radius: 10px;
    padding: 0;
    overflow: hidden;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    transition: transform 0.2s;
    margin: 10px;
    border: 1px solid #e0e0e0;
}

.character-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 4px 10px rgba(0,0,0,0.12);
}

.card-header {
    background-color: #f7931e;
    color: white;
    padding: 10px;
    text-align: center;
    font-weight: bold;
}

.student-name {
    font-size: 20px;
    font-weight: bold;
    margin: 10px 0;
    text-align: center;
}

.student-description {
    padding: 0 15px;
    text-align: center;
    color: #555;
    font-size: 14px;
    height: 60px;
    overflow: hidden;
}

.model-tag {
    background-color: #f0f0f0;
    border-radius: 15px;
    padding: 5px 10px;
    margin: 10px auto;
    display: inline-block;
    font-size: 12px;
    color: #666;
}

.chat-btn {
    background-color: #f7931e !important;
    color: white !important;
    border: none !important;
    border-radius: 20px !important;
    padding: 8px 0 !important;
    margin: 15px auto !important;
    width: 90% !important;
    display: block !important;
    font-weight: bold !important;
    cursor: pointer !important;
}

.chat-btn:hover {
    background-color: #e67e00 !important;
}

/* Selection page title */
.main-title {
    background-color: #f7931e;
    color: white;
    padding: 15px;
    margin: 0;
    text-align: center;
    font-size: 24px;
    font-weight: bold;
    border-radius: 8px 8px 0 0;
}

/* Avatar styling */
.avatar-container {
    position: relative;
    width: 100px;
    height: 100px;
    margin: 15px auto;
    border-radius: 50%;
    overflow: hidden;
    border: 3px solid white;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.avatar-container img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 50%;
}

/* Hide all image controls */
.gradio-image .panel-buttons,
.gradio-image button,
.gradio-image .absolute,
.gradio-image .gr-image-tools,
button[title="Open in new tab"],
button[title="Download"],
.panel-btn, 
.tool-button,
.panel-buttons,
.image-tool-button,
div[class*="image-tools"],
div[class*="tool-buttons"],
.svelte-1g805jl .panel-buttons,
.svelte-1g805jl .absolute,
.svelte-1g805jl button {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
}

/* Make avatars circular without controls */
.gradio-image img {
    border-radius: 50% !important;
    object-fit: cover !important;
}

/* Chat page styling */
.chat-page-container {
    max-width: 800px;
    margin: 0 auto;
    background: white;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    overflow: hidden;
}

.chat-header {
    display: flex;
    align-items: center;
    padding: 15px;
    border-bottom: 1px solid #eee;
    background-color: white;
    position: relative;
}

.chat-avatar {
    width: 40px !important;
    height: 40px !important;
    border-radius: 50% !important;
    margin-right: 15px !important;
    border: 2px solid white !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    object-fit: cover !important;
}

.back-btn {
    position: absolute;
    right: 15px;
    background-color: #f5f5f5 !important;
    border: 1px solid #ddd !important;
    color: #555 !important;
    border-radius: 5px !important;
    padding: 5px 15px !important;
}

/* Character.ai style chat bubbles */
.chatbot-container {
    background-color: #f6f7f8 !important;
    border: none !important;
    border-radius: 0 !important;
    box-shadow: none !important;
}

/* Make messages display properly */
.chatbot-container .message-wrap {
    display: flex !important;
    margin-bottom: 20px !important;
    position: relative !important;
}

.chatbot-container .user-message {
    flex-direction: row-reverse !important;
}

.chatbot-container .bot-message {
    flex-direction: row !important;
}

/* Message bubble styling */
.chatbot-container .message {
    max-width: 80% !important;
    padding: 12px 16px !important;
    border-radius: 18px !important;
    margin: 0 12px !important;
    position: relative !important;
    word-break: break-word !important;
    white-space: pre-wrap !important;
}

.chatbot-container .user-bubble {
    background-color: #f8e5b9 !important;
    color: #000 !important;
    border-top-right-radius: 4px !important;
    text-align: right !important;
    margin-left: auto !important;
}

.chatbot-container .bot-bubble {
    background-color: white !important;
    color: #000 !important;
    border-top-left-radius: 4px !important;
    text-align: left !important;
    margin-right: auto !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.1) !important;
}

/* Message avatar styling */
.chatbot-container .avatar {
    width: 36px !important;
    height: 36px !important;
    border-radius: 50% !important;
    background-size: cover !important;
    background-position: center !important;
}

/* Emotion tag styling - like in the screenshot */
.emotion-tag {
    display: block;
    font-style: italic;
    color: #666;
    margin-top: 5px;
    font-size: 14px;
}

/* Input area styling */
.input-container {
    background-color: white;
    border-top: 1px solid #eee;
    padding: 15px;
    position: relative;
}

.message-input {
    border-radius: 20px !important;
    border: 1px solid #e0e0e0 !important;
    padding: 12px 15px !important;
    font-size: 14px !important;
    transition: border-color 0.3s !important;
}

.message-input:focus {
    border-color: #f7931e !important;
    box-shadow: 0 0 0 2px rgba(247, 147, 30, 0.2) !important;
}

.send-btn {
    background-color: #f7931e !important;
    color: white !important;
    border: none !important;
    border-radius: 24px !important;
    padding: 12px 20px !important;
    font-weight: 500 !important;
    cursor: pointer !important;
    margin-left: 10px !important;
    transition: background-color 0.3s !important;
}

.send-btn:hover {
    background-color: #e67e00 !important;
}

.clear-btn {
    background-color: transparent !important;
    color: #666 !important;
    border: none !important;
    margin-top: 10px !important;
    font-size: 13px !important;
    text-decoration: underline !important;
    cursor: pointer !important;
}

/* Override Gradio's default chat styles */
.message > .self, .message > .svelte-16r4uzs {
    border-top-right-radius: 4px !important;
    background-color: #f8e5b9 !important;
}

.message:not(.self), .message:not(.svelte-16r4uzs) {
    border-top-left-radius: 4px !important;
    background-color: white !important;
}

/* Don't display Gradio's default avatars */
.message.self::before, .message:not(.self)::before {
    display: none !important;
}

/* Message container styling */
.message-container {
    border-radius: 18px;
    padding: 10px 15px;
    margin-bottom: 10px;
    max-width: 70%;
    position: relative;
}

.user-message-container {
    background-color: #f8e5b9;
    margin-left: auto;
    border-top-right-radius: 4px;
}

.bot-message-container {
    background-color: white;
    margin-right: auto;
    border-top-left-radius: 4px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.1);
}

/* Force image controls to be hidden */
.gradio-image .p-absolute,
.gradio-image div[class^="flex"],
.gradio-image div[class*="flex"] {
    display: none !important;
}

/* Make sure both header and input are visible */
.chat-header, .input-container {
    position: sticky;
    z-index: 10;
}

.chat-header {
    top: 0;
}

.input-container {
    bottom: 0;
}
"""

# --------------------------------------------
# = UI BUILDING =
# --------------------------------------------
with gr.Blocks(css=custom_css) as demo:

    # ── History state (all students) ──────────
    history_dict_state = gr.State(get_empty_history_dict())
    selected_id_state = gr.State("")
    
    # ── Create both pages as components ──────────
    selection_page = gr.Group(visible=True)
    chat_page = gr.Group(visible=False, elem_classes="chat-page-container")
    
    # ── Define chat page components FIRST ──────────
    with chat_page:
        # Chat header with student info
        with gr.Row(elem_classes="chat-header"):
            avatar_display = gr.Image(
                value="avatar/default.png", 
                show_label=False,
                elem_classes="chat-avatar",
                height=40,
                width=40
            )
            with gr.Column():
                name_display = gr.Markdown("Student Name")
                model_display = gr.Markdown("Powered by GPT-4", elem_classes="model-tag")
            back_button = gr.Button("← Back", elem_classes="back-btn")
            
        # Chat area with character.ai style
        chatbot = gr.Chatbot(
            label="",
            elem_classes="chatbot-container",
            avatar_images=("avatar/user.png", None),
            height=500,
            show_label=False,
            bubble=True,
        )
        
        # Input area styled like character.ai
        with gr.Row(elem_classes="input-container"):
            with gr.Column(scale=5):
                msg = gr.Textbox(
                    placeholder="Type your message...",
                    label="",
                    elem_classes="message-input",
                    show_label=False,
                )
            
            with gr.Column(scale=1, min_width=100):
                send_btn = gr.Button("Send", elem_classes="send-btn")
        
        clear_btn = gr.Button("Clear conversation", elem_classes="clear-btn")
    
    # ── Selection page ───────────────────────────
    with selection_page:
        gr.Markdown("# 🎓 Digital-Twin Chat Demo", elem_classes="main-title")
        gr.Markdown("### Choose a student to chat with")
        
        # Create student selection grid
        with gr.Row():
            for i in range(0, 5):  # First row with 5 students
                student_id = f"student{i+1:03d}"
                
                with gr.Column(elem_classes="character-card"):
                    gr.Markdown("Digital Twin", elem_classes="card-header")
                    with gr.Column(elem_classes="avatar-container"):
                        gr.Image(
                            value=f"avatar/{student_id}.png",
                            show_label=False,
                            elem_classes="avatar-img",
                            height=100,
                            width=100
                        )
                    gr.Markdown(f"### {name_dict[student_id]}", elem_classes="student-name")
                    gr.Markdown(student_descriptions[student_id], elem_classes="student-description")
                    gr.Markdown(f"Powered by {model_info[student_id]}", elem_classes="model-tag")
                    
                    btn = gr.Button("Start Chat", elem_classes="chat-btn")
                    btn.click(
                        select_student_direct,
                        inputs=[
                            gr.Textbox(value=student_id, visible=False),
                            history_dict_state
                        ],
                        outputs=[
                            selection_page, 
                            chat_page, 
                            selected_id_state, 
                            name_display, 
                            model_display,
                            avatar_display, 
                            chatbot
                        ]
                    )
        
        with gr.Row():
            for i in range(5, 10):  # Second row with 5 students
                student_id = f"student{i+1:03d}"
                
                with gr.Column(elem_classes="character-card"):
                    gr.Markdown("Digital Twin", elem_classes="card-header")
                    with gr.Column(elem_classes="avatar-container"):
                        gr.Image(
                            value=f"avatar/{student_id}.png",
                            show_label=False,
                            elem_classes="avatar-img",
                            height=100,
                            width=100
                        )
                    gr.Markdown(f"### {name_dict[student_id]}", elem_classes="student-name")
                    gr.Markdown(student_descriptions[student_id], elem_classes="student-description")
                    gr.Markdown(f"Powered by {model_info[student_id]}", elem_classes="model-tag")
                    
                    btn = gr.Button("Start Chat", elem_classes="chat-btn")
                    btn.click(
                        select_student_direct,
                        inputs=[
                            gr.Textbox(value=student_id, visible=False),
                            history_dict_state
                        ],
                        outputs=[
                            selection_page, 
                            chat_page, 
                            selected_id_state, 
                            name_display, 
                            model_display,
                            avatar_display, 
                            chatbot
                        ]
                    )
    
    # ── Event handlers ─────────────────────────    
    # Return to selection page
    back_button.click(
        return_to_selection,
        inputs=[],
        outputs=[selection_page, chat_page]
    )
    
    # Send message
    msg.submit(
        chat,
        inputs=[msg, chatbot, selected_id_state, history_dict_state],
        outputs=[msg, chatbot, history_dict_state],
    )
    
    send_btn.click(
        chat,
        inputs=[msg, chatbot, selected_id_state, history_dict_state],
        outputs=[msg, chatbot, history_dict_state],
    )
    
    # Clear chat history
    clear_btn.click(
        clear_current_chat,
        inputs=[selected_id_state, history_dict_state],
        outputs=[chatbot, history_dict_state],
        queue=False
    )

    # JavaScript to enhance the chat interface and force proper styling
    demo.load(None, None, None, js="""
    function() {
        // Custom function to enhance the chat interface
        function enhanceChatInterface() {
            // Helper to create emotion tag
            function addEmotionTagsToMessages() {
                document.querySelectorAll('.bot-message .message-content').forEach(function(msgElement) {
                    let text = msgElement.textContent;
                    if (text.includes('Emotion:') || text.includes('Emotion tag:')) {
                        let parts = text.split(/Emotion:|\nEmotion tag:/);
                        if (parts.length > 1) {
                            let mainContent = parts[0].trim();
                            let emotion = parts[1].trim();
                            
                            // Replace the content with just the main part
                            msgElement.textContent = mainContent;
                            
                            // Create and append emotion tag
                            let emotionTag = document.createElement('span');
                            emotionTag.className = 'emotion-tag';
                            emotionTag.textContent = 'Emotion: ' + emotion;
                            msgElement.appendChild(emotionTag);
                        }
                    }
                });
            }
            
            // Style message bubbles and add avatars
            function styleMessageBubbles() {
                // Hide all image controls
                document.querySelectorAll('.gradio-image button, .gradio-image .panel-buttons, .gradio-image .absolute').forEach(function(el) {
                    el.style.display = 'none';
                    el.style.visibility = 'hidden';
                    el.style.opacity = '0';
                    el.style.pointerEvents = 'none';
                });
                
                // Make all avatar images circular
                document.querySelectorAll('.gradio-image img').forEach(function(img) {
                    img.style.borderRadius = '50%';
                    img.style.objectFit = 'cover';
                });
                
                // Get avatar URLs
                const userAvatar = 'avatar/user.png';
                const studentAvatar = document.querySelector('.chat-avatar')?.src || 'avatar/default.png';
                
                // Style chatbot messages
                document.querySelectorAll('.chatbot-container .message').forEach(function(msgElement) {
                    // Skip if already processed
                    if (msgElement.dataset.processed === 'true') return;
                    
                    // Check if user or bot message
                    const isUserMessage = msgElement.classList.contains('self');
                    
                    // Create avatar element if it doesn't exist
                    if (!msgElement.querySelector('.chat-message-avatar')) {
                        const avatarElement = document.createElement('div');
                        avatarElement.className = 'avatar';
                        
                        // Set correct avatar image and position
                        if (isUserMessage) {
                            avatarElement.style.backgroundImage = `url('${userAvatar}')`;
                            msgElement.classList.add('user-bubble');
                            msgElement.parentElement.classList.add('user-message');
                        } else {
                            avatarElement.style.backgroundImage = `url('${studentAvatar}')`;
                            msgElement.classList.add('bot-bubble');
                            msgElement.parentElement.classList.add('bot-message');
                        }
                        
                        // Add avatar before or after message based on sender
                        if (isUserMessage) {
                            msgElement.parentElement.appendChild(avatarElement);
                        } else {
                            msgElement.parentElement.prepend(avatarElement);
                        }
                    }
                    
                    // Mark as processed
                    msgElement.dataset.processed = 'true';
                });
                
                // Add emotion tags
                addEmotionTagsToMessages();
            }
            
            // Run styling functions periodically
            styleMessageBubbles();
            setInterval(styleMessageBubbles, 500);
        }
        
        // Initialize the chat interface enhancement
        enhanceChatInterface();
        
        // Additional CSS fixes via JavaScript for elements that might be dynamically added
        const style = document.createElement('style');
        style.textContent = `
            .message {
                max-width: 80% !important;
                border-radius: 18px !important;
                padding: 12px 16px !important;
                margin: 0 12px !important;
                position: relative !important;
            }
            
            .user-bubble {
                background-color: #f8e5b9 !important;
                border-top-right-radius: 4px !important;
            }
            
            .bot-bubble {
                background-color: white !important;
                border-top-left-radius: 4px !important;
                box-shadow: 0 1px 2px rgba(0,0,0,0.1) !important;
            }
            
            .avatar {
                width: 36px !important;
                height: 36px !important;
                min-width: 36px !important;
                min-height: 36px !important;
                border-radius: 50% !important;
                background-size: cover !important;
                background-position: center !important;
                margin: 0 8px !important;
                align-self: flex-end !important;
            }
        `;
        document.head.appendChild(style);
    }
    """)

# Run the application
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860))
    )
