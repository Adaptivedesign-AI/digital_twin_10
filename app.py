import os
import json
import gradio as gr
from openai import OpenAI

# 初始化 OpenAI 客户端（记得设置 OPENAI_API_KEY 环境变量）
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# 加载 shared_prompt.txt
with open("shared_prompt.txt", "r") as f:
    shared_prompt = f.read().strip()

# 加载每个角色的个性化 prompt
student_prompts = {}
for i in range(1, 11):
    with open(f"prompt_10/{i}.json", "r") as f:
        prompt_data = json.load(f)
        student_id = f"student{str(i).zfill(3)}"
        student_prompts[student_id] = prompt_data["prompt"]

# 初始化每个角色的聊天记录
chat_histories = {sid: [] for sid in student_prompts}

# 当前选中的角色（默认 student001）
selected_student = gr.State("student001")

# 拼接完整的 system prompt
def get_full_prompt(student_id):
    return shared_prompt + "\n\n" + student_prompts[student_id]

# 聊天函数
def chat(message, history, student_id):
    full_prompt = get_full_prompt(student_id)
    messages = [{"role": "system", "content": full_prompt}]
    
    for user_msg, bot_msg in history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": bot_msg})
    
    messages.append({"role": "user", "content": message})

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7
        )
        reply = response.choices[0].message.content.strip()
        history.append((message, reply))
        chat_histories[student_id] = history
        return "", history
    except Exception as e:
        error_msg = f"Sorry, an error occurred: {str(e)}"
        history.append((message, error_msg))
        return "", history

# 切换角色时加载对应历史
def switch_student(student_id):
    return chat_histories[student_id]

# UI
with gr.Blocks(title="Digital Twin Chat Demo") as demo:
    gr.Markdown("🎓 **Digital Twin Chat Demo**")

    with gr.Row():
        with gr.Column(scale=1):
            radio = gr.Radio(
                choices=list(student_prompts.keys()),
                value="student001",
                label="Select a Student",
                interactive=True
            )
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(label="Chatbot", height=500)
            msg = gr.Textbox(
            placeholder="Type a message...",
            show_label=False,
            lines=2
        )
        send = gr.Button("Send")
        clear = gr.Button("Clear")
        
        # 显式点击发送按钮
        send.click(
            chat,
            inputs=[msg, chatbot, radio],
            outputs=[msg, chatbot]
        )
        
        # 清空聊天记录
        clear.click(
            lambda: [],
            inputs=None,
            outputs=chatbot
        )




# 本地或 Render 启动服务
if __name__ == "__main__":
    demo.queue(api_open=True).launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860))
    )
