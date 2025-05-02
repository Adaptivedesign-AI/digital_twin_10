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

# Global history dictionary
history_dict = {student_id: [] for student_id in name_dict.keys()}

def chat(message, history, student_id):
    if not message or not message.strip():
        return "", history
        
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
        # Update global history
        history_dict[student_id] = history
        return "", history
    except Exception as e:
        history.append([message, f"⚠️ Error: {str(e)}"])
        history_dict[student_id] = history
        return "", history

# Create one interface per student
def build_interface():
    # Definition of all interfaces
    student_interfaces = {}
    demo = gr.Blocks(title="Digital-Twin Chat Demo")
    
    # Create a selection page
    with demo:
        # Main title
        gr.Markdown("# 🎓 Digital-Twin Chat Demo", elem_class="title")
        gr.Markdown("### Choose a student to chat with")
        
        # Create a grid layout for students
        with gr.Row():
            for i in range(1, 6):  # First row
                student_id = f"student{i:03d}"
                with gr.Column():
                    with gr.Box() as student_card:
                        gr.Markdown(f"## {name_dict[student_id]}")
                        gr.Image(value=f"avatar/{student_id}.png", width=100, height=100)
                        gr.Markdown(student_descriptions[student_id])
                        gr.Markdown(f"*{model_info[student_id]}*")
                        gr.Button(f"Chat with {name_dict[student_id]}").click(
                            lambda sid=student_id: sid, 
                            None, 
                            student_id_state
                        )
        
        with gr.Row():
            for i in range(6, 11):  # Second row
                student_id = f"student{i:03d}"
                with gr.Column():
                    with gr.Box() as student_card:
                        gr.Markdown(f"## {name_dict[student_id]}")
                        gr.Image(value=f"avatar/{student_id}.png", width=100, height=100)
                        gr.Markdown(student_descriptions[student_id])
                        gr.Markdown(f"*{model_info[student_id]}*")
                        gr.Button(f"Chat with {name_dict[student_id]}").click(
                            lambda sid=student_id: sid, 
                            None, 
                            student_id_state
                        )
        
        # Hidden chat interface
        with gr.Group(visible=False) as chat_interface:
            gr.Markdown("# Chat with Student")
            
            # Display student info
            with gr.Row():
                student_image = gr.Image(label="Student", width=100, height=100)
                with gr.Column():
                    student_name = gr.Markdown("Student Name")
                    student_desc = gr.Markdown("Student Description")
                    student_model = gr.Markdown("Model Info")
            
            # Chat interface
            chatbot = gr.Chatbot(height=400)
            
            with gr.Row():
                message = gr.Textbox(placeholder="Type your message here...", scale=4)
                submit_btn = gr.Button("Send", scale=1)
            
            clear_btn = gr.Button("Clear Chat")
            back_btn = gr.Button("← Back to Selection")
            
            # Handle sending messages
            message.submit(chat, [message, chatbot, student_id_state], [message, chatbot])
            submit_btn.click(chat, [message, chatbot, student_id_state], [message, chatbot])
            
            # Clear chat
            clear_btn.click(
                lambda sid: ([], []),
                [student_id_state],
                [chatbot]
            )
            
            # Go back to selection
            back_btn.click(
                lambda: gr.update(visible=True), 
                None, 
                demo.children[0]
            ).then(
                lambda: gr.update(visible=False),
                None,
                chat_interface
            )
            
        # Student ID state to track which student is selected
        student_id_state = gr.State("")
        
        # Set up the page switching
        def update_chat_interface(student_id):
            if not student_id:
                return [gr.update(visible=False)] * 5
            
            # Show chat interface and hide selection
            name = name_dict.get(student_id, "Unknown")
            desc = student_descriptions.get(student_id, "")
            model = model_info.get(student_id, "")
            img = f"avatar/{student_id}.png"
            
            # Get chat history
            history = history_dict.get(student_id, [])
            
            return [
                gr.update(visible=False),  # Selection page
                gr.update(visible=True),   # Chat interface
                gr.update(value=img),      # Student image
                gr.update(value=f"# {name}"),  # Student name
                gr.update(value=desc),     # Student description
                gr.update(value=model),    # Student model
                gr.update(value=history)   # Chat history
            ]
        
        student_id_state.change(
            update_chat_interface,
            [student_id_state],
            [demo.children[0], chat_interface, student_image, student_name, student_desc, student_model, chatbot]
        )
    
    return demo

# Launch the app
if __name__ == "__main__":
    demo = build_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860)),
        share=True
    )
