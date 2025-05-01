import gradio as gr
import json
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# 加载 shared_prompt.txt
with open("shared_prompt.txt", "r") as f:
    shared_prompt = f.read().strip()

# 加载所有 prompts（拼接 shared + individual）
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

# 学生 ID 和名字映射
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

# 学生 ID 和头像文件映射
avatar_dict = {
    sid: f"avatar/{sid}.png" for sid in name_dict.keys()
}

# 保存所有学生的聊天历史
def get_empty_history_dict():
    return {student_id: [] for student_id in name_dict.keys()}

# 切换学生，保持各自聊天历史
def select_student(student_id, history_dict):
    # 返回选定学生的历史记录
    return student_id, history_dict, history_dict.get(student_id, []), gr.update(avatar_images=("avatar/user.png", avatar_dict.get(student_id, "avatar/default.png")))

# 聊天函数
def chat(message, history, student_id, history_dict):
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
        # 更新历史记录字典
        history_dict[student_id] = history
        return "", history, history_dict
    except Exception as e:
        history.append((message, f"⚠️ Error: {str(e)}"))
        history_dict[student_id] = history
        return "", history, history_dict

# 清除当前学生的聊天历史
def clear_current_chat(student_id, history_dict):
    history_dict[student_id] = []
    return [], history_dict

# 自定义CSS
custom_css = """
/* 全局样式 */
body {
    font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
}

/* 顶部橙色栏 */
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

/* 主容器 */
.main-container {
    display: flex;
    border: 1px solid #e0e0e0;
    border-radius: 0 0 8px 8px;
    overflow: hidden;
    background: white;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

/* 学生选择器 */
.student-radio {
    padding: 15px;
    background-color: #f8f9fa;
    border-right: 1px solid #e0e0e0;
}

.student-radio label {
    display: flex !important;
    align-items: center;
    padding: 10px;
    margin-bottom: 8px;
    border-radius: 8px;
    transition: all 0.2s;
    cursor: pointer;
}

.student-radio label:hover {
    background-color: #f0f0f0;
}

.student-radio input:checked + label {
    background-color: #fff3e0;
    border-left: 3px solid #f7931e;
    font-weight: 500;
}

/* 聊天区域 */
.chat-area {
    min-height: 450px !important;
    border: none !important;
    background-color: #fafafa !important;
}

.chat-area > div {
    padding: 16px !important;
}

/* 输入框和按钮 */
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

/* 响应式调整 */
@media (max-width: 768px) {
    .main-container {
        flex-direction: column;
    }
    
    .student-radio {
        border-right: none;
        border-bottom: 1px solid #e0e0e0;
    }
}
"""

# --------------------------------------------
# ＝ UI 构建 ＝
# --------------------------------------------
with gr.Blocks(
    theme=gr.themes.Soft(primary_hue="orange"),
    css=custom_css
) as demo:

    # ── 历史记录状态（所有学生） ──────────
    history_dict_state = gr.State(get_empty_history_dict())

    # ── 顶栏 ───────────────────────────
    with gr.Row(elem_classes="header-container"):
        gr.Markdown("# 🎓 Digital-Twin Chat Demo")

    # ── 主体 ───────────────────────────
    with gr.Row(elem_classes="main-container"):
        # 左侧：学生选择器
        with gr.Column(scale=1, elem_classes="student-radio"):
            gr.Markdown("### Select a Student")
            student_selector = gr.Radio(
                choices=[(name_dict[sid], sid) for sid in name_dict],
                value="student001",
                label="",
                elem_classes=["student-radio"],
            )

        # 右侧：聊天 + 输入
        with gr.Column(scale=3):
            # 聊天区域
            chatbot = gr.Chatbot(
                label="Conversation",
                avatar_images=("avatar/user.png", avatar_dict["student001"]),
                elem_classes="chat-area",
                height=450,
            )
            
            # 输入区域
            with gr.Row(elem_classes="input-container"):
                with gr.Column():
                    msg = gr.Textbox(
                        placeholder="Type a message and press Enter...",
                        label="",
                        elem_classes="input-box",
                    )
                    
                    with gr.Row(elem_classes="action-buttons"):
                        send_btn = gr.Button("Send", variant="primary", elem_classes="send-btn")
                        clear_btn = gr.Button("Clear", variant="secondary", elem_classes="clear-btn")

    # ── 状态：当前选中学生 ───────────────
    selected_id_state = gr.State("student001")

    # ── 交互绑定 ─────────────────────────
    student_selector.change(
        select_student,
        inputs=[student_selector, history_dict_state],
        outputs=[selected_id_state, history_dict_state, chatbot, chatbot],
    )

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

    clear_btn.click(
        clear_current_chat,
        inputs=[selected_id_state, history_dict_state],
        outputs=[chatbot, history_dict_state],
        queue=False
    )

# ── 运行 ───────────────────────────────
if __name__ == "__main__":
    demo.queue().launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860)),
    )
