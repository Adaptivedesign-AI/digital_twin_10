import gradio as gr
import json
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Load shared prompt
with open("shared_prompt.txt", "r") as f:
    shared_prompt = f.read().strip()

# Load all prompts
all_prompts = {}
for i in range(1, 11):
    sid = f"student{i:03d}"
    path = f"prompts/{i}.json"
    if os.path.exists(path):
        with open(path, "r") as f:
            data = json.load(f)
            all_prompts[sid] = shared_prompt + "\n\n" + data["prompt"]

# Name and avatar mapping
name_dict = {
    "student001": "Jaden", "student002": "Elijah", "student003": "Caleb",
    "student004": "Aiden", "student005": "Ava", "student006": "Brooklyn",
    "student007": "Zoe", "student008": "Kayla", "student009": "Maya", "student010": "Isaiah"
}

avatar_dict = {sid: f"avatar/{sid}.png" for sid in name_dict.keys()}

# Maintain history per student
history_store = {sid: [] for sid in name_dict.keys()}
selected_id = gr.State("student001")

# On student change
def select_student(student_id):
    return (
        student_id,
        history_store.get(student_id, []),
        gr.update(avatar_images=("avatar/user.png", avatar_dict.get(student_id, "avatar/default.png")))
    )

# Chat logic

def chat(message, history, student_id):
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
        history_store[student_id] = history
        return "", history
    except Exception as e:
        history.append([message, f"⚠️ Error: {str(e)}"])
        return "", history

# UI Layout
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🎓 Digital Twin Chat Demo
    Select a student from the left and begin chatting. Each twin retains their memory!
    """)

    with gr.Row():
        with gr.Column(scale=1):
            student_selector = gr.Radio(
                choices=[(name_dict[sid], sid) for sid in name_dict],
                label="Select a Student",
                value="student001",
                interactive=True
            )
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(
                label="Conversation",
                avatar_images=("avatar/user.png", avatar_dict["student001"])
            )
            msg = gr.Textbox(placeholder="Type your message and press Enter...", show_label=False)
            clear = gr.Button("Clear", elem_classes="rounded")

    student_selector.change(select_student, student_selector, [selected_id, chatbot, chatbot])
    msg.submit(chat, [msg, chatbot, selected_id], [msg, chatbot])
    clear.click(lambda: [], None, chatbot, queue=False)

if __name__ == "__main__":
    demo.queue().launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))
