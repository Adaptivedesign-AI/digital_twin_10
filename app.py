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

# Student ID to avatar file mapping
avatar_dict = {
    sid: f"avatar/{sid}.png" for sid in name_dict.keys()
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
    student_avatar = avatar_dict.get(student_id, "avatar/default.png")
    student_history = history_dict.get(student_id, [])
    student_model = get_student_model(student_id)
    
    print(f"Selecting student: {student_id}, name: {student_name}")
    
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

# Custom CSS with improved character.ai style and better cross-device support
custom_css = """
/* Global styles */
body {
    font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
    background-color: #f9f9f9;
}

/* Top orange bar */
.header-container {
    background: linear-gradient(90deg, #f7931e, #ff8c00);
    border-radius: 8px 8px 0 0;
    padding: 16px 24px;
    margin: 0;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.header-container h1 {
    color: white;
    margin: 0;
    font-size: 24px;
    font-weight: 600;
}

.header-icon {
    margin-right: 10px;
    font-size: 28px;
}

/* Main container */
.main-container {
    display: flex;
    border: 1px solid #e0e0e0;
    border-radius: 0 0 8px 8px;
    overflow: hidden;
    background: white;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

/* Chat area */
.chat-area {
    min-height: 450px !important;
    border: none !important;
    background-color: #fafafa !important;
}

.chat-area > div {
    padding: 16px !important;
}

/* Input box and buttons */
.input-container {
    padding: 16px;
    border-top: 1px solid #e0e0e0;
    background-color: white;
}

.input-box {
    border-radius: 20px !important;
    border: 1px solid #e0e0e0 !important;
    padding: 10px 16px !important;
}

.action-buttons {
    display: flex;
    gap: 10px;
    margin-top: 10px;
}

.send-btn {
    background-color: #f7931e !important;
    color: white !important;
    border-radius: 20px !important;
    font-weight: 500 !important;
    flex-grow: 1;
}

.clear-btn {
    background-color: #f5f5f5 !important;
    color: #666 !important;
    border-radius: 20px !important;
    border: 1px solid #ddd !important;
}

.back-btn {
    background-color: #f5f5f5 !important;
    color: #666 !important;
    border-radius: 20px !important;
    border: 1px solid #ddd !important;
    margin-right: auto;
}

/* Character Card Styles - Student selection page */
.character-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
    padding: 20px;
}

.character-card {
    background: white;
    border-radius: 12px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.1);
    overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
    cursor: pointer;
    border: 1px solid #e0e0e0;
    position: relative; /* For card click */
}

.character-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.15);
}

/* Add transparent overlay for better click experience */
.card-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    cursor: pointer;
    z-index: 10;
}

.card-header {
    padding: 15px;
    background-color: #f7931e;
    color: white;
    text-align: center;
}

.card-avatar {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    margin: 15px auto;
    display: block;
    object-fit: cover;
    border: 3px solid white;
    box-shadow: 0 3px 8px rgba(0,0,0,0.15);
    background-color: #f0f0f0;  /* Fallback background */
}

.card-body {
    padding: 15px;
    text-align: center;
}

.character-name {
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 5px;
}

.character-description {
    font-size: 14px;
    color: #666;
    margin-bottom: 10px;
    height: 60px;
    overflow: hidden;
}

.model-tag {
    display: inline-block;
    background-color: #f0f0f0;
    padding: 5px 10px;
    border-radius: 15px;
    font-size: 12px;
    color: #555;
    margin-top: 5px;
}

.chat-btn {
    background-color: #f7931e;
    color: white;
    border: none;
    border-radius: 20px;
    padding: 8px 16px;
    font-weight: 500;
    cursor: pointer;
    width: 100%;
    margin-top: 15px;
    transition: background-color 0.2s;
    position: relative;
    z-index: 20; /* Ensure button is above overlay */
}

.chat-btn:hover {
    background-color: #e67e00;
}

/* Chat interface styles */
.chat-header {
    display: flex;
    align-items: center;
    padding: 15px;
    background-color: #f8f9fa;
    border-bottom: 1px solid #e0e0e0;
}

.chat-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    margin-right: 15px;
}

.chat-name {
    font-size: 18px;
    font-weight: 500;
}

.chat-model {
    font-size: 12px;
    color: #666;
    margin-left: 10px;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .character-grid {
        grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    }
}

/* Fix for desktop click issues */
button {
    cursor: pointer;
    /* Prevent button events from being captured by other elements */
    position: relative;
    z-index: 20;
}

.chat-btn {
    pointer-events: auto !important;
}

.gradio-button {
    user-select: none;
}

/* Avoid text selection triggering card click */
* {
    user-select: none;
}
"""

# Create HTML for student grid - using a function to avoid f-string issues
def create_student_grid_html():
    cards_html = ""
    for student_id in name_dict.keys():
        name = name_dict[student_id]
        desc = student_descriptions[student_id]
        model = model_info[student_id]
        
        card_html = f"""
        <div class="character-card" id="card-{student_id}" data-student-id="{student_id}">
            <div class="card-header">Digital Twin</div>
            <img src="avatar/{student_id}.png" class="card-avatar" />
            <div class="card-body">
                <div class="character-name">{name}</div>
                <div class="character-description">{desc}</div>
                <div class="model-tag">Powered by {model}</div>
                <button class="chat-btn" id="btn-{student_id}" data-student-id="{student_id}">Start Chat</button>
            </div>
        </div>
        """
        cards_html += card_html
    
    # Full HTML with JavaScript
    grid_html = f"""
    <div class="character-grid">
        {cards_html}
    </div>
    <script>
    document.addEventListener('DOMContentLoaded', function() {{
        console.log("Adding click events to buttons");
        
        // Add click events to all Start Chat buttons
        document.querySelectorAll('.chat-btn').forEach(button => {{
            button.addEventListener('click', function(e) {{
                e.preventDefault();
                e.stopPropagation();
                
                const studentId = this.getAttribute('data-student-id');
                console.log("Button clicked for student:", studentId);
                
                // Find the hidden input field and set studentId as its value
                const hiddenInput = document.getElementById('student-id-input');
                if(hiddenInput) {{
                    hiddenInput.value = studentId;
                    
                    // Trigger submit event
                    const submitEvent = new Event('input', {{ bubbles: true }});
                    hiddenInput.dispatchEvent(submitEvent);
                    
                    // Click the hidden submit button
                    const submitButton = document.getElementById('select-student-btn');
                    if(submitButton) {{
                        submitButton.click();
                    }}
                }}
            }});
        }});
        
        // Also add click events to the entire card
        document.querySelectorAll('.character-card').forEach(card => {{
            card.addEventListener('click', function(e) {{
                // Prevent bubbling to Start Chat button
                if(e.target.classList.contains('chat-btn')) return;
                
                const studentId = this.getAttribute('data-student-id');
                console.log("Card clicked for student:", studentId);
                
                // Trigger the corresponding button click
                const button = document.getElementById(`btn-${{studentId}}`);
                if(button) {{
                    button.click();
                }}
            }});
        }});
    }});
    </script>
    """
    
    return grid_html

# --------------------------------------------
# = UI BUILDING =
# --------------------------------------------
with gr.Blocks(
    theme=gr.themes.Soft(primary_hue="orange"),
    css=custom_css
) as demo:

    # State variables
    history_dict_state = gr.State(get_empty_history_dict())
    selected_id_state = gr.State("")
    
    # Create main pages
    selection_page = gr.Group(visible=True)
    chat_page = gr.Group(visible=False)
    
    # Define chat page components
    with chat_page:
        # Chat header
        with gr.Row(elem_classes="chat-header"):
            student_avatar_display = gr.Image(
                value="avatar/default.png", 
                elem_classes="chat-avatar", 
                show_label=False, 
                height=40, 
                width=40
            )
            with gr.Column():
                student_name_display = gr.Markdown("Student Name")
                student_model_display = gr.Markdown("Powered by GPT-4", elem_classes="chat-model")
            back_button = gr.Button("← Back", elem_classes="back-btn")
            
        # Chat area
        chatbot = gr.Chatbot(
            label="Conversation",
            avatar_images=("avatar/user.png", None),
            elem_classes="chat-area",
            height=450,
        )
        
        # Input area
        with gr.Row(elem_classes="input-container"):
            with gr.Column():
                msg = gr.Textbox(
                    placeholder="Type your message...",
                    label="",
                    elem_classes="input-box",
                )
                
                with gr.Row(elem_classes="action-buttons"):
                    send_btn = gr.Button("Send", variant="primary", elem_classes="send-btn")
                    clear_btn = gr.Button("Clear Chat", variant="secondary", elem_classes="clear-btn")
    
    # Define selection page
    with selection_page:
        with gr.Row(elem_classes="header-container"):
            gr.Markdown("# 🎓 Digital-Twin Chat Demo")
        
        gr.Markdown("### Choose a student to chat with")
        
        # Create student selection cards using HTML (as a function)
        students_grid = gr.HTML(create_student_grid_html())
        
        # Create hidden components for student selection
        student_id_input = gr.Textbox(value="", visible=False, elem_id="student-id-input")
        select_student_btn = gr.Button("Select", visible=False, elem_id="select-student-btn")
            
    # Event handlers 
    # Student selection button click event
    select_student_btn.click(
        select_student_direct,
        inputs=[student_id_input, history_dict_state],
        outputs=[selection_page, chat_page, selected_id_state, 
                student_name_display, student_model_display,
                student_avatar_display, chatbot]
    )
    
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

# Run the application
if __name__ == "__main__":
    print("Starting application...")
    print(f"Avatar paths: {avatar_dict}")
    
    # Ensure avatar directory exists
    if not os.path.exists("avatar"):
        os.makedirs("avatar")
        print("Created avatar directory")
        
    # Create default user avatar
    if not os.path.exists("avatar/user.png"):
        print("Creating default user avatar")
        with open("avatar/user.png", "w") as f:
            f.write("")
            
    demo.queue().launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860)),
        debug=True,  # Enable debug mode
        max_threads=20  # Increase threads
    )
