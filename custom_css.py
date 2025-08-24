# 完全自定义的HTML结构 + 干净CSS方案
import gradio as gr

# 干净的自定义CSS - 不依赖Gradio变量系统
CUSTOM_CSS = """
/* 重置所有Gradio默认样式 */
* {
    box-sizing: border-box;
}

body, html {
    margin: 0;
    padding: 0;
    background-color: #FEFCF3 !important;
    font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
}

/* 主容器 - 完全自定义 */
#app-container {
    background-color: #FEFCF3;
    min-height: 100vh;
    padding: 20px;
}

/* 角色选择页面 */
#selection-page {
    max-width: 1200px;
    margin: 0 auto;
    background-color: #FEFCF3;
}

#page-header {
    text-align: center;
    margin-bottom: 30px;
}

#page-title {
    color: #2e285c;
    font-size: 28px;
    font-weight: bold;
    margin-bottom: 10px;
}

#page-description {
    color: #2e285c;
    font-size: 16px;
    font-style: italic;
    max-width: 800px;
    margin: 0 auto;
}

#character-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    padding: 20px 0;
}

/* 聊天页面 */
#chat-page {
    max-width: 1400px;
    margin: 0 auto;
    background-color: #FEFCF3;
}

#chat-header {
    background-color: #bdbad4;
    color: white;
    padding: 15px 20px;
    border-radius: 12px 12px 0 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
}

#chat-layout {
    display: grid;
    grid-template-columns: 1fr 350px;
    gap: 20px;
}

/* 左侧聊天区域 */
#chat-main {
    background-color: white;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 12px rgba(46, 40, 92, 0.1);
    border: 1px solid #bdbad4;
    display: flex;
    flex-direction: column;
    min-height: 600px;
}

#chatbot-container {
    flex: 1;
    min-height: 500px;
    margin-bottom: 20px;
}

#input-area {
    display: flex;
    gap: 10px;
    align-items: flex-end;
}

#message-input-container {
    flex: 1;
}

#button-container {
    display: flex;
    flex-direction: column;
    gap: 8px;
    width: 100px;
}

/* 右侧信息面板 */
#info-sidebar {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.info-panel {
    background-color: white;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 12px rgba(46, 40, 92, 0.1);
    border: 1px solid #bdbad4;
}

.panel-title {
    color: #2e285c;
    font-size: 18px;
    font-weight: bold;
    margin: 0 0 15px 0;
    text-align: center;
}

.panel-content {
    color: #2e285c;
    font-size: 14px;
    line-height: 1.6;
}

/* 组件样式覆盖 - 针对挂载的Gradio组件 */
#chatbot-container .gradio-chatbot {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

#message-input-container textarea {
    background-color: white !important;
    border: 1px solid #bdbad4 !important;
    border-radius: 20px !important;
    padding: 12px 16px !important;
    font-size: 14px !important;
    color: #2e285c !important;
    resize: none !important;
}

#send-button button {
    background-color: #bdbad4 !important;
    color: white !important;
    font-weight: bold !important;
    border-radius: 20px !important;
    padding: 8px 15px !important;
    border: none !important;
    cursor: pointer !important;
    transition: background-color 0.2s !important;
}

#send-button button:hover {
    background-color: #2e285c !important;
}

#clear-button button {
    background-color: white !important;
    color: #2e285c !important;
    font-weight: bold !important;
    border-radius: 20px !important;
    padding: 8px 15px !important;
    border: 2px solid #bdbad4 !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
}

#clear-button button:hover {
    background-color: #f0edfe !important;
    border-color: #2e285c !important;
}

#back-button button {
    background-color: white !important;
    color: #2e285c !important;
    font-weight: bold !important;
    border-radius: 8px !important;
    padding: 8px 16px !important;
    border: 2px solid #bdbad4 !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
}

/* 响应式设计 */
@media (max-width: 1024px) {
    #chat-layout {
        grid-template-columns: 1fr;
    }
    
    #character-grid {
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    }
}

@media (max-width: 768px) {
    #app-container {
        padding: 10px;
    }
    
    #input-area {
        flex-direction: column;
    }
    
    #button-container {
        flex-direction: row;
        width: 100%;
    }
}
"""

def create_selection_page():
    """创建角色选择页面 - 完全自定义HTML结构"""
    return gr.HTML("""
        <div id="app-container">
            <div id="selection-page">
                <div id="page-header">
                    <h1 id="page-title">Digital Adolescents Chat</h1>
                    <p id="page-description">Choose a digital twin to start chatting with</p>
                </div>
                <div id="character-grid">
                    <!-- 角色卡片将通过JavaScript动态插入 -->
                </div>
            </div>
        </div>
    """)

def create_chat_page():
    """创建聊天页面 - 完全自定义HTML结构"""
    with gr.Column():
        # 自定义HTML结构
        gr.HTML("""
            <div id="app-container">
                <div id="chat-page">
                    <div id="chat-header">
                        <div id="back-button-container"></div>
                        <h2 id="chat-title">Digital Twin Chat</h2>
                        <div style="width: 100px;"></div> <!-- 占位符保持居中 -->
                    </div>
                    <div id="chat-layout">
                        <div id="chat-main">
                            <div id="chatbot-container">
                                <!-- Chatbot组件将挂载到这里 -->
                            </div>
                            <div id="input-area">
                                <div id="message-input-container">
                                    <!-- Textbox组件将挂载到这里 -->
                                </div>
                                <div id="button-container">
                                    <div id="send-button"></div>
                                    <div id="clear-button"></div>
                                </div>
                            </div>
                        </div>
                        <div id="info-sidebar">
                            <div class="info-panel">
                                <h3 class="panel-title">Character Profile</h3>
                                <div class="panel-content" id="character-info">
                                    <!-- 角色信息将动态插入 -->
                                </div>
                            </div>
                            <div class="info-panel">
                                <h3 class="panel-title">Scene Setting</h3>
                                <div class="panel-content" id="scene-controls">
                                    <!-- 场景控制将挂载到这里 -->
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        """)
        
        # Gradio组件 - 通过elem_id精确挂载
        back_btn = gr.Button("← Back", elem_id="back-button", size="sm")
        chatbot = gr.Chatbot(elem_id="chatbot-container", show_label=False, height=500)
        msg_input = gr.Textbox(
            elem_id="message-input-container", 
            show_label=False, 
            placeholder="Type your message here...",
            lines=2
        )
        send_btn = gr.Button("Send", elem_id="send-button", variant="primary")
        clear_btn = gr.Button("Clear", elem_id="clear-button", variant="secondary")
        
        # 场景控制组件
        scene_dropdown = gr.Dropdown(
            choices=["School", "Home", "Park", "Custom"],
            value="School",
            label="Scene",
            elem_id="scene-selector"
        )
        
    return back_btn, chatbot, msg_input, send_btn, clear_btn, scene_dropdown

# 主应用
def create_app():
    with gr.Blocks(css=CUSTOM_CSS, title="Digital Adolescents Chat") as demo:
        # 页面状态
        current_page = gr.State("selection")
        selected_character = gr.State(None)
        
        # 选择页面
        with gr.Group(visible=True) as selection_interface:
            create_selection_page()
            
        # 聊天页面  
        with gr.Group(visible=False) as chat_interface:
            back_btn, chatbot, msg_input, send_btn, clear_btn, scene_dropdown = create_chat_page()
            
        # 页面切换逻辑
        def switch_to_chat(character):
            return [
                gr.Group.update(visible=False),  # 隐藏选择页面
                gr.Group.update(visible=True),   # 显示聊天页面
                "chat",                          # 更新页面状态
                character                        # 保存选择的角色
            ]
            
        def switch_to_selection():
            return [
                gr.Group.update(visible=True),   # 显示选择页面
                gr.Group.update(visible=False),  # 隐藏聊天页面
                "selection",                     # 更新页面状态
                []                               # 清空聊天记录
            ]
        
        # 绑定事件（这里需要根据实际的角色选择按钮来绑定）
        back_btn.click(
            switch_to_selection,
            outputs=[selection_interface, chat_interface, current_page, chatbot]
        )
    
    return demo

if __name__ == "__main__":
    app = create_app()
    app.launch()
