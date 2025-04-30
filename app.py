import gradio as gr
import json
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# 加载所有 prompts（假设位于 ./prompt_10/1.json, ..., 10.json）
def load_prompts():
    prompts = {}
    for i in range(1, 11):
        path = f"prompt_10/{i}.json"
        if os.path.exists(path):
            with open(path, "r") as f:
                data = json.load(f)
                prompts[f"student{i:03d}"] = data["prompt"]  # 保证 key 是 student001 ~ student010
    return prompts

all_prompts = load_prompts()

# 当前选择的 student_id
selected_id = gr.State("student001")

def select_student(student_id):
    return student_id, [], ""  # 清空聊天记录

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
        history.append((message, reply))
        return "", history
    except Exception as e:
        return "", history + [(message, f"⚠️ Error: {str(e)}")]

with gr.Blocks() as demo:
    gr.Markdown("## 🎓 Digital Twin Chat Demo")
    with gr.Row():
        with gr.Column(scale=1):
            student_selector = gr.Radio(
                choices=[f"student{i:03d}" for i in range(1, 11)],
                label="Select a Student",
                value="student001"
            )
        with gr.Column(scale=3):
            chatbot = gr.Chatbot()
            msg = gr.Textbox(placeholder="Type a message and press Enter...")
            clear = gr.Button("Clear")

    selected_id_state = gr.State("student001")

    student_selector.change(select_student, student_selector, [selected_id_state, chatbot, msg])
    msg.submit(chat, [msg, chatbot, selected_id_state], [msg, chatbot])
    clear.click(lambda: [], None, chatbot, queue=False)

if __name__ == "__main__":
    demo.queue().launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))
