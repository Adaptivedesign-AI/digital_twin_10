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

# Simple interface with fixed pages instead of tabs
def create_demo():
    # Create empty history dictionary
    history_dict = get_empty_history_dict()
    
    # Selection page interface
    with gr.Blocks() as selection_page:
        gr.Markdown("# 🎓 Digital-Twin Chat Demo", elem_classes="main-title")
        gr.Markdown("### Choose a student to chat with")
        
        with gr.Row():
            for i in range(1, 6):  # First row with 5 students
                student_id = f"student{i:03d}"
                with gr.Column(elem_classes="student-card"):
                    gr.Markdown("Digital Twin", elem_classes="student-title")
                    gr.Image(value=f"avatar/{student_id}.png", elem_classes="avatar-img")
                    gr.Markdown(f"### {name_dict[student_id]}", elem_classes="student-name")
                    gr.Markdown(student_descriptions[student_id], elem_classes="student-desc")
                    gr.Markdown(f"Powered by {model_info[student_id]}", elem_classes="model-info")
                    
                    btn = gr.Button(f"Start Chat", elem_classes="chat-button")
                    btn.click(
                        lambda sid=student_id: (sid, name_dict[sid], f"Powered by {model_info[sid]}", 
                                               f"avatar/{sid}.png", history_dict.get(sid, [])),
                        inputs=None,
                        outputs=[
                            student_id_output, 
                            name_display, 
                            model_display,
                            avatar_display,
                            chatbot
                        ]
                    )
                    
        with gr.Row():
            for i in range(6, 11):  # Second row with 5 students
                student_id = f"student{i:03d}"
                with gr.Column(elem_classes="student-card"):
                    gr.Markdown("Digital Twin", elem_classes="student-title")
                    gr.Image(value=f"avatar/{student_id}.png", elem_classes="avatar-img")
                    gr.Markdown(f"### {name_dict[student_id]}", elem_classes="student-name")
                    gr.Markdown(student_descriptions[student_id], elem_classes="student-desc")
                    gr.Markdown(f"Powered by {model_info[student_id]}", elem_classes="model-info")
                    
                    btn = gr.Button(f"Start Chat", elem_classes="chat-button")
                    btn.click(
                        lambda sid=student_id: (sid, name_dict[sid], f"Powered by {model_info[sid]}", 
                                              f"avatar/{sid}.png", history_dict.get(sid, [])),
                        inputs=None,
                        outputs=[
                            student_id_output, 
                            name_display, 
                            model_display,
                            avatar_display,
                            chatbot
                        ]
                    )
    
    # Chat page interface
    with gr.Blocks() as chat_page:
        with gr.Row(elem_classes="chat-header"):
            avatar_display = gr.Image(value="avatar/default.png", elem_classes="chat-avatar")
            
            with gr.Column(elem_classes="chat-info"):
                name_display = gr.Markdown("Student Name", elem_classes="chat-title")
                model_display = gr.Markdown("Powered by GPT-4", elem_classes="chat-subtitle")
                
            back_btn = gr.Button("← Back", elem_classes="back-button")
        
        chatbot = gr.Chatbot(height=500)
        student_id_output = gr.Textbox(visible=False)
        
        with gr.Row():
            msg = gr.Textbox(
                placeholder="Type your message here...",
                show_label=False,
                scale=9
            )
            
            submit_btn = gr.Button("Send", scale=1)
        
        clear_btn = gr.Button("Clear Chat")
        
        # Chat functionality
        def process_message(message, chat_history, student_id):
            if not message or not student_id:
                return "", chat_history
            
            if not message.strip():
                return "", chat_history
            
            # Get existing history from the global dictionary
            existing_history = history_dict.get(student_id, [])
            
            # Ensure chat_history is up to date
            if chat_history != existing_history:
                chat_history = existing_history.copy()
            
            # Process the new message
            messages = [{"role": "system", "content": all_prompts.get(student_id, "You are a helpful assistant.")}]
            for user_msg, bot_reply in chat_history:
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
                
                # Update history
                chat_history.append([message, reply])
                history_dict[student_id] = chat_history
                
                return "", chat_history
            except Exception as e:
                chat_history.append([message, f"⚠️ Error: {str(e)}"])
                history_dict[student_id] = chat_history
                return "", chat_history
        
        # Set up event handlers
        msg.submit(
            process_message,
            inputs=[msg, chatbot, student_id_output],
            outputs=[msg, chatbot]
        )
        
        submit_btn.click(
            process_message,
            inputs=[msg, chatbot, student_id_output],
            outputs=[msg, chatbot]
        )
        
        def clear_chat(student_id):
            if student_id in history_dict:
                history_dict[student_id] = []
            return []
        
        clear_btn.click(
            clear_chat,
            inputs=[student_id_output],
            outputs=[chatbot]
        )
        
        # Button to go back to selection page
        back_btn.click(
            lambda: None,
            None,
            None,
            _js="""
            () => {
                document.getElementById('selection-page').style.display = 'block';
                document.getElementById('chat-page').style.display = 'none';
                return [];
            }
            """
        )
    
    # Main interface with both pages
    with gr.Blocks(css=css) as demo:
        with gr.Box(elem_id="selection-page"):
            selection_page.render()
        
        with gr.Box(elem_id="chat-page", visible=False):
            chat_page.render()
        
        # Set up buttons to navigate between pages
        for btn in selection_page.buttons:
            btn.click(
                fn=None,
                inputs=None,
                outputs=None,
                _js="""
                () => {
                    document.getElementById('selection-page').style.display = 'none';
                    document.getElementById('chat-page').style.display = 'block';
                }
                """
            )
    
    return demo

# Simple CSS to make it look nicer
css = """
#selection-page, #chat-page {
    padding: 20px;
}
.student-card {
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 15px;
    margin: 10px;
    text-align: center;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    background-color: white;
}
.student-card:hover {
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    transform: translateY(-2px);
}
.student-title {
    background-color: #f7931e;
    color: white;
    padding: 10px;
    margin: -15px -15px 15px -15px;
    border-radius: 10px 10px 0 0;
}
.avatar-img {
    width: 80px;
    height: 80px;
    border-radius: 50% !important;
    margin: 10px auto;
    display: block;
    object-fit: cover;
}
.student-name {
    font-weight: bold;
    font-size: 18px;
    margin: 10px 0;
}
.student-desc {
    color: #666;
    margin-bottom: 10px;
    font-size: 14px;
}
.model-info {
    font-size: 12px;
    color: #888;
    background-color: #f5f5f5;
    border-radius: 15px;
    display: inline-block;
    padding: 5px 10px;
    margin: 5px 0;
}
.chat-button {
    background-color: #f7931e;
    color: white;
    border: none;
    border-radius: 20px;
    padding: 8px 15px;
    cursor: pointer;
    margin-top: 10px;
    font-weight: bold;
}
.chat-button:hover {
    background-color: #e57200;
}
.chat-header {
    display: flex;
    align-items: center;
    padding: 10px;
    border-bottom: 1px solid #eee;
    background-color: #f8f9fa;
}
.chat-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50% !important;
    margin-right: 10px;
}
.chat-info {
    flex-grow: 1;
}
.chat-title {
    margin: 0;
    font-size: 16px;
    font-weight: bold;
}
.chat-subtitle {
    margin: 0;
    font-size: 12px;
    color: #666;
}
.main-title {
    background-color: #f7931e;
    color: white;
    padding: 15px;
    margin: 0 0 20px 0;
    text-align: center;
    font-size: 24px;
    font-weight: bold;
}
.back-button {
    background-color: #f5f5f5;
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 5px 10px;
    margin-left: auto;
    cursor: pointer;
}
.back-button:hover {
    background-color: #e0e0e0;
}
/* Hide image controls */
.svelte-1g805jl .panel-buttons, 
.svelte-1g805jl .absolute, 
.svelte-1g805jl .gr-image-tools, 
.svelte-1g805jl button {
    display: none !important;
}
.gradio-container .prose img {
    margin: 0 !important;
}
.gradio-container .panel-image {
    border-radius: 50% !important;
    overflow: hidden !important;
}
"""

# Launch the app
if __name__ == "__main__":
    demo = create_demo()
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860))
    )
