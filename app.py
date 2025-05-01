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

# 学生描述信息（可以添加更多信息，比如性格、背景等）
student_descriptions = {
    "student001": "16岁，擅长科学与数学，性格内向但乐于助人",
    "student002": "15岁，热爱运动特别是篮球，外向活泼",
    "student003": "17岁，喜欢音乐和艺术，有创意但有些敏感",
    "student004": "16岁，擅长辩论和写作，思维敏捷",
    "student005": "15岁，热爱自然科学，好奇心强",
    "student006": "17岁，社交能力强，喜欢时尚和设计",
    "student007": "16岁，喜欢阅读和写作，有些害羞但思想深刻",
    "student008": "15岁，有领导力，参与多项校园活动",
    "student009": "17岁，数学天才，喜欢解决复杂问题",
    "student010": "16岁，有体育特长，乐观开朗"
}

# 学生使用的模型信息
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

# 学生 ID 和头像文件映射
avatar_dict = {
    sid: f"avatar/{sid}.png" for sid in name_dict.keys()
}

# 保存所有学生的聊天历史
def get_empty_history_dict():
    return {student_id: [] for student_id in name_dict.keys()}

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

# 从选择页面切换到聊天页面
def start_chat_with_student(student_id, history_dict):
    student_name = name_dict.get(student_id, "Unknown")
    student_avatar = avatar_dict.get(student_id, "avatar/default.png")
    student_history = history_dict.get(student_id, [])
    
    # 返回选定学生信息和历史记录以更新聊天界面
    return (
        gr.update(visible=False),  # 隐藏选择页面
        gr.update(visible=True),   # 显示聊天页面
        student_id,
        student_name,
        student_avatar,
        student_history
    )

# 返回到选择页面
def return_to_selection():
    return (
        gr.update(visible=True),   # 显示选择页面
        gr.update(visible=False)   # 隐藏聊天页面
    )

# 自定义CSS
custom_css = """
/* 全局样式 */
body {
    font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
    background-color: #f9f9f9;
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

.back-btn {
    background-color: #f5f5f5 !important;
    color: #666 !important;
    border-radius: 20px !important;
    border: 1px solid #ddd !important;
    margin-right: auto;
}

/* Character Card Styles - 学生选择页面 */
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
}

.character-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.15);
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
}

.chat-btn:hover {
    background-color: #e67e00;
}

/* 聊天界面样式 */
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

/* 响应式调整 */
@media (max-width: 768px) {
    .character-grid {
        grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    }
}
"""

# 创建角色卡片HTML
def create_character_card_html(student_id):
    name = name_dict.get(student_id, "Unknown")
    description = student_descriptions.get(student_id, "No description available")
    avatar = avatar_dict.get(student_id, "avatar/default.png")
    model = model_info.get(student_id, "Unknown Model")
    
    return f"""
    <div class="character-card" id="{student_id}-card" onclick="selectStudent('{student_id}')">
        <div class="card-header">
            <span>Digital Twin</span>
        </div>
        <img class="card-avatar" src="{avatar}">
        <div class="card-body">
            <div class="character-name">{name}</div>
            <div class="character-description">{description}</div>
            <div class="model-tag">Powered by {model}</div>
        </div>
    </div>
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
    selected_id_state = gr.State("")
    
    # ── 选择页面 ───────────────────────────
    with gr.Group(visible=True) as selection_page:
        with gr.Row(elem_classes="header-container"):
            gr.Markdown("# 🎓 Digital-Twin Chat Demo")
        
        with gr.Column():
            gr.Markdown("### 选择一个学生进行对话")
            
            # 使用HTML生成角色卡片网格
            character_grid_html = ""
            for student_id in name_dict.keys():
                character_grid_html += create_character_card_html(student_id)
            
            character_grid = gr.HTML(f'<div class="character-grid">{character_grid_html}</div>')
            
            # 隐藏的按钮，用于JavaScript调用
            select_student_btn = gr.Button("Select", visible=False)
            student_id_input = gr.Textbox("", visible=False)
    
    # ── 聊天页面 ───────────────────────────
    with gr.Group(visible=False) as chat_page:
        # 聊天头部信息
        with gr.Row(elem_classes="chat-header"):
            student_avatar_display = gr.Image(value="avatar/default.png", elem_classes="chat-avatar", show_label=False, height=40, width=40)
            with gr.Column():
                student_name_display = gr.Markdown("Student Name")
                student_model_display = gr.Markdown("Powered by GPT-4", elem_classes="chat-model")
            back_button = gr.Button("← 返回", elem_classes="back-btn")
        
        # 聊天区域
        chatbot = gr.Chatbot(
            label="Conversation",
            avatar_images=("avatar/user.png", "avatar/default.png"),
            elem_classes="chat-area",
            height=450,
        )
        
        # 输入区域
        with gr.Row(elem_classes="input-container"):
            with gr.Column():
                msg = gr.Textbox(
                    placeholder="输入你的消息...",
                    label="",
                    elem_classes="input-box",
                )
                
                with gr.Row(elem_classes="action-buttons"):
                    send_btn = gr.Button("发送", variant="primary", elem_classes="send-btn")
                    clear_btn = gr.Button("清除聊天记录", variant="secondary", elem_classes="clear-btn")
    
    # ── 页面切换逻辑 ─────────────────────────
    # JavaScript函数，用于通过卡片选择学生
    demo.load(js="""
    function selectStudent(studentId) {
        document.getElementById('student_id_input').value = studentId;
        document.getElementById('select_student_btn').click();
    }
    """)
    
    # 切换到聊天页面
    select_student_btn.click(
        start_chat_with_student,
        inputs=[student_id_input, history_dict_state],
        outputs=[
            selection_page, 
            chat_page, 
            selected_id_state, 
            student_name_display, 
            student_avatar_display, 
            chatbot
        ]
    )
    
    # 返回选择页面
    back_button.click(
        return_to_selection,
        inputs=[],
        outputs=[selection_page, chat_page]
    )
    
    # 发送消息
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
    
    # 清除聊天记录
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
