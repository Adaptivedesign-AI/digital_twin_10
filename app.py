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

# Direct student selection function - simplified for better compatibility
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

# This CSS focuses on completely hiding image controls and enforcing circular avatars
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

/* Card styling */
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
    margin-left: auto !important;
}

/* CRITICAL: Avatar styling and controls hiding */
/* For the avatar images in the cards */
.avatar-container {
    position: relative;
    width: 100px;
    height: 100px;
    margin: 15px auto;
    border-radius: 50%;
    overflow: hidden;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    border: 3px solid white;
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

/* Input and buttons styling */
.message-input {
    border-radius: 20px !important;
    padding: 10px 15px !important;
    border: 1px solid #e0e0e0 !important;
}

.send-btn {
    background-color: #f7931e !important;
    color: white !important;
    border: none !important;
    border-radius: 20px !important;
    padding: 8px 15px !important;
}

.clear-btn {
    background-color: #f0f0f0 !important;
    color: #555 !important;
    border: 1px solid #ddd !important;
    border-radius: 5px !important;
}

/* Force image controls to be hidden with !important */
.gradio-image .p-absolute,
.gradio-image div[class^="flex"],
.gradio-image div[class*="flex"] {
    display: none !important;
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
            
        # Chat area
        chatbot = gr.Chatbot(
            label="Conversation",
            avatar_images=("avatar/user.png", None),
            height=450,
        )
        
        # Input area
        with gr.Row():
            msg = gr.Textbox(
                placeholder="Type your message...",
                label="",
                elem_classes="message-input",
            )
            
            send_btn = gr.Button("Send", elem_classes="send-btn")
        
        clear_btn = gr.Button("Clear Chat", elem_classes="clear-btn")
    
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

    # JavaScript to fix image display and hide controls
    demo.load(None, None, None, js="""
    function() {
        // Force hide image controls
        setInterval(function() {
            // Hide all image controls
            document.querySelectorAll('.gradio-image button, .gradio-image .panel-buttons, .gradio-image .absolute').forEach(function(el) {
                el.style.display = 'none';
                el.style.visibility = 'hidden';
                el.style.opacity = '0';
                el.style.pointerEvents = 'none';
            });
            
            // Make all images circular
            document.querySelectorAll('.gradio-image img').forEach(function(img) {
                img.style.borderRadius = '50%';
                img.style.objectFit = 'cover';
            });
        }, 100);
    }
    """)

# Run the application
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860))
    )
