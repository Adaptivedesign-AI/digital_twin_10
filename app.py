import gradio as gr
import json
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Load shared prompt
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
    "student001": "16 years old. Quiet and thoughtful. Loves sports but keeps emotions to himself.",
    "student002": "15 years old. Restless and impulsive. Often skips school and feels overwhelmed.",
    "student003": "17 years old. Withdrawn and isolated. Struggles with sadness and low energy.",
    "student004": "16 years old. Top of class. Perfectionist who avoids risks and stays cautious.",
    "student005": "15 years old. Sensitive and anxious. Rarely sleeps well and feels out of control.",
    "student006": "17 years old. Shy and socially anxious. Finds it hard to speak up or connect.",
    "student007": "16 years old. Positive and motivated. Tries hard at school and helps others.",
    "student008": "15 years old. Mature and calm. Focused on school, avoids conflict and drama.",
    "student009": "17 years old. Quiet and independent. Rarely opens up but stays composed.",
    "student010": "16 years old. Athletic and confident. Faces family stress but feels strong at school."
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
    student_history = history_dict.get(student_id, [])
    student_model = get_student_model(student_id)
    
    return (
        gr.update(visible=False),  # Hide selection page
        gr.update(visible=True),   # Show chat page
        student_id,                # Update selected student ID
        f"# {student_name}",       # Update student name display
        student_model,             # Update model display
        student_history            # Update chat history
    )

# Return to selection page
def return_to_selection():
    return (
        gr.update(visible=True),   # Show selection page
        gr.update(visible=False)   # Hide chat page
    )

# Enhanced CSS for better UI with Character.ai style
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

/* Character.ai style grid for selection page - now 5 columns */
.character-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 10px;
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
}

/* Responsive breakpoints for character grid */
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

/* Card styling - more compact for 5-column layout */
.character-card {
    background: white;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
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
    box-shadow: 0 4px 10px rgba(0,0,0,0.12);
}

.card-header {
    background-color: #f7931e;
    color: white;
    padding: 6px;
    text-align: center;
    font-weight: bold;
    font-size: 13px;
}

/* Student info styling - even more compact */
.student-name {
    font-size: 16px;
    font-weight: bold;
    margin: 6px 0 2px;
    text-align: center;
}

.student-description {
    padding: 0 10px;
    text-align: center;
    color: #555;
    font-size: 12px;
    min-height: 45px;
    overflow: hidden;
    flex-grow: 1;
    margin-bottom: 4px;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
}

.model-tag {
    background-color: #f0f0f0;
    border-radius: 12px;
    padding: 3px 6px;
    margin: 4px auto;
    display: inline-block;
    font-size: 10px;
    color: #666;
    text-align: center;
}

/* Avatar styling in selection cards - smaller for 5 columns */
.avatar-container {
    width: 70px;
    height: 70px;
    margin: 10px auto 6px;
    border-radius: 50%;
    overflow: hidden;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    border: 2px solid white;
}

.avatar-container img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 50%;
}

/* Chat button styling */
.chat-btn {
    background-color: #f7931e !important;
    color: white !important;
    border: none !important;
    border-radius: 20px !important;
    padding: 5px 0 !important;
    margin: 6px auto 10px !important;
    width: 85% !important;
    display: block !important;
    font-weight: bold !important;
    cursor: pointer !important;
    font-size: 13px !important;
}

.chat-btn:hover {
    background-color: #e67e00 !important;
}

/* Chat interface styling */
.chat-header {
    display: flex;
    align-items: center;
    padding: 15px;
    border-bottom: 1px solid #eee;
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

/* Input and buttons styling */
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
    background-color: #f7931e !important;
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

/* Student name styling */
.student-name-header {
    font-size: 22px;
    font-weight: bold;
    margin: 0;
}

/* Model display styling */
.model-display {
    margin-top: 4px;
    font-size: 12px;
    color: #666;
}

/* Character.ai style chat styling */
.character-ai-style {
    border-radius: 12px;
    background-color: white;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

/* Custom styling for chat bubbles */
.chatbot-row {
    display: flex;
    margin-bottom: 20px;
}

/* TINY AVATARS - now 6px instead of 12px */
.gradio-chatbot .avatar {
    display: block !important;
    width: 6px !important;
    height: 6px !important;
    border-radius: 50% !important;
    margin-right: 4px !important;
    margin-top: 5px !important;
    flex-shrink: 0 !important;
}

/* Make sure the avatars are visible and styled correctly with micro size */
.gradio-chatbot .message-wrap.user .avatar,
.gradio-chatbot .message-wrap.bot .avatar {
    display: inline-block !important;
    width: 6px !important;
    height: 6px !important;
    border-radius: 50% !important;
    overflow: hidden !important;
    margin-right: 4px !important;
    flex-shrink: 0 !important;
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
}

/* User message styling */
.gradio-chatbot .message.user {
    background-color: #f7931e !important;
    color: white !important;
    border-bottom-right-radius: 4px !important;
    margin-left: auto !important;
}

/* Bot message styling */
.gradio-chatbot .message.bot {
    background-color: #f1f1f1 !important;
    color: #333 !important;
    border-bottom-left-radius: 4px !important;
    margin-right: auto !important;
}

/* Emotion tag styling */
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

/* Override default gradio chatbot styling for tiny avatars */
.gradio-container .prose img.avatar-image {
    display: inline-block !important;
    margin: 0 !important;
    border-radius: 50% !important;
    width: 12px !important;
    height: 12px !important;
}

/* Selection heading styling */
.selection-heading {
    text-align: center;
    margin: 20px 0 10px;
    color: #333;
    font-size: 20px;
}

/* Container for the main content */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 24px;
}

/* Fix any Gradio spacing issues */
.gradio-container {
    max-width: 100% !important;
}

/* Hide unnecessary margins */
.block {
    margin-bottom: 0 !important;
}

/* Center the name and model in the chat header */
.center-header {
    margin: 0 auto;
    text-align: center;
}

/* Add more whitespace around messages */
.gradio-chatbot .message-wrap {
    margin-bottom: 10px !important;
}

/* Adjust spacing for better alignment with tiny avatars */
.gradio-chatbot .message-wrap > div {
    display: flex !important;
    align-items: flex-start !important;
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
        # Chat header with student info - REMOVED avatar, centered student info
        with gr.Row(elem_classes="chat-header"):
            back_button = gr.Button("← Back", elem_classes="back-btn")
            
            # Student information - centered, no avatar
            with gr.Column(elem_classes="center-header"):
                name_display = gr.Markdown("Student Name")
                model_display = gr.Markdown("Powered by GPT-4", elem_classes="model-tag")
            
        # Chat area with avatars
        chatbot = gr.Chatbot(
            label="Conversation",
            avatar_images=("avatar/user.png", None),  # Will be updated dynamically
            height=450,
            elem_classes="character-ai-style chatbox-container",
            show_label=True,
            show_copy_button=True,
        )
        
        # Input area with improved layout
        with gr.Row():
            # Left column for text input
            with gr.Column(scale=5):
                msg = gr.Textbox(
                    placeholder="Type your message...",
                    label="",
                    elem_classes="message-input",
                )
            
            # Right column for buttons (stacked vertically)
            with gr.Column(scale=1, elem_classes="button-container"):
                send_btn = gr.Button("Send", elem_classes="send-btn")
                clear_btn = gr.Button("Clear", elem_classes="clear-btn")
    
    # ── Selection page - Now with responsive 5-column grid like Character.ai ───────────────────────────
    with selection_page:
        with gr.Column(elem_classes="container"):
            gr.Markdown("# 🎓 Digital-Twin Chat Demo", elem_classes="main-title")
            gr.Markdown("### Choose a student to chat with", elem_classes="selection-heading")
            
            # Create a single responsive grid for all students - now 5 columns
            with gr.Column(elem_classes="character-grid"):
                # Loop through all 10 students to create a 5-column grid
                for i in range(0, 10):
                    student_id = f"student{i+1:03d}"
                    
                    with gr.Column(elem_classes="character-card"):
                        gr.Markdown("Digital Twin", elem_classes="card-header")
                        
                        # Avatar container
                        with gr.Column(elem_classes="avatar-container"):
                            gr.Image(
                                value=f"avatar/{student_id}.png",
                                show_label=False,
                                elem_classes="avatar-img"
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
                                chatbot
                            ]
                        )

    # Function to update avatar_images in chatbot
    def update_chatbot_avatars(student_id):
        user_avatar = "avatar/user.png"
        bot_avatar = f"avatar/{student_id}.png"
        return gr.update(avatar_images=(user_avatar, bot_avatar))
        
    # Event to update avatars when student is selected
    selected_id_state.change(
        update_chatbot_avatars,
        inputs=[selected_id_state],
        outputs=[chatbot]
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

    # JavaScript to ensure avatars display correctly and at the much smaller size
    demo.load(None, None, None, js="""
    function() {
        // Keep checking and fixing the avatars periodically to ensure they're tiny
        setInterval(function() {
            // Ensure avatar images are visible but TINY (12px)
            document.querySelectorAll('.gradio-chatbot .avatar').forEach(function(avatar) {
                avatar.style.display = 'inline-block';
                avatar.style.width = '6px';
                avatar.style.height = '6px';
                avatar.style.marginRight = '4px';
                avatar.style.borderRadius = '50%';
                avatar.style.marginTop = '4px';
            });
            
            // Format message bubbles
            document.querySelectorAll('.gradio-chatbot .message').forEach(function(msg) {
                msg.style.borderRadius = '18px';
                msg.style.padding = '12px 16px';
                msg.style.maxWidth = '80%';
                
                if (msg.classList.contains('user')) {
                    msg.style.backgroundColor = '#f7931e';
                    msg.style.color = 'white';
                    msg.style.borderBottomRightRadius = '4px';
                } else {
                    msg.style.backgroundColor = '#f1f1f1';
                    msg.style.color = '#333';
                    msg.style.borderBottomLeftRadius = '4px';
                }
            });
            
            // Make character cards clickable (entire card, not just button)
            document.querySelectorAll('.character-card').forEach(function(card) {
                card.style.cursor = 'pointer';
                card.addEventListener('click', function(e) {
                    // Find and click the button within this card
                    const button = this.querySelector('.chat-btn');
                    if (button && e.target !== button) {
                        button.click();
                    }
                });
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
