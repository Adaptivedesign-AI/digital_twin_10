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

    # Function to update chatbot avatar when selecting a student
    def select_student_direct(student_id, history_dict):
        student_name = name_dict.get(student_id, "Unknown")
        student_avatar = f"avatar/{student_id}.png"
        student_history = history_dict.get(student_id, [])
        student_model = get_student_model(student_id)
        
        # Update chatbot to use the correct student avatar
        return (
            gr.update(visible=False),  # Hide selection page
            gr.update(visible=True),   # Show chat page
            student_id,                # Update selected student ID
            f"# {student_name}",       # Update student name display
            student_model,             # Update model display
            gr.Chatbot.update(avatar_images=("avatar/user.png", student_avatar)),  # Update avatar
            student_history            # Update chat history
        )

# Return to selection page
def return_to_selection():
    return (
        gr.update(visible=True),   # Show selection page
        gr.update(visible=False)   # Hide chat page
    )

# Enhanced CSS with significant improvements
custom_css = """
/* Global styles */
body {
    font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
    background-color: #f9f9f9;
}

/* Header styling */
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

/* Card grid layout - FIXED GRID WITH 3 CARDS PER ROW */
.card-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr); /* Fixed 3 cards per row */
    gap: 16px;
    margin: 15px;
}

/* Ensure consistent grid across all device sizes */
@media (max-width: 992px) {
    .card-grid {
        grid-template-columns: repeat(3, 1fr); /* Keep 3 columns even on smaller screens */
    }
}

/* Last row with just one card */
.last-row {
    display: grid;
    grid-template-columns: 1fr;
    max-width: 33%;
    margin: 15px auto;
}

/* Card styling */
.character-card {
    background: white;
    border-radius: 10px;
    padding: 0;
    overflow: hidden;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    transition: transform 0.2s;
    border: 1px solid #e0e0e0;
    height: 100%;
    display: flex;
    flex-direction: column;
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

/* Student info styling */
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

/* Chat button styling */
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

/* CSS to make the chat interface more like a messaging app */
.chat-area {
    border-radius: 10px !important;
    overflow: hidden !important;
    background-color: #f8f9fa !important;
    padding: 10px !important;
}

/* Input container styling */
.input-container {
    margin-top: 10px !important;
    gap: 10px !important;
    align-items: center !important;
}

.input-box {
    border-radius: 20px !important;
    padding: 10px 15px !important;
    border: 1px solid #e0e0e0 !important;
    background-color: white !important;
}

/* Button styling */
.action-buttons {
    display: flex !important;
    flex-direction: column !important;
    gap: 8px !important;
}

.send-btn {
    background-color: #f7931e !important;
    color: white !important;
    border: none !important;
    border-radius: 20px !important;
    padding: 8px 15px !important;
    font-weight: bold !important;
    width: 100% !important;
}

.clear-btn {
    background-color: #f0f0f0 !important;
    color: #555 !important;
    border: 1px solid #ddd !important;
    border-radius: 5px !important;
    font-size: 12px !important;
    width: 100% !important;
}

/* Chat message bubbles styling */
.message-bubble {
    border-radius: 18px !important;
    padding: 10px 15px !important;
    max-width: 80% !important;
    position: relative !important;
    margin: 8px 0 !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.1) !important;
}

.user-message {
    background-color: #DCF8C6 !important;
    color: #333 !important;
    margin-left: auto !important;
    border-bottom-right-radius: 4px !important;
}

.assistant-message {
    background-color: #f7931e !important;
    color: white !important;
    margin-right: auto !important;
    border-bottom-left-radius: 4px !important;
}

/* Avatar styling for chat */
.chat-avatar {
    width: 40px !important;
    height: 40px !important;
    border-radius: 50% !important;
    border: 2px solid white !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.2) !important;
    flex-shrink: 0 !important;
}

/* Ensuring avatars are visible */
.gradio-chatbot .avatar {
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
}

/* Chat message row styling */
.chat-row {
    display: flex !important;
    align-items: flex-start !important;
    margin-bottom: 15px !important;
    position: relative !important;
}

.chat-row img {
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
}

/* Force avatar visibility */
.svelte-1ed2p3z {
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
}

/* CRITICAL: Avatar styling for PERFECTLY CIRCULAR AVATARS */
.avatar-container {
    position: relative;
    width: 100px;
    height: 100px;
    margin: 15px auto;
    border-radius: 50%;
    overflow: hidden;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    border: 3px solid white;
    aspect-ratio: 1/1; /* Force perfect circle */
}

.avatar-container img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 50%;
    aspect-ratio: 1/1; /* Force perfect circle */
}

/* Better hide all image controls */
.gradio-image .panel-buttons,
.gradio-image .get_interpret_btn,
.gradio-image .wrap.svelte-1cl284s,
.gradio-image .absolute,
.gradio-image .gr-image-tools,
.gradio-image .tool-button,
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
.svelte-1g805jl button,
.image-buttons-row {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
    width: 0 !important;
    height: 0 !important;
    position: absolute !important;
    z-index: -999 !important;
}

/* Make avatars circular without controls */
.gradio-image img {
    border-radius: 50% !important;
    object-fit: cover !important;
}

/* Additional fix for Safari */
.gradio-container .prose img,
.gradio-container .panel-image {
    border-radius: 50% !important;
    margin: 0 auto !important;
    display: block !important;
}

/* Chat avatar specific */
.chat-avatar {
    width: 40px !important;
    height: 40px !important;
    border-radius: 50% !important;
    margin-right: 15px !important;
    border: 2px solid white !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    object-fit: cover !important;
}

/* Chatbot styling for better message bubbles */
.chatbot-container {
    border-radius: 10px !important;
    overflow: hidden !important;
}

.message-bubble {
    border-radius: 18px !important;
    padding: 10px 15px !important;
    max-width: 80% !important;
    position: relative !important;
    margin: 8px 0 !important;
}

.user-message {
    background-color: #f0f0f0 !important;
    color: #333 !important;
    margin-left: auto !important;
    border-bottom-right-radius: 4px !important;
}

.assistant-message {
    background-color: #f7931e !important;
    color: white !important;
    margin-right: auto !important;
    border-bottom-left-radius: 4px !important;
}

/* Input and buttons styling - FIX FOR ISSUE #3: CHAT CONTROLS LAYOUT */
.chat-controls {
    display: flex !important;
    gap: 10px !important;
    margin-top: 10px !important;
}

.message-input {
    flex-grow: 1 !important;
    border-radius: 20px !important;
    padding: 10px 15px !important;
    border: 1px solid #e0e0e0 !important;
}

.controls-container {
    display: flex !important;
    flex-direction: column !important;
    gap: 8px !important;
}

.send-btn {
    background-color: #f7931e !important;
    color: white !important;
    border: none !important;
    border-radius: 20px !important;
    padding: 8px 15px !important;
    font-weight: bold !important;
}

.clear-btn {
    background-color: #f0f0f0 !important;
    color: #555 !important;
    border: 1px solid #ddd !important;
    border-radius: 5px !important;
    font-size: 12px !important;
}

/* Hide image controls more aggressively */
.gradio-image .p-absolute,
.gradio-image .relative > div:last-child,
.gradio-image div[class^="flex"],
.gradio-image div[class*="flex"],
.gradio-image button {
    display: none !important;
    visibility: hidden !important;
}

/* Chat bubble styling for messages */
.chatbot-row {
    display: flex !important;
    margin-bottom: 12px !important;
    align-items: flex-start !important;
}

.chatbot-msg {
    max-width: 85% !important;
    border-radius: 18px !important;
    padding: 10px 14px !important;
    position: relative !important;
    word-break: break-word !important;
}

.user-row {
    justify-content: flex-end !important;
}

.bot-row {
    justify-content: flex-start !important;
}

.user-msg {
    background-color: #DCF8C6 !important;
    margin-right: 10px !important;
    border-bottom-right-radius: 4px !important;
}

.bot-msg {
    background-color: #f7931e !important;
    color: white !important;
    margin-left: 10px !important;
    border-bottom-left-radius: 4px !important;
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
    chat_page = gr.Group(visible=False)
    
    # ── Define chat page components FIRST ──────────
    with chat_page:
        # Chat header with student info - BACK BUTTON ON LEFT
        with gr.Row(elem_classes="chat-header"):
            back_button = gr.Button("← Back", elem_classes="back-btn")
            with gr.Column(scale=3):
                name_display = gr.Markdown("Student Name")
                model_display = gr.Markdown("Powered by GPT-4", elem_classes="model-tag")
        
        # Create a dictionary to map student IDs to their avatar paths
        avatar_dict = {f"student{i:03d}": f"avatar/student{i:03d}.png" for i in range(1, 11)}
        
        # Chat area with properly configured avatars
        chatbot = gr.Chatbot(
            label="Conversation",
            avatar_images=("avatar/user.png", "avatar/student001.png"),  # Default student avatar
            elem_classes="chat-area",
            height=450,
            show_label=False,
        )
            
        # Input area with better layout
        with gr.Row(elem_classes="input-container"):
            with gr.Column(scale=4):
                msg = gr.Textbox(
                    placeholder="Type a message and press Enter...",
                    label="",
                    elem_classes="input-box",
                )
                
            with gr.Column(scale=1, elem_classes="controls-container"):
                with gr.Row(elem_classes="action-buttons"):
                    send_btn = gr.Button("Send", variant="primary", elem_classes="send-btn")
                    clear_btn = gr.Button("Clear", variant="secondary", elem_classes="clear-btn")
        
        # Input area - IMPROVED LAYOUT FOR ISSUE #3
        with gr.Row(elem_classes="chat-controls"):
            msg = gr.Textbox(
                placeholder="Type your message...",
                label="",
                elem_classes="message-input",
                scale=5
            )
            
            with gr.Column(elem_classes="controls-container", scale=1):
                send_btn = gr.Button("Send", elem_classes="send-btn")
                clear_btn = gr.Button("Clear", elem_classes="clear-btn")
    
    # ── Selection page ───────────────────────────
    with selection_page:
        gr.Markdown("# 🎓 Digital-Twin Chat Demo", elem_classes="main-title")
        gr.Markdown("### Choose a student to chat with")
        
        # Create student selection grid - REVISED LAYOUT FOR 3+3+3+1
        with gr.Column():
            # First row with students 1-3
            with gr.Row(elem_classes="card-grid"):
                for i in range(1, 4):  # Students 1-3
                    student_id = f"student{i:03d}"
                    
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
            
            # Second row with students 4-6
            with gr.Row(elem_classes="card-grid"):
                for i in range(4, 7):  # Students 4-6
                    student_id = f"student{i:03d}"
                    
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
                        
            # Third row with students 7-9
            with gr.Row(elem_classes="card-grid"):
                for i in range(7, 10):  # Students 7-9
                    student_id = f"student{i:03d}"
                    
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
            
            # Fourth row with just student 10 (centered)
            with gr.Row(elem_classes="last-row"):
                student_id = "student010"
                
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

    # JavaScript to force avatar visibility and fix chat display
    demo.load(None, None, None, js="""
    function() {
        // Force circular avatars and make them visible in chat
        const fixChatAvatars = function() {
            // Fix avatar visibility in chatbot
            document.querySelectorAll('.gradio-chatbot .avatar img, .svelte-s88hzt img, [class*="avatar"] img').forEach(function(img) {
                // Fix visibility
                img.style.display = 'block';
                img.style.visibility = 'visible';
                img.style.opacity = '1';
                
                // Fix shape
                img.style.width = '40px';
                img.style.height = '40px';
                img.style.borderRadius = '50%';
                img.style.objectFit = 'cover';
                
                // Fix container
                const container = img.closest('div');
                if (container) {
                    container.style.display = 'block';
                    container.style.visibility = 'visible';
                    container.style.opacity = '1';
                }
            });
            
            // Hide image controls
            document.querySelectorAll('.gradio-image button, .gradio-image .panel-buttons, .gradio-image .absolute').forEach(function(el) {
                el.style.display = 'none';
                el.style.visibility = 'hidden';
                el.style.opacity = '0';
                el.style.pointerEvents = 'none';
            });
            
            // Make selection page avatars circular
            document.querySelectorAll('.avatar-container img, .gradio-image img').forEach(function(img) {
                img.style.borderRadius = '50%';
                img.style.aspectRatio = '1/1';
            });
            
            // Style chat bubbles
            document.querySelectorAll('.gradio-chatbot > div').forEach(function(row) {
                if (!row.classList.contains('styled-chat-row')) {
                    row.classList.add('styled-chat-row');
                    row.style.display = 'flex';
                    row.style.alignItems = 'flex-start';
                    row.style.marginBottom = '15px';
                    
                    // Add margins around avatar and text
                    const avatarContainer = row.querySelector('.avatar');
                    const textContainer = row.querySelector('.message, .block');
                    
                    if (avatarContainer) {
                        avatarContainer.style.marginRight = '10px';
                        avatarContainer.style.marginLeft = '10px';
                    }
                    
                    if (textContainer) {
                        textContainer.classList.add('message-bubble');
                        if (row.classList.contains('user')) {
                            textContainer.classList.add('user-message');
                        } else {
                            textContainer.classList.add('assistant-message');
                        }
                    }
                }
            });
        };
        
        // Apply fixes repeatedly
        fixChatAvatars();
        setInterval(fixChatAvatars, 200);
        
        // Setup mutation observer for real-time updates
        const chatObserver = new MutationObserver(function() {
            fixChatAvatars();
        });
        
        // Start observing
        setTimeout(function() {
            chatObserver.observe(document.body, { 
                childList: true, 
                subtree: true,
                attributes: true
            });
        }, 500);
    }
    """)

# Run the application
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860))
    )
