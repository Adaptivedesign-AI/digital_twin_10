import gradio as gr
import json
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# 读取 shared prompt
with open("shared_prompt.txt", "r") as f:
    shared_prompt = f.read().strip()

# 读取各个学生的特定 prompt
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

# 名字和头像
name_dict = {
    "student001": "Jaden",    "student002": "Elijah",   "student003": "Caleb",
    "student004": "Aiden",    "student005": "Ava",      "student006": "Brooklyn",
    "student007": "Zoe",      "student008": "Kayla",    "student009": "Maya",
    "student010": "Isaiah"
}
avatar_dict = {sid: f"avatar/{sid}.png" for sid in name_dict.keys()}

# 当前选择的 student id
selected_id = gr.State("student001")

# 切换学生
def select_student(student_id):
    return student_id, [], gr.update(avatar_images=("avatar/user.png", avatar_dict.get(student_id, "avatar/default.png")))


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
        # 确保返回的数据是长度为 2 的元组
        history.append((message, reply))  # 确保是 (message, reply) 这个格式
        return "", history
    except Exception as e:
        history.append((message, f"⚠️ Error: {str(e)}"))  # 继续以元组形式添加
        return "", history

# 构建 UI
with gr.Blocks(
    theme=gr.themes.Soft(primary_hue="orange"),
    css="""
    .student-radio label {
        display: block !important;
        margin-bottom: 8px;
        font-size: 16px;
    }
    .chat-area {
        min-height: 400px;
    }
    """
) as demo:

    with gr.Row():
        with gr.Column(scale=1):
            student_selector = gr.Radio(
                choices=[(name_dict[sid], sid) for sid in name_dict.keys()],
                label="Select a Student",
                value="student001",
                elem_classes=["student-radio"]
            )
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(
                label="Conversation",
                avatar_images=("avatar/user.png", avatar_dict["student001"]),
                elem_classes="chat-area",
                type="messages"
            )
            msg = gr.Textbox(placeholder="Type your message and press Enter...")
            clear = gr.Button("Clear")

    selected_id_state = gr.State("student001")

    student_selector.change(select_student, student_selector, [selected_id_state, chatbot, chatbot])
    msg.submit(chat, [msg, chatbot, selected_id_state], [msg, chatbot])
    clear.click(lambda: [], None, chatbot, queue=False)

if __name__ == "__main__":
    demo.queue().launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))
