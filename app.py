import gradio as gr
import json
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

with open("shared_prompt.txt", "r") as f:
    shared_prompt = f.read().strip()

# 加载每个学生的完整 prompt
def load_prompts():
    prompts = {}
    for i in range(1, 11):
        path = f"json_prompts/{i}.json"
        if os.path.exists(path):
            with open(path, "r") as f:
                data = json.load(f)
                prompts[f"student{i:03d}"] = shared_prompt + "\n\n" + data["prompt"]
    return prompts

all_prompts = load_prompts()

# 学生编号对应名字
name_dict = {
    "student001": "Liam",
    "student002": "Noah",
    "student003": "James",
    "student004": "Lucas",
    "student005": "Emma",
    "student006": "Ava",
    "student007": "Sophia",
    "student008": "Isabella",
    "student009": "Mia",
    "student010": "Elijah"
}

# 学生编号对应头像路径
avatar_dict = {
    student_id: f"avatar/{student_id}.png" for student_id in name_dict.keys()
}

# 切换学生时保留历史记录，不清空
def select_student(student_id, history):
    if not isinstance(history, list):
        history = []
    return student_id, history, "", ("avatar/default.png", avatar_dict.get(student_id, "avatar/default.png"))

# 聊天函数
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
        return "", history, ("avatar/default.png", avatar_dict.get(student_id, "avatar/default.png"))
    except Exception as e:
        history.append((message, f"\u26a0\ufe0f Error: {str(e)}"))
        return "", history, ("avatar/default.png", avatar_dict.get(student_id, "avatar/default.png"))

# UI 构建
with gr.Blocks() as demo:
    gr.Markdown("## 🎓 Digital Twin Chat Demo")

    with gr.Row():
        with gr.Column(scale=1):
            student_selector = gr.Radio(
                choices=[(name_dict[student_id], student_id) for student_id in name_dict.keys()],
                label="Select a Student",
                value="student001"
            )
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(
                avatar_images=("avatar/default.png", avatar_dict["student001"])
            )
            msg = gr.Textbox(placeholder="Type a message and press Enter...")
            clear = gr.Button("Clear")

    selected_id_state = gr.State("student001")
    history_state = gr.State([])

    student_selector.change(
        select_student,
        [student_selector, history_state],
        [selected_id_state, chatbot, msg, chatbot]
    )

    msg.submit(
        chat,
        [msg, chatbot, selected_id_state],
        [msg, chatbot, chatbot]
    )

    clear.click(lambda: [], None, chatbot, queue=False)

if __name__ == "__main__":
    demo.queue().launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))
